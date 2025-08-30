from dotenv import load_dotenv
from pathlib import Path
import os
from openpyxl import load_workbook
import logging
import yfinance as yf
import datetime

from engine import get_table_excel

def yahoo_assets_history():

    ###
    ### Start Logging
    ###
    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_path = os.path.join(script_dir, 'app_yahoo_assets_history.log')
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_path, mode='w'),  # Sobrescreve o arquivo
            logging.StreamHandler()
        ]
    )

    logging.info("####################################################")
    logging.info("### Starting Yahoo Finance Asset Data Processing ###")
    logging.info("####################################################")

    ###
    ### Load environment variables
    ###

    env_path = Path(__file__).parent / ".env.yahoo"
    load_dotenv(dotenv_path=env_path, override=True)

    file_name = os.getenv("FILE_NAME")
    file_path = os.getenv("FILE_PATH")
    sheet_name = os.getenv("SHEET_NAME")
    table_name = os.getenv("TABLE_NAME")

    file = file_path + file_name + ".xlsx"

    workbook = load_workbook(file, data_only=True)

    df = get_table_excel(workbook, sheet_name, table_name)
    df = df.drop(df.columns[[0,2,4,5,8,9,10,12,13,14]], axis=1)
    df["ticker_yahoo"] = df.apply(
        lambda row:
        row["ticker"] + ".SA" if row["exchange"] == "B3"
        else row["ticker"],
        axis = 1
    )
    print(df)

    lista_tickers = df['ticker_yahoo'].tolist()
    print(lista_tickers)

    ticker_name = df.loc[18]['ticker_yahoo']
    logging.info("####################################################")
    start_date = datetime.datetime(2015, 1, 1)
    end_date =  datetime.date.today()

    ticker = yf.Ticker(ticker_name)

    ticker_history = ticker.history(
        start=start_date,
        end=end_date,
        interval="1mo",
        auto_adjust=True,
        actions=True
    )
    # ticker_history = yf.download(
    #     tickers=['BTC-USD'],
    #     #  group_by='ticker',
    #     start=start_date,
    #     end=end_date,
    #     interval="1mo",
    #     auto_adjust=True
    # )
    print(ticker_history)

if __name__ == "__main__":
    yahoo_assets_history()