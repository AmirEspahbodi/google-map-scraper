import asyncio
from lxml import etree
from data.dao import BrowserPage
from playwright.async_api import Page, Locator
from random import choice
from config import RuntimeResource
from data.dto import Listing


class ScrapDataBo:
    def __init__(self):
        self.resource = RuntimeResource()

    async def scrap_page(self):
        browsers_pages = self.resource.browsers_pages

        result = await asyncio.gather(
            *[self.__extract_listings(browser_page) for browser_page in browsers_pages]
        )
        
        len = 0
        for re in result:
            print('=====================================================')
            broser_page_name = re[0]
            print(broser_page_name)
            for k, v in re[1].items():
                print('----------------------')
                print(k)
                print(v)

        listings_for_page = self.__assign_unique_listings_to_pages(result)

        for page, listings in listings_for_page.items():
            print(page)
            for l in listings:
                print(l)
            
            print('--------------------------------------')
        # temp1 = {
        #     browser_page.name: browser_page.page for browser_page in browsers_pages
        # }
        # final_listings = await asyncio.gather(
        #     *[
        #         self.__scrap_listings(temp1[page_name], listings)
        #         for page_name, listings in listings_for_page.items()
        #     ]
        # )
        # return final_listings

    async def __scrap_listings(self, page: Page, listings: list[Locator]):
        base_selector = "//div[@id='QA0Szd']//div[@jstcache='4']//div[contains(@class, 'm6QErb WNBkOb XiKgde')]//div[contains(@class, 'm6QErb DxyBCb kA9KIf dS8AEf XiKgde')]"
        parser = etree.HTMLParser()
        for listing in listings:
            listing_list = []
            try:
                await listing.click()
                await page.wait_for_timeout(7000)
                page_content = await page.content()
                tree = etree.fromstring(page_content, parser)

                # listing = Listing()

                # get listing title
                title_fa = tree.xpath(
                    base_selector
                    + "//div[contains(@class, 'TIHn2')]//div[contains(@class, 'lMbq3e')]//h1//span[2]/text()"
                )
                title_en = tree.xpath(
                    base_selector
                    + "//div[contains(@class, 'TIHn2')]//div[contains(@class, 'lMbq3e')]//h1/text()"
                )
                title = title_en or title_fa

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

                # # get location
                location_in_map = page.url

                # active hourse
                active_hours = tree.xpath(
                    base_selector
                    + "//div[contains(@class, 'OqCZI fontBodyMedium WVXvdc')]/div[2]/@aria-label"
                )

                print(f"title = {title}")
                print(f"category = {category}")
                print(f"address = {address}")
                print(f"phone_number = {phone_number}")
                print(f"website = {website}")
                print(f"location_in_map = {location_in_map}")
                print(f"active_hours = {active_hours}")
                print(" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")

                # listing_list.append(listing)

            except Exception as e:
                print(f"Error occured: {e}")

        return listing_list

    @staticmethod
    def __assign_unique_listings_to_pages(input: list[dict]):
        """
        mess up listings collected from each page
        Most listings collected from the pages have overlaps,
        so a listing may be scraped from more than one page.
        The purpose of this function is to identify such listings
        and assign each listing to a single page.


        Args:
            result: listing collected from each page

        Output: Specifies the listings for each page to be clicked and scraped.
        """

        # step 1
        """
        in this step we created a dict 
        and added all listings with same key to a list with their browser tab name (browser_tab_name, listing)
        and assigned this list to dict by key
        """
        temp1 = {}
        for result in input:
            browser_page = result[0]
            for k, v in result[1].items():
                if k in temp1:
                    if isinstance(v, list):
                        temp1[k].extends(list(map(lambda x: (browser_page.name, x), v)))
                    else:
                        temp1[k].append((browser_page.name, v))
                else:
                    if isinstance(v, list):
                        temp1[k] = list(map(lambda x: (browser_page.name, x), v))
                    else:
                        temp1[k] = [(browser_page.name, v)]

        # step 2
        """
        in this step we randomly chosing (browser_tab_name, listing) from each dict item
        in other word for each key we chose a browser and listing
        this browsers tab will sccrap that listing later 
        """
        temp2 = []
        for key, value in temp1.items():
            temp2.append(choice(value))

        # step3
        """
        post processing data
        for each browser we will create list ao listing to scrape
        based on listings selected on step 2
        """
        final_result = {}
        for value in temp2:
            if value[0] in final_result:
                final_result[value[0]].append(value[1])
            else:
                final_result[value[0]] = [value[1]]

        return final_result

    @staticmethod
    async def __extract_listings(browser_page: BrowserPage):
        try:
            """
            :param page:
            :return:
            a dict of <listing_title+autor phone_number, listings>
            """
            listings = await browser_page.page.locator(
                '//a[contains(@href, "https://www.google.com/maps/place")]'
            ).all()
            listings = [listing.locator("xpath=..") for listing in listings]

            parser = etree.HTMLParser()
            base_selector = "//div[contains(@class, 'lI9IFe')]//div[contains(@class, 'Z8fK3b')]//div[contains(@class, 'UaQhfb')]"

            result = {}

            for listing in listings:
                tree = etree.fromstring(await listing.inner_html(), parser)
                if tree is not None:
                    title_en = tree.xpath(
                        base_selector
                        + "//div[contains(@class, 'NrDZNb')]//div[contains(@class, 'qBF1Pd')]/text()"
                    )
                    title_fa = tree.xpath(
                        base_selector
                        + "//div[contains(@class, 'NrDZNb')]//div[contains(@class, 'qBF1Pd')]//span/text()"
                    )
                    title = title_en or title_fa
                    phone = tree.xpath(
                        base_selector
                        + "//div[contains(@class, 'W4Efsd')]//span[contains(@class, 'UsdlK')]/text()"
                    )
                    short_address_en = tree.xpath(
                        base_selector
                        + "//div[contains(@class, 'W4Efsd')][2]//div[contains(@class, 'W4Efsd')][1]//span[2]//span[2]/text()"
                    )
                    short_address_fa = tree.xpath(
                        base_selector
                        + "//div[contains(@class, 'W4Efsd')][2]//div[contains(@class, 'W4Efsd')][1]//span[2]//span[2]//span/text()"
                    )

                    short_address = short_address_en or short_address_fa

                    # print("Title:", title)
                    # print("Phone:", phone)
                    # print("short_address:", short_address)

                    if phone:
                        phone = phone[0].strip()

                    if title:
                        title = title[0].strip()

                    if short_address:
                        short_address = short_address[0].strip()

                    if phone and title and short_address:
                        if phone in result:
                            result[
                                f"{title} - {phone} - {short_address}"
                                + f"_{len(result[f"{title} - {phone} - {short_address}"])}"
                            ] = listing
                        else:
                            result[f"{title} - {phone} - {short_address}"] = listing
                    elif phone and title:
                        if phone in result:
                            result[
                                f"{title} - {phone}"
                                + f"_{len(result[f"{title} - {phone}"])}"
                            ] = listing
                        else:
                            result[f"{title} - {phone}"] = listing
                    elif phone and short_address:
                        if phone in result:
                            result[
                                f"{phone} - {short_address}"
                                + f"_{len(result[f"{phone} - {short_address}"])}"
                            ] = listing
                        else:
                            result[f"{phone} - {short_address}"] = listing
                    elif title and short_address:
                        if f"{title} - {short_address}" in result:
                            result[
                                f"{title} - {short_address}"
                                + f"_{len(result[f"{title} - {short_address}"])}"
                            ] = listing
                        else:
                            result[f"{title} - {short_address}"] = listing
                    else:
                        if phone:
                            if phone in result:
                                result[phone + f"_{len(result[phone])}"] = listing
                            else:
                                result[phone] = listing
                        if short_address:
                            if short_address in result:
                                result[
                                    short_address + f"_{len(result[short_address])}"
                                ] = listing
                            else:
                                result[short_address] = listing
                        if title:
                            if title in result:
                                result[title + f"_{len(result[title])}"] = listing
                            else:
                                result[title] = listing
            return browser_page, result

        except BaseException as e:
            print(
                f"error in ScrapDataBo in __extract_listings function\nerror: {e}\npage={browser_page.name}"
            )
