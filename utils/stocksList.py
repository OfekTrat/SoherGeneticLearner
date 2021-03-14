import pandas as pd
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm

STOCKS_URL = "https://swingtradebot.com/equities?page={}"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
}


def get_stock_list(n_stocks=-1):
    i = 1
    resp = requests.get(STOCKS_URL.format(i), headers=HEADERS)
    bar_tqdm = tqdm(total=131)
    total = []

    while resp.status_code == 200:
        soup = BeautifulSoup(resp.text)
        table = soup.find("tbody")

        tr = table.find_all("tr")
        for row in tr:
            td = row.find_all("td")[0]
            symbol = td.a.contents[0]
            title = td.a.attrs["title"]
            total.append({"symbol": symbol, "name": title})

        bar_tqdm.update()
        i += 1
        resp = requests.get(STOCKS_URL.format(i), headers=HEADERS)

    all_stocks = pd.DataFrame(total)

    return all_stocks
