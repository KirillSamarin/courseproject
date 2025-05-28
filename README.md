# Финансовый аналитик

Проект предоставляет инструменты для анализа финансовых операций, включая отчеты по категориям, поиск транзакций и визуализацию данных.

## Функционал

### Основные модули:

1. **reports.py** - генерация отчетов:
   - `spending_by_category()` - анализ расходов по категориям за указанный период
   - Декоратор `report_file()` для сохранения отчетов в JSON

2. **services.py** - сервисные функции:
   - `search_by_word()` - поиск транзакций по ключевому слову в описании или категории

3. **views.py** - основной интерфейс:
   - `main()` - формирует сводную информацию:
     - Приветствие в зависимости от времени суток
     - Данные по картам (расходы и кэшбек за текущий месяц)
     - Топ-5 транзакций месяца
     - Курсы валют (USD, EUR)
     - Цены акций крупных компаний

## Установка

1. Склонируйте репозиторий:
   ```bash
   git clone https://github.com/KirillSamarin/courseproject.git

## Использование

1. Получение отчета по категориям:

from reports import spending_by_category
import pandas as pd

df = pd.read_excel("data/operations.xlsx")
report = spending_by_category(df, "супермаркеты", "01.01.2023")

2. Поиск транзакций:

from services import search_by_word
import pandas as pd

df = pd.read_excel("data/operations.xlsx")
result = search_by_word(df, "кафе")

3. Запуск интерфейса:

from views import main

print(main())

Покрытие тестами составляет 81%(отчет в папке htmlcov)

