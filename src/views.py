import datetime
import os
import pandas as pd
import requests
from dotenv import load_dotenv
import json
import logging

# Настройка логгера
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='..\\logs\\views.log'
)
logger = logging.getLogger(__name__)

def log_file(file="..\\logs\\reports.log"):
    """декоратор для логирования функции"""
    def report(func):
        def wrapper(*args, **kwargs):
            try:
                logger.info(f"Вызов функции {func.__name__} с аргументами {args}, {kwargs}")
                result = func(*args, **kwargs)
                with open(file, "a", encoding="utf-8") as f:
                    f.write(result)
                logger.info(f"Результат успешно записан в файл {file}")
                return result
            except Exception as e:
                logger.error(f"Ошибка в функции {func.__name__}: {str(e)}")
                raise
        return wrapper
    return report


load_dotenv(".env")

API_KEY = os.getenv("API_KEY")

symbols = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA", "^GSPC"]

date = datetime.datetime.now()


def main(date):
    current_time = date
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


def cards_information(path: str):
    """Принимает на вход путь к файлу xlsx с транзакциями, после чего возвращает информацию о картах в нем
    в виде json"""
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


def top_five_transactions(path: str):
    """Принимает на вход путь к файлу xlsx с транзакциями, после чего возвращает 5 самых больших транзакций за месяц
    в виде json"""
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
    """Функция возвращает курс валют: доллар в рублях, евро в рублях"""
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


print(main(date))
