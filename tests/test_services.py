import pandas as pd
import json
from src.services import search_by_word


def test_search_by_word():
    # Создаем тестовые данные
    test_data = pd.DataFrame({
        'Описание': ['Покупка в Apple', 'Оплата Amazon', 'Кино'],
        'Категория': ['Техника', 'Магазин', 'Развлечения'],
        'Сумма': [100, 200, 50]
    })

    # Тест поиска по описанию
    result = search_by_word(test_data, "apple")
    data = json.loads(result)
    assert len(data) == 1
    assert data[0]['Описание'] == 'Покупка в Apple'

    # Тест поиска по категории
    result = search_by_word(test_data, "магазин")
    data = json.loads(result)
    assert len(data) == 1
    assert data[0]['Категория'] == 'Магазин'