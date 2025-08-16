import pandas as pd
import requests
from bs4 import BeautifulSoup
import logging

##############################
### Conversion function
##############################

#####
### Convert text to number
#####

def convert_default(column):

    logging.info('# Starting conversion of "{}" from text to number'.format(column.name))
    ### Remove thousand separator
    column = column.str.replace('.', '')
    # column = column.replace('.', '', regex=False)

    ### Substitute comma by dot for decimal separator
    column = column.str.replace(',', '.')
    
    ### Convet to numer
    column = pd.to_numeric(column)

    logging.info('# Number conversion finished')
    return column

#####
### Convert text to percentage
#####

def convert_percentage(column):

    logging.info('# Starting conversion of "{}" from text to percentage'.format(column.name))
    ### Remove thousand separator
    column = column.str.replace('.', '')

    ### Substitute comma by dot for decimal separator
    column = column.str.replace(',', '.')
    
    ### Remove % symbol and divide number by 100
    column = column.str.replace('%', '')
    column = pd.to_numeric(column)
    column = column/100

    logging.info('# Percentage conversion finished')
    return column

##############################
### Fundamentus Functions
##############################

#####
### Funtion to get net equity data and add to dataframe column
#####

def fundamentus_fii_net_equity(df, column_number):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    ### Get number of rows
    nb_rows = df.shape[0]
    
    for i in range(nb_rows):

        ticker = df.iloc[i,0]
        
        ### Access ticker page
        url_detailed = "https://www.fundamentus.com.br/detalhes.php?papel=" + ticker
        
        response = requests.get(url_detailed, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        tables = soup.findAll("table")
        rows = tables[2].find_all('tr')

        columns = rows[11].find_all('td')
        cell = columns[5].get_text().strip()

        logging.info("{}/{}: {} / {}".format(i+1,nb_rows+1,ticker, cell))
        
        df.iloc[i,column_number] = cell

#####
### Funtion to get addititonal data and add to dataframe column
#####

def fundamentus_additional_data(df, sector_col, subsector_col, ticker_complet_col, ticker_type_col):

    ### Iterate ticker by ticker
    for i in range(df.shape[0]):

        ### Get data from ticker
        ticker = df.iloc[i,0]
        url_detailed = "https://www.fundamentus.com.br/detalhes.php?papel=" + ticker

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        response = requests.get(url_detailed, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        tables = soup.findAll("table")

        ### Get information from table
        if len(tables) != 0:
            rows = tables[0].find_all('tr')
            
            if len(rows) > 3:
                
                ### Get Sector
                columns = rows[3].find_all('td')
                setor = columns[1].get_text().strip()

                ### Get SubSector
                columns = rows[4].find_all('td')
                subsetor = columns[1].get_text().strip()

                ### Get complete ticker
                columns = rows[2].find_all('td')
                ticker_completo = columns[1].get_text().strip()

                ### Get ticker type
                columns = rows[1].find_all('td')
                tipo_ticker = columns[1].get_text().strip()

                logging.info("{} / {} / {} / {} / {}".format(ticker, setor, subsetor, ticker_completo, tipo_ticker))

                ### Write output in dataframe columns
                df.iloc[i,sector_col] = setor
                df.iloc[i,subsector_col] = subsetor
                df.iloc[i,ticker_complet_col] = ticker_completo
                df.iloc[i,ticker_type_col] = tipo_ticker