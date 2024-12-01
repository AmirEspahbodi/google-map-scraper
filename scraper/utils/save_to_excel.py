import pandas as pd
from pathlib import Path
from config.app import AppConfig


def save_to_excel(
    final_listings: list[dict], listing_category: str, search_query: str, province: str
):
    file_name = (
        f"{listing_category}"
        f"{AppConfig.SEARCH_QUERY_ITEMS_SEPARATOR}"
        f"{search_query}"
        f"{AppConfig.SEARCH_QUERY_ITEMS_SEPARATOR}"
        f"{province}"
        f"{AppConfig.SEARCH_QUERY_ITEMS_SEPARATOR}"
    )
    dirs = AppConfig.NOT_IMPORTED_SHEETS_DIRECTORY.split("/")
    for dir_count in range(len(dirs)):
        Path(
            f"{AppConfig.PARENT_DIRECTORY_PROJECTS_MAIN_FILE}/{"/".join(dirs[0:dir_count+1])}"
        ).mkdir(parents=True, exist_ok=True)

    print("scraper ->writing data to excel file")
    df = pd.DataFrame(final_listings)
    df.to_excel(
        f"{AppConfig.PARENT_DIRECTORY_PROJECTS_MAIN_FILE}/{AppConfig.NOT_IMPORTED_SHEETS_DIRECTORY}/{file_name}.xlsx",
        index=False,
    )
