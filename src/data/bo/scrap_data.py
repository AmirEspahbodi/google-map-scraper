import asyncio
from lxml import etree
from data.dao import BrowserPage
from random import choice
from config import RuntimeResource


class ScrapDataBo:
    def __init__(self):
        self.resource = RuntimeResource()

    async def scrap_page(self):
        browsers_pages = self.resource.browsers_pages

        result = await asyncio.gather(
            *[self.__extract_listings(browser_page) for browser_page in browsers_pages]
        )

        listings_for_page = self.__assign_unique_listings_to_pages(result)

        for page_name, listings in listings_for_page.items():
            print(page_name)
            print(listings)
            print()

        # await asyncio.gather(*[self.__scrap_listings(browser_page) for browser_page in browsers_pages])

    async def __scrap_listings(self, page: BrowserPage):
        pass

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
        temp2 = {}
        for key, value in temp1.items():
            temp2[key] = choice(value)

        # step3
        final_result = {}
        for value in temp2.values():
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
