from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from pathlib import Path
import logging
from engine import convert_default, convert_percentage, fundamentus_fii_net_equity

###
### Start Logging
###
script_dir = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(script_dir, 'app_fund.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_path, mode='w'),  # Sobrescreve o arquivo
        logging.StreamHandler()
    ]
)

###
### Get environment variables
###
logging.info('### Loading environment variables')
### .env file in the same folder as .py
env_path = Path(__file__).parent / ".env.fundstatus"
load_dotenv(dotenv_path=env_path, override=True)

download_path = os.getenv("DOWNLOAD_PATH")
destination_path = os.getenv("DESTINATION_PATH")
fundamentus_url = os.getenv("FUNDAMENTUS_URL")
output_file_name = os.getenv("FII_FUNDAMENTUS_SHEET_NAME")

###
### Connect to Fundamentus
###
logging.info('### Connecting to Fundamentus')
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

response = requests.get(fundamentus_url, headers=headers, timeout=30)
soup = BeautifulSoup(response.content, 'html.parser')

logging.info('### Get data from Fundamentus')

###
### Get table from Fundamentus
###
table = soup.find('table')
### Get rows from table
rows = table.find_all('tr')

###
### Define columns to get
###
dict_columns = {
    'papel'              : 'text',
    'segmento'           : 'text',
    'cotacao'            : 'number',
    'ffo_yield'          : 'percentage',
    'dividend_yield'     : 'percentage',
    'p_vp'               : 'number',
    'valor_de_mercado'   : 'number',
    'liquidez'           : 'number',
    'qtd_de_imoveis'     : 'number',
    'preco_m2'           : 'number',
    'aluguel_m2'         : 'number',
    'cap_rate'           : 'percentage',
    'vacancia_media'     : 'percentage',
    "endereco"           : 'text'
}

###
### Create empty dataframe to fill
###
logging.info('### Create empty dataframe')
df = pd.DataFrame(columns=list(dict_columns.keys()))

###
### Iterate data from each unformatted row
###
logging.info('### Fill dataframe by iterating row by row')
for i, row in enumerate(rows):
    
    ### Create a new empty row in dataframe to be filled
    if i != 0:
        df.loc[i-1] = [None] * len(df.columns)
    
    ### Get columns from row
    columns = row.find_all('td')
    
    ### Iterate column by column
    for j, column in enumerate(columns):
        # print("{}, {}".format(i-1,j))
        
        ### Get cell from column
        cell = column.get_text().strip()
        if cell != "":
            ### Fill dataframe cell with value
            df.iloc[i-1, j] = cell

###
### Convert numeric and percentage columns
###
logging.info('### Converting numeric and percentage columns')
for key, value in dict_columns.items():
    if value == 'number':
        df[key] = convert_default(df[key])
    if value == 'percentage':
        df[key] = convert_percentage(df[key])
logging.info('### Columns converted')

###
### Create new empty column to fill net equity data
###
df["patrimonio_liquido"] = ""

###
### Filter only not empty tickers
###
df = df[df['papel'].notna()]

st = time.time()

###
### Get net equity from Fundamentus
###
fundamentus_fii_net_equity(df, df.columns.get_loc("patrimonio_liquido"))

###
### Convert column to number
###
df["patrimonio_liquido"] = convert_default(df["patrimonio_liquido"])

et = time.time()

logging.info("### Execution time: {:.2f} seg / {:.2f} min".format(et - st, (et - st)/60))

###
### Save file to Excel
###
df.to_excel(destination_path + output_file_name + ".xlsx", index=False)

logging.info('### Excel created')