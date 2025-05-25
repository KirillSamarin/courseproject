from unittest.mock import Mock, patch
from src.views import get_stock_price, currency_get, main


@patch('src.views.requests.get')
def test_get_stock_price(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {
        "Global Quote": {
            "05. price": "150.25"
        }
    }
    mock_get.return_value = mock_response

    result = get_stock_price("AAPL")

    assert result['stock'] == "AAPL"
    assert result['price'] == 150.25


@patch('src.views.requests.get')
def test_currency_get(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {
        "Valute": {
            "USD": {"Value": 90.5},
            "EUR": {"Value": 99.3}
        }
    }
    mock_get.return_value = mock_response

    result = currency_get()

    assert len(result) == 2
    assert result[0]['rate'] == 90.5
    assert result[1]['rate'] == 99.3


@patch('src.views.cards_information')
@patch('src.views.top_five_transactions')
@patch('src.views.currency_get')
@patch('src.views.get_stock_price')
@patch('src.views.datetime.datetime')
def test_main_greeting(mock_datetime, mock_stock, mock_currency, mock_top, mock_cards):
    mock_time = Mock()
    mock_time.hour = 10
    mock_datetime.now.return_value.time.return_value = mock_time

    mock_cards.return_value = [{"card": "1234", "total_spent": 1000}]
    mock_top.return_value = [{"transaction": "test"}]
    mock_currency.return_value = [{"currency": "USD", "rate": 90.0}]
    mock_stock.return_value = {"stock": "AAPL", "price": 150.0}

    result = main()

    assert result['greeting'] == "Доброе утро!"
    assert len(result['cards']) == 1
    assert len(result['top_transactions']) == 1
    assert len(result['currency_rates']) == 1
    assert "stock_prices" in result

    mock_time.hour = 20
    result = main()
    assert result['greeting'] == "Добрый вечер!"
