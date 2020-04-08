import requests
from bs4 import BeautifulSoup 
import json
import time

def get_api_stock_data(company_str):
    r = requests.get(f"https://financialmodelingprep.com/api/v3/historical-price-full/{company_str}?timeseries=100")
    response = json.loads(r.text)

    with open('TSLA_100_days_stock.json', 'w') as f:
        f.write(r.text)

    for historical in response["historical"]:
        print(historical['date'])

    


def __main__():
    try:
        with open('TSLA_100_days_stock.json') as f:
            data = json.loads(f.read())
            print(len(data['historical']))
        print("Didn't Access The API!")
    except FileNotFoundError:
        get_api_stock_data('TSLA')


if __name__ == '__main__':
    __main__()