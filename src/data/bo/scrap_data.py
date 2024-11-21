import asyncio
from lxml import etree
from playwright.async_api import Page


class ScrapDataBo:
    def __init__(self):
        pass

    async def scrap_page(self, pages: list[Page]):
        result = await asyncio.gather(
            *[self.__extract_listings(page) for page in pages]
        )

        listings_for_page = self.__assign_unique_listings_to_pages(result)

        await asyncio.gather(*[page.pause() for page in pages])

        await asyncio.gather(*[self.__scrap_listings(page) for page in pages])

    async def __scrap_listings(self, page: Page):
        pass

    @staticmethod
    def __assign_unique_listings_to_pages(result):
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

        return result

    @staticmethod
    async def __extract_listings(page: Page):
        """
        :param page:
        :return:
        a dict of <listing_title+autor phone_number, listings>
        """
        listings = await page.locator(
            '//a[contains(@href, "https://www.google.com/maps/place")]'
        ).all()
        listings = [listing.locator("xpath=..") for listing in listings]

        parser = etree.HTMLParser()
        base_selector = "//div[contains(@class, 'lI9IFe')]//div[contains(@class, 'Z8fK3b')]//div[contains(@class, 'UaQhfb')]"

        result = {}
        no_unique_key = []

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

                if phone and title and short_address:
                    result[f"{title[0]} - {phone[0]} - {short_address[0]}"] = listing
                elif phone and title:
                    result[f"{title[0]} - {phone[0]}"] = listing
                elif phone and short_address:
                    result[f"{phone[0]} - {short_address[0]}"] = listing
                elif title and short_address:
                    result[f"{title[0]} - {short_address[0]}"] = listing
                else:
                    no_unique_key.append(listing)
            else:
                continue

        result["no_unique_key"] = no_unique_key

        return result
