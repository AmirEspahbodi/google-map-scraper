import traceback
from lxml import etree
from playwright.async_api import Page, Locator
from random import randint

async def scrap_pictures(page: Page, base_selector, key, browser_page_name):
    
    photo_base_selector = "//div[@id='QA0Szd']//div[@jstcache=15]//div[@jstcache='3']//div[contains(@class, 'm6QErb DxyBCb kA9KIf dS8AEf XiKgde')]"
    try:
        selector = "//div[contains(@class, 'ZKCDEc')]//button[contains(@aria-label, 'Photo of')]"
        photo_button = page.locator(base_selector+selector)
        if await photo_button.count() > 0:
            await photo_button.click()
            await page.wait_for_load_state("networkidle")
            await page.wait_for_timeout(randint(7500, 10500))
        else:
            print(f"000000000000000000000000000 no photo found {browser_page_name} - {key}")
            return ['']
    except Exception as e:
        print("in ScrapDataBo.__scrap_listings part 1:")
        print(f"browser: {browser_page_name}")
        print(f"key: {key}")
        print(f"Error: {e}")
        traceback.print_exc()
        return [""]
        
    try:
        page_content = await page.content()
        parser = etree.HTMLParser()
        tree = etree.fromstring(page_content, parser)
        photos_style_selector = photo_base_selector+"//a[contains(@class, 'OKAoZd')]//div[contains(@class, 'Uf0tqf loaded')]/@style"
        photos = tree.xpath(photos_style_selector)
        if photos:
            count = 0
            for photo in photos:
                count+=1
                if count >= 6:
                    break
                print(photo)
    except Exception as e:
        print("in ScrapDataBo.__scrap_listings part 2:")
        print(f"browser: {browser_page_name}")
        print(f"key: {key}")
        print(f"Error: {e}")
        traceback.print_exc()
        
    try:
        back_button_selector1 = photo_base_selector + "//button[contains(@aria-label, 'Back')]"
        back_button_selector2 = photo_base_selector + "//button[contains(@class, 'iPpe6d')]"
        back_button_selector3 = '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/button[1]'
        back_button1 = page.locator(back_button_selector1)
        back_button2 = page.locator(back_button_selector2)
        back_button3 = page.locator(back_button_selector3)
        
        if await back_button1.count()>0:
            pass
        elif await back_button2.count()>0:
            await back_button2.click()
        elif await back_button3.count()>0:
            await back_button3.click()
        else:
            await page.pause()
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(randint(7500, 10500))
        
    except Exception as e:
        print("in ScrapDataBo.__scrap_listings part 3:")
        print(f"browser: {browser_page_name}")
        print(f"key: {key}")
        print(f"Error: {e}")
        traceback.print_exc()
        return ['']
