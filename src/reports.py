from datetime import datetime, timedelta
import pandas as pd
from typing import Optional


def report_file(file="..\\data\\reports.json"):
    """декоратор для записи результата функции в json файл"""
    def report(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            with open(file, "a", encoding="utf-8") as f:
                f.write(result)
            return result
        return wrapper
    return report


def spending_by_category(
        transactions: pd.DataFrame,
        category: str,
        date: Optional[str] = None
) -> str:
    """принимает на вход dataframe с транзакциями, возвращает его в виде json, отфильтрованным по категории"""
    df = transactions.copy()

    df = df[df['Категория'].str.lower() == category.lower()].copy()

    if date is None:
        end_date = datetime.now()
    else:
        end_date = datetime.strptime(date, "%d.%m.%Y")

    start_date = end_date - timedelta(days=92)

    df.loc[:, 'Дата операции'] = pd.to_datetime(
        df['Дата операции'],
        format='%d.%m.%Y %H:%M:%S',
        dayfirst=True
    )

    filtered_df = df[
        (df['Дата операции'] >= start_date) &
        (df['Дата операции'] <= end_date)
        ].copy()

    return filtered_df.to_json()
