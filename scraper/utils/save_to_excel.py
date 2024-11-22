import pandas as pd
from pathlib import Path


def save_to_excel(final_listings: dict, search_query):
    Path("../results").mkdir(parents=True, exist_ok=True)
    print("writing data to csv file")
    df = pd.DataFrame(final_listings)
    df.to_excel(f"../results/{search_query}.xlsx", index=False)
