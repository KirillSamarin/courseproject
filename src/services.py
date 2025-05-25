import pandas as pd
import json


def search_by_word(transactions: pd.DataFrame, search: str) -> json:
    """функция для поиска транзакция по слову, принимает dataframe и слово для поиска, вовзвращает в виде json"""
    search = search.lower()

    mask = (
            transactions['Описание'].str.lower().str.contains(search) |
            (transactions['Категория'].str.lower().str.contains(search)
             ))

    transactions_return = transactions[mask]

    return transactions_return.to_json(orient='records', force_ascii=False)
