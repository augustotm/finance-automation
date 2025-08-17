from dotenv import load_dotenv
import os
from pathlib import Path
from selenium import webdriver
from time import sleep
import pandas as pd
import time
import logging
from engine import convert_default, convert_percentage, fundamentus_additional_data

def etl_statusinvest_acao():

    ###
    ### Start Logging
    ###
    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_path = os.path.join(script_dir, 'app_status.log')
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_path, mode='w'),  # Sobrescreve o arquivo
            logging.StreamHandler()
        ]
    )

    logging.info("##############################################################")
    logging.info("### Starting Acao (Status Invest + Fundamentus) processing ###")
    logging.info("##############################################################")

    ###
    ### Get environment variables
    ###
    logging.info("### Loading environment variables")
    ### .env file in the same folder as .py
    env_path = Path(__file__).parent / ".env.fundstatus"
    load_dotenv(dotenv_path=env_path, override=True)

    download_path = os.getenv("DOWNLOAD_PATH")
    destination_path = os.getenv("DESTINATION_PATH")
    statusinvest_url = os.getenv("STATUSINVEST_URL")
    output_file_name = os.getenv("ACAO_STATUSINVEST_SHEET_NAME")

    download_csv = "statusinvest-busca-avancada.csv"

    ###
    ### Open URL in Chrome and wait 1.5 seconds
    ###
    driver = webdriver.Chrome()
    driver.get(statusinvest_url)
    sleep(1.5)

    ###
    ### Find Buscar button, click and wait 1 seconds
    ###
    button_buscar = driver.find_element("xpath",
                                        '//div/button[contains(@class, "find")]')
    button_buscar.click()
    sleep(1)

    ###
    ### Find Download button, click and wait 2 seconds
    ###
    button_download = driver.find_element("xpath", 
                                        '//div/a[contains(@class, "btn-download")]')
    button_download.click()
    sleep(2)

    ###
    ### Delete treated file if it exists
    ###
    if os.path.exists(destination_path + "statusinvest_acao_treated.xlsx"):
        os.remove(destination_path + "statusinvest_acao_treated.xlsx")

    ###
    ### Move downloaded csv file to destination path
    ###
    downloaded_file = download_path + download_csv
    destination_csv_file = destination_path + download_csv

    if os.path.exists(destination_csv_file):
        ### Remove csv file from destination and move download file to destination
        os.remove(destination_csv_file)
        os.replace(downloaded_file, destination_csv_file)
    else:
        ### Only move file to destination
        os.replace(downloaded_file, destination_csv_file)


    ###
    ### Read csv file and define percentage columns
    ###
    logging.info("\n### Read csv")
    df = pd.read_csv(destination_csv_file, sep=';')
    n_col = df.shape[1]

    percentage = ["DY", "MARGEM BRUTA", "MARGEM EBIT",
                    "MARG. LIQUIDA","ROE", "ROA",
                    "ROIC", "CAGR RECEITAS 5 ANOS", "CAGR LUCROS 5 ANOS"]

    ###
    ### Treat columns from text to number/percentage
    ###
    logging.info("### Treat columns")
    for i in range(1, n_col):
        # print("@ Column name: {} | {}".format(i, df.columns[i]))
        if df.columns[i] in percentage:
            df.iloc[:, i] = convert_percentage(df.iloc[:, i])
        else:
            df.iloc[:, i] = convert_default(df.iloc[:, i])

    ###
    ### Add other informations using Fundamentus
    ###
    logging.info("### Complement with sector and subsector")
    df["SETOR"] = ""
    df["SUBSETOR"] = ""
    df["TICKER COMPLETO"] = ""
    df["TIPO TICKER"] = ""

    st = time.time()

    fundamentus_additional_data(df,
                                df.columns.get_loc("SETOR"),
                                df.columns.get_loc("SUBSETOR"),
                                df.columns.get_loc("TICKER COMPLETO"),
                                df.columns.get_loc("TIPO TICKER")
                                )

    et = time.time()
    logging.info("### Additional information finished")
    logging.info("### Execution time: {:.2f} seg / {:.2f} min".format(et - st, (et - st)/60))

    ###
    ### Save dataframe to xlsx
    ###
    logging.info("### Save xlsx file")
    df.to_excel(destination_path + output_file_name + ".xlsx", index=False)

    logging.info("### Remove csv file")
    if os.path.exists(destination_csv_file):
        os.remove(destination_csv_file)

    logging.info("###############################################################")
    logging.info("### Acao (Status Invest + Fundamentus) processing finished! ###")
    logging.info("###############################################################")