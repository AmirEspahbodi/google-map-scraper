import pandas as pd
import json

# Convert Excel To Json With Python

# Print the JSON data


def test_repetitive_listing():
    path = "../storage/scraped_excel/ __ آبمیوه و بستنی در  تهران.xlsx"
    data = pd.read_excel(path, sheet_name="Sheet1")
    dict_data = data.to_dict(orient="records")
    for index, l_id in enumerate(data["listing_unique_id"]):
        for index_i, l_id_i in enumerate(data["listing_unique_id"]):
            if index != index_i:
                if l_id == l_id_i:
                    print(
                        f"SCRAPER ->error\nlisting_unique_id: {l_id},  is duplicate\n"
                    )


test_repetitive_listing()
