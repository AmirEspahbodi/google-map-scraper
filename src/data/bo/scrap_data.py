import traceback
import asyncio
import json
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

        listings_for_page = self.__assign_unique_listings_to_pages(result)

        # for page_name, listings_and_key in listings_for_page.items():
        #     print(page_name)  # browser tab name
        #     for l in listings_and_key:
        #         print(l[0])  # listings
        #         print(l[1])  # key
        #     print("--------------------------------------")

        browser_selector = {
            browser_page.name: browser_page.page for browser_page in browsers_pages
        }
        pre_final_listings = await asyncio.gather(
            *[
                self.__scrap_listings(browser_selector[page_name], listings, page_name)
                for page_name, listings in listings_for_page.items()
            ]
        )
        final_listings = []
        for re in pre_final_listings:
            final_listings.extend(re)
        return final_listings

    @staticmethod
    def __assign_unique_listings_to_pages(input: list[tuple[str, dict]]):
        """
        mess up listings collected from each page
        Most listings collected from the pages have overlaps,
        so a listing may be scraped from more than one page.
        The purpose of this function is to identify such listings
        and assign each listing to a single page.

        input:
        list of tuple[browser_page_name, dict]
        dict is key:listing
            key is combine of title, phone, short_addresss


        Output:
        Specifies the unique listings for each page to be clicked and scraped.
        """

        # step 1
        """
        in this step we created a dict 
        and added all listings with same key to a list with their browser tab name
        key:= list of (browser_tab_name, listing)
        and assigned this list to dict by key
        """
        temp1 = {}
        for result in input:
            browser_page = result[0]
            key_listing_dict = result[1]
            for key, listings in key_listing_dict.items():
                if key in temp1:
                    temp1[key].extend(
                        list(map((lambda x: (browser_page.name, x, key)), listings))
                    )
                else:
                    temp1[key] = list(
                        map((lambda x: (browser_page.name, x, key)), listings)
                    )

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
                final_result[value[0]].append((value[1], value[2]))
            else:
                final_result[value[0]] = [(value[1], value[2])]

        return final_result

    @staticmethod
    async def __extract_listings(browser_page: BrowserPage):
        """
        :param page:
        :return:
        browser_page_name, a dict

        dict is: key: listings
            key is combine of <title, phone, short_address>
        """
        listings = await browser_page.page.locator(
            '//a[contains(@href, "https://www.google.com/maps/place")]'
        ).all()
        listings = [listing.locator("xpath=..") for listing in listings]

        parser = etree.HTMLParser()
        base_selector = "//div[contains(@class, 'lI9IFe')]//div[contains(@class, 'Z8fK3b')]//div[contains(@class, 'UaQhfb')]"

        result = {}

        for listing in listings:
            try:
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
                        if f"{title} - {phone} - {short_address}" in result:
                            result[f"{title} - {phone} - {short_address}"].append(
                                listing
                            )
                        else:
                            result[f"{title} - {phone} - {short_address}"] = [listing]
                    elif phone and title:
                        if f"{title} - {phone}" in result:
                            result[f"{title} - {phone}"].append(listing)
                        else:
                            result[f"{title} - {phone}"] = [listing]
                    elif phone and short_address:
                        if f"{phone} - {short_address}" in result:
                            result[f"{phone} - {short_address}"].append(listing)
                        else:
                            result[f"{phone} - {short_address}"] = [listing]
                    elif f"{title} - {short_address}" and short_address:
                        if f"{title} - {short_address}" in result:
                            result[f"{title} - {short_address}"].append(listing)
                        else:
                            result[f"{title} - {short_address}"] = [listing]
                    else:
                        if phone:
                            if phone in result:
                                result[phone].append(listing)
                            else:
                                result[phone] = [listing]
                        if short_address:
                            if short_address in result:
                                result[short_address].append(listing)
                            else:
                                result[short_address] = [listing]
                        if title:
                            if title in result:
                                result[title].append(listing)
                            else:
                                result[title] = [listing]

            except Exception as e:
                print("error in ScrapDataBo in __extract_listings function:")
                print(f"Error: {e}")
                print(f"page: {browser_page.name}")
                traceback.print_exc()

        return browser_page, result

    async def __scrap_listings(
        self, page: Page, listings_keys: list[Locator], browser_page_name
    ):
        base_selector = "//div[@id='QA0Szd']//div[@jstcache='4']//div[contains(@class, 'm6QErb WNBkOb XiKgde')]//div[contains(@class, 'm6QErb DxyBCb kA9KIf dS8AEf XiKgde')]"
        parser = etree.HTMLParser()
        listing_list = []
        for listing_key in listings_keys:
            listing, key = listing_key
            try:
                await listing.click()
                await page.wait_for_timeout(7000)
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

                listing_list.append(
                    json.dumps(
                        {
                            "title": title,
                            "category": category,
                            "address": address,
                            "phone_number": phone_number,
                            "website": website,
                            "location_in_map": location_in_map,
                            "active_hours": active_hours,
                            "browser_page_name": browser_page_name,
                            "key": key,
                        }
                    )
                )

            except Exception as e:
                print("in ScrapDataBo.__scrap_listings:")
                print(f"Error: {e}")
                traceback.print_exc()

        return listing_list
