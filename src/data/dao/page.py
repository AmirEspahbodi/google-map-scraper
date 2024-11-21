from playwright.async_api import Page


class BrowserPage:
    name: str  # unique
    page: Page

    def __init__(self, name, page):
        self.name = name
        self.page = page
