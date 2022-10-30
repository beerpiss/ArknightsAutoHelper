import json
import requests
import os


def get_table(lang, table):
    return requests.get(
        f"https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/{lang}/gamedata/excel/{table}_table.json"
    ).text


item_table_cn = json.loads(get_table("zh_CN", "item"))
item_table_en = json.loads(get_table("en_US", "item"))

for (_, val) in item_table_cn["items"].items():
    item_id = val["itemId"]
    for path in ["archive", "not-loot"]:
        if os.path.exists(f"./{path}/{val['name']}.png"):
            os.rename(
                f"./{path}/{val['name']}.png",
                f"./{path}/{item_table_en['items'][item_id]['name']}.png",
            )
