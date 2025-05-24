import datetime
import os
import pandas as pd
import requests
from dotenv import load_dotenv
import json

load_dotenv(".env")

API_KEY = os.getenv("API_KEY")

symbols = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA", "^GSPC"]


def main():
    current_time = datetime.datetime.now().time()
    hour = current_time.hour
    json_answer = {}

    if 5 <= hour < 12:
        json_answer["greeting"] = "Доброе утро!"
    elif 12 <= hour < 17:
        json_answer["greeting"] = "Добрый день!"
    elif 17 <= hour < 22:
        json_answer["greeting"] = "Добрый вечер!"
    else:
        json_answer["greeting"] = "Доброй ночи!"

    stock_data = []
    for symbol in symbols:
        data = get_stock_price(symbol)
        if data:
            stock_data.append(data)

    json_answer["cards"] = cards_information("..\\data\\operations.xlsx")
    json_answer["top_transactions"] = top_five_transactions("..\\data\\operations.xlsx")
    json_answer["currency_rates"] = currency_get()
    json_answer["stock_prices"] = json.dumps(stock_data)

    return json_answer


def cards_information(path):
    today_date = datetime.datetime.now().date()

    start_date = today_date.replace(day=1)

    transactions = pd.read_excel(path, engine="openpyxl")

    transactions['Дата операции'] = pd.to_datetime(transactions['Дата операции'], dayfirst=True).dt.date

    transactions = transactions[
        (transactions['Дата операции'] >= start_date) &
        (transactions['Дата операции'] <= today_date)
        ]

    cards_data = transactions.groupby('Номер карты', dropna=True).agg(
        total_spent=('Сумма платежа', 'sum'),
        cashback=('Сумма платежа', lambda x: sum(x) // 100)
    ).reset_index()

    result = cards_data.to_dict("records")

    for elem in result:
        elem["total_spent"] = abs(elem["total_spent"])
        elem["cashback"] = abs(elem["cashback"])

    return result


def top_five_transactions(path):
    today_date = datetime.datetime.now().date()

    start_date = today_date.replace(day=1)

    transactions = pd.read_excel(path, engine="openpyxl")

    transactions['Дата операции'] = pd.to_datetime(transactions['Дата операции'], dayfirst=True).dt.date

    transactions = transactions[
        (transactions['Дата операции'] >= start_date) &
        (transactions['Дата операции'] <= today_date)
        ]

    transactions['Сумма'] = transactions['Сумма платежа'].abs()

    top_5 = transactions.nlargest(5, "Сумма")

    top_5 = top_5[["Дата операции", "Сумма", "Категория", "Описание"]].to_dict("records")

    for transaction in top_5:
        transaction["Дата операции"] = transaction["Дата операции"].strftime("%d.%m.%Y")

    return top_5


def currency_get():
    url = "https://www.cbr-xml-daily.ru/daily_json.js"
    response = requests.get(url).json()

    usd_rate = round(response["Valute"]["USD"]["Value"], 2)
    eur_rate = round(response["Valute"]["EUR"]["Value"], 2)
    return [{"currency": "USD", "rate": usd_rate}, {"currency": "EUR", "rate": eur_rate}]


def get_stock_price(symbol):
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}"
    response = requests.get(url).json()

    if "Global Quote" in response:
        return {
            "stock": symbol,
            "price": float(response["Global Quote"]["05. price"])
        }
    return None
