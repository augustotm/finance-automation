import pandas as pd
import requests
from bs4 import BeautifulSoup

##############################
### Conversion function
##############################

#####
### Convert text to number
#####

def convert_default(column):

    ### Remove thousand separator
    column = column.str.replace('.', '')
    # column = column.replace('.', '', regex=False)

    ### Substitute comma by dot for decimal separator
    column = column.str.replace(',', '.')
    
    ### Convet to numer
    column = pd.to_numeric(column)

    return column

#####
### Convert text to percentage
#####

def convert_percentage(column):

    ### Remove thousand separator
    column = column.str.replace('.', '')

    ### Substitute comma by dot for decimal separator
    column = column.str.replace(',', '.')
    
    ### Remove % symbol and divide number by 100
    column = column.str.replace('%', '')
    column = pd.to_numeric(column)
    column = column/100

    return column

##############################
### FII Functions
##############################

#####
### Convert text to percentage
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

        print("{} / {}".format(ticker, cell))
        
        df.iloc[i,column_number] = cell