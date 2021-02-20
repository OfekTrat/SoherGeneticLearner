from bs4 import BeautifulSoup
import requests

S_P_WIKI_URL = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"


def get_stock_list(n_stocks=10):
    # Returns stocks names out of the S&P 500 broker.
    stocks_list = []

    resp = requests.get(S_P_WIKI_URL)
    soup = BeautifulSoup(resp.text)

    table = soup.find("table", attrs={"id": "constituents"})
    table_body = table.tbody

    for row in table_body.find_all("tr"):
        columns = row.find_all("td")
        for c in columns:
            stocks_list.append(c.text.strip("\n"))
            break

    return stocks_list[:n_stocks]

