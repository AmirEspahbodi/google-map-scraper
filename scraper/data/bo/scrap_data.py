import traceback
import asyncio
from lxml import etree
from data.dao import BrowserPage
from playwright.async_api import Page, Locator
from random import choice, randint
from config import RuntimeResource
from utils import save_image
from config import AppConfig


class ScrapDataBo:
    def __init__(self):
        self.resource = RuntimeResource()

    async def scrap_page(self):
        browsers_pages = self.resource.browsers_pages

        print("SCRAPER ->extracting listings")
        result = await asyncio.gather(
            *[self._extract_listings(browser_page) for browser_page in browsers_pages]
        )

        listings_for_page = self._assign_unique_listings_to_pages(result)

        # await self.__test_assign_unique_listings_to_pages(listings_for_page)

        print("SCRAPER ->start scraping listings")

        final_listings = await self._scrap_listings(listings_for_page)
        return final_listings

    async def _scrap_listings(self, listings_for_page):
        base_selector = "//div[@id='QA0Szd']//div[@jstcache='4']//div[contains(@class, 'm6QErb WNBkOb XiKgde')]//div[contains(@class, 'm6QErb DxyBCb kA9KIf dS8AEf XiKgde')]"
        listing_list = []
        lock = asyncio.Lock()

        async def individual_page_scrap_listing(
            page: Page, listings: list[Locator], browser_page_name
        ):
            parser = etree.HTMLParser()
            for listing in listings:
                try:
                    short_listing_inner_html = await listing.inner_html()
                    short_listing_inner_html_tree = etree.fromstring(
                        short_listing_inner_html, parser
                    )
                    latitude, longitude, phone, title = (
                        self.__get_listing_unique_id_items(
                            short_listing_inner_html, short_listing_inner_html_tree
                        )
                    )
                    listing_unique_id = f"{latitude}_{longitude}"
                    if phone:
                        listing_unique_id += f"_{phone}"
                    if title:
                        listing_unique_id += f"_{title}"

                    print(f"SCRAPER ->scraping {listing_unique_id}")
                    await listing.click(timeout=120000)
                    await page.wait_for_timeout(randint(7000, 10000))
                    page_content = await page.content()
                    tree = etree.fromstring(page_content, parser)

                    # get listing title
                    title_fa = tree.xpath(
                        base_selector
                        + "//div[contains(@class, 'TIHn2')]//div[contains(@class, 'lMbq3e')]//h1//span[2]/text()"
                    )
                    title_en = tree.xpath(
                        base_selector
                        + "//div[contains(@class, 'TIHn2')]//div[contains(@class, 'lMbq3e')]//h1/text()"
                    )
                    title = title_fa if title_fa else title_en if title_en else ""

                    # get listing category
                    category = tree.xpath(
                        base_selector
                        + "//div[contains(@class, 'TIHn2')]//button[contains(@class, 'DkEaL')]/text()"
                    )

                    # get listing addrress
                    address = tree.xpath(
                        base_selector
                        + "//div[contains(@class, 'm6QErb XiKgde')]//button[@class='CsEnBe' and @data-tooltip='Copy address']/@aria-label"
                    )

                    # get phone number
                    phone_number = tree.xpath(
                        base_selector
                        + "//div[contains(@class, 'm6QErb XiKgde')]//button[@class='CsEnBe' and @data-tooltip='Copy phone number']/@aria-label"
                    )

                    # get website
                    website = tree.xpath(
                        base_selector
                        + "//div[contains(@class, 'm6QErb XiKgde')]//a[@class='CsEnBe' and @data-tooltip='Open website']/@href"
                    )

                    # active hourse
                    active_hours = tree.xpath(
                        base_selector
                        + "//div[contains(@class, 'OqCZI fontBodyMedium WVXvdc')]/div[2]/@aria-label"
                    )

                    # get picture
                    image_img_src = tree.xpath(
                        "//button[contains(@class, 'aoRNLd kn2E5e NMjTrf lvtCsd')]//img/@src"
                    )

                    pictures_path = ""
                    if image_img_src:
                        pictures_path = await save_image(image_img_src[0])
                    async with lock:
                        listing_list.append(
                            {
                                "title": title[0] if title else "",
                                "category": category[0] if category else "",
                                "address": address[0] if address else "",
                                "phone_number": phone_number[0]
                                if phone_number
                                else "09373110981",
                                "website": website[0] if website else "",
                                "latitude": latitude if latitude else "",
                                "longitude": longitude if longitude else "",
                                "active_hours": active_hours[0]
                                if active_hours
                                else "",
                                "browser_page_name": browser_page_name,
                                "listing_unique_id": listing_unique_id,
                                "pictures_path": pictures_path,
                                "description": "",
                            }
                        )

                except Exception as e:
                    print("SCRAPER ->in ScrapDataBo.__scrap_listings:")
                    print(f"SCRAPER ->browser: {browser_page_name}")
                    print(f"SCRAPER ->listing_unique_id: {listing_unique_id}")
                    print(f"SCRAPER ->Error: {e}")
                    traceback.print_exc()

        browsers_pages = self.resource.browsers_pages
        browser_selector = {
            browser_page.name: browser_page.page for browser_page in browsers_pages
        }
        await asyncio.gather(
            *[
                individual_page_scrap_listing(
                    browser_selector[page_name], listings, page_name
                )
                for page_name, listings in listings_for_page.items()
            ]
        )
        return listing_list

    async def _extract_listings(
        self, browser_page: BrowserPage
    ) -> dict[str, dict[str, str | Locator]]:
        """
        :param page:
        :return:
        browser_page_name, a dict

        dict is: key: listings
            key is combine of <latitude, longitude, title, phone>
        """
        listings = await browser_page.page.locator(
            '//a[contains(@href, "https://www.google.com/maps/place")]'
        ).all()
        listings = [listing.locator("xpath=..") for listing in listings]

        parser = etree.HTMLParser()

        result = {}

        for listing in listings:
            try:
                tree = etree.fromstring(await listing.inner_html(), parser)
                if tree is not None:
                    listing_inner_html = await listing.inner_html()

                    latitude, longitude, phone, title = (
                        self.__get_listing_unique_id_items(listing_inner_html, tree)
                    )

                    listing_unique_id = f"{latitude}_{longitude}"
                    if phone:
                        listing_unique_id += f"_{phone}"
                    if title:
                        listing_unique_id += f"_{title}"

                    result[listing_unique_id] = {
                        "browser_tab_name": browser_page.name,
                        "listing_locator": listing,
                    }

            except Exception as e:
                print("SCRAPER ->error in ScrapDataBo in __extract_listings function:")
                print(f"SCRAPER ->Error: {e}")
                print(f"SCRAPER ->page: {browser_page.name}")
                traceback.print_exc()

        return result

    def _assign_unique_listings_to_pages(
        self, input: list[tuple[str, dict[str, dict[str, str | Locator]]]]
    ) -> dict[str, list[Locator]]:
        """
        step 1
        Listings collected from different browser tabs sometimes overlap.
        At this stage, listings that share common attributes should be
        grouped into a single list so that one can later be selected from them.
        To achieve this, a dictionary is created where the key is the listing_unique_id,
        and the value for each key is a list of listing locators corresponding to that listing_unique_id.
        """
        step1: dict[str, list[dict[str, str | Locator]]] = {}
        for lisings_unique_id__listing_browser in input:
            for (
                listing_unique_id,
                listing_locator__browser_tab_name,
            ) in lisings_unique_id__listing_browser.items():
                if not listing_unique_id in step1:
                    step1[listing_unique_id] = [listing_locator__browser_tab_name]
                else:
                    step1[listing_unique_id].append(listing_locator__browser_tab_name)

        """
        An empty list is initialized, and the dictionary created in the previous step is iterated over.
        From each value in the dictionary (which is a list of listing_locator and browser_tab_name),
        one item is randomly selected, ensuring that, in the end,
        all browser tabs contribute an equal number of listing_locators.
        """
        step2 = []
        for listing_unique_id, listing_locator__browser_tab_name_list in step1.items():
            step2.append(choice(listing_locator__browser_tab_name_list))

        """
        The list from the previous step is processed, and for each item in the list,
        which includes listing_locator and browser_tab_name, the value of listing_locator
        is assigned to a dictionary with browser_tab_name as the key.
        """
        step3 = {browser_page.name: [] for browser_page in self.resource.browsers_pages}
        for listing_locator__browser_tab_name in step2:
            broser_tab_name = listing_locator__browser_tab_name["browser_tab_name"]
            listing_locator = listing_locator__browser_tab_name["listing_locator"]
            step3[broser_tab_name].append(listing_locator)

        return step3

    @staticmethod
    def __extract_coordinates_from_listing_inner_html(
        short_listing_inner_html: str,
    ) -> tuple[float, float]:
        """helper function to extract coordinates from url"""

        parser = etree.HTMLParser()
        tree = etree.fromstring(short_listing_inner_html, parser)

        url = tree.xpath(
            '//a[contains(@href, "https://www.google.com/maps/place")]/@href'
        )

        latitude_side, longitude_side = url[0].split("!4d")
        latitude = latitude_side.split("!3d")[-1]
        longitude = longitude_side.split("!16s")[0]
        # return latitude, longitude

        return float(latitude), float(longitude)

    def __get_listing_unique_id_items(self, listing_inner_html, tree):
        base_selector = "//div[contains(@class, 'lI9IFe')]//div[contains(@class, 'Z8fK3b')]//div[contains(@class, 'UaQhfb')]"

        latitude, longitude = self.__extract_coordinates_from_listing_inner_html(
            listing_inner_html
        )
        title_en = tree.xpath(
            base_selector
            + "//div[contains(@class, 'NrDZNb')]//div[contains(@class, 'qBF1Pd')]/text()"
        )
        title_fa = tree.xpath(
            base_selector
            + "//div[contains(@class, 'NrDZNb')]//div[contains(@class, 'qBF1Pd')]//span/text()"
        )
        phone = tree.xpath(
            base_selector
            + "//div[contains(@class, 'W4Efsd')]//span[contains(@class, 'UsdlK')]/text()"
        )

        if phone:
            phone = phone[0].strip()

        title = title_en if title_en else title_fa if title_fa else None
        if title:
            title: str = title[0].strip()
            title = title.replace(" ", "_")

        return latitude, longitude, phone, title

    async def __test_assign_unique_listings_to_pages(
        self, input: dict[str, list[Locator]]
    ):
        print(
            "SCRAPER ->* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * "
        )
        print("SCRAPER ->__test_assign_unique_listings_to_pages result")

        data = []
        for key, value in input.items():
            browser_page_listings = value
            data.append(browser_page_listings)

        listings_unique_id_items: list[dict[str, str]] = []

        lock = asyncio.Lock()

        async def get_listings_unique_id_items(browser_page_listings: list[Locator]):
            parser = etree.HTMLParser()

            for listing in browser_page_listings:
                tree = etree.fromstring(await listing.inner_html(), parser)
                try:
                    listing_inner_html = await listing.inner_html()

                    latitude, longitude, phone, title = (
                        self.__get_listing_unique_id_items(listing_inner_html, tree)
                    )
                    async with lock:
                        listings_unique_id_items.append(
                            {
                                "latitude": latitude,
                                "longitude": longitude,
                                "phone": phone,
                                "title": title,
                            }
                        )
                except Exception as e:
                    pass

        await asyncio.gather(*[get_listings_unique_id_items(d) for d in data])

        for index, listing_unique_id_item in enumerate(listings_unique_id_items):
            for index_i, listing_unique_id_item_i in enumerate(
                listings_unique_id_items
            ):
                if index != index_i:
                    if (
                        listing_unique_id_item["latitude"]
                        == listing_unique_id_item_i["latitude"]
                        and listing_unique_id_item["longitude"]
                        == listing_unique_id_item_i["longitude"]
                    ):
                        listing_unique_id = f"{listing_unique_id_item["latitude"]}_{listing_unique_id_item["longitude"]}"
                        if listing_unique_id_item["phone"]:
                            listing_unique_id += f"_{listing_unique_id_item["phone"]}"
                        if listing_unique_id_item["title"]:
                            listing_unique_id += f"_{listing_unique_id_item["title"]}"

                        listing_unique_id_i = f"{listing_unique_id_item_i["latitude"]}_{listing_unique_id_item_i["longitude"]}"
                        if listing_unique_id_item_i["phone"]:
                            listing_unique_id += f"_{listing_unique_id_item_i["phone"]}"
                        if listing_unique_id_item_i["title"]:
                            listing_unique_id += f"_{listing_unique_id_item_i["title"]}"

                        print(
                            f"SCRAPER ->listings {listing_unique_id} and {listing_unique_id_i}"
                        )
        print(
            "SCRAPER ->* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * "
        )
