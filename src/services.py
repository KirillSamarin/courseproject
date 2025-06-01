import pandas as pd
import json
import logging

# Настройка логгера
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='..\\logs\\services.log'
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



def search_by_word(transactions: pd.DataFrame, search: str) -> json:
    """функция для поиска транзакция по слову, принимает dataframe и слово для поиска, вовзвращает в виде json"""
    search = search.lower()

    mask = (
            transactions['Описание'].str.lower().str.contains(search) |
            (transactions['Категория'].str.lower().str.contains(search)
             ))

    transactions_return = transactions[mask]

    return transactions_return.to_json(orient='records', force_ascii=False)
