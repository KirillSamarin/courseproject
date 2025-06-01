import pytest
import pandas as pd
from src.reports import spending_by_category


@pytest.fixture
def sample_transactions():
    return pd.DataFrame({
        'Дата операции': [
            '01.01.2023 12:00:00',
            '15.02.2023 18:30:00',
            '20.03.2023 09:15:00',
            '10.04.2023 14:45:00',
            '05.05.2023 11:20:00'
        ],
        'Категория': [
            'супермаркеты',
            'кафе',
            'супермаркеты',
            'аптека',
            'супермаркеты'
        ],
        'Сумма операции': [100, 200, 150, 300, 250]
    })


def test_spending_by_category_basic(sample_transactions):
    result_json = spending_by_category(sample_transactions, "супермаркеты", "01.04.2023")

    assert result_json is not None

    result_df = pd.read_json(result_json)
    assert not result_df.empty


def test_spending_by_category_date_filter(sample_transactions):
    result_json = spending_by_category(sample_transactions, "кафе", "15.04.2023")
    assert result_json is not None
    result_df = pd.read_json(result_json)
    assert len(result_df) == 1


def test_spending_by_category_no_date(sample_transactions):
    result_json = spending_by_category(sample_transactions, "кафе")
    assert result_json is not None
    result_df = pd.read_json(result_json)
    assert isinstance(result_df, pd.DataFrame)


def test_spending_by_category_empty_result(sample_transactions):
    result_json = spending_by_category(sample_transactions, "несуществующая категория", "01.04.2023")
    assert result_json is not None
    result_df = pd.read_json(result_json)
    assert result_df.empty
