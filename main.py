from src.reports import spending_by_category
from src.services import search_by_word
from src.views import main
import pandas as pd
import datetime

date = datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")

spending_by_category(pd.read_excel(".\\data\\operations.xlsx", engine="openpyxl"), "")
search_by_word(pd.read_excel(".\\data\\operations.xlsx", engine="openpyxl"), "")
main(datetime)
