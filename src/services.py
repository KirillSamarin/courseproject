import pandas as pd
import json


def search_by_word(transactions: pd.DataFrame, search: str) -> json:
    search = search.lower()

    mask = (
            transactions['Описание'].str.lower().str.contains(search) |
            (transactions['Категория'].str.lower().str.contains(search)
             ))

    transactions_return = transactions[mask]

    return transactions_return.to_json(orient='records', force_ascii=False)
