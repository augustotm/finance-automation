# :gear: Finance Automations

This repository contains python automations to obtain financial data (Stocks, REITs, ETFs, etc.)

### [:open_file_folder: 01-fundamentus-statusinvest-automation](./01-fundamentus-statusinvest-automation)

This project gets brazilian stock data from [Status Invest](https://statusinvest.com.br/) and FII data from [Fundamentus](https://www.fundamentus.com.br/). It generates as output `xlsx` files.

You need to create a `.env.fundstatus` file to define environment variables.

1. Create a `.env.fundstatus` file to add variables in the project folder ([01-fundamentus-statusinvest-automation](./01-fundamentus-statusinvest-automation)).

2. Create the following variables.

```ini
DOWNLOAD_PATH=C:/Users/username/Downloads/
DESTINATION_PATH=C:/Users/username/folder_to_send_file
FUNDAMENTUS_URL=https://www.fundamentus.com.br/fii_resultado.php
STATUSINVEST_URL=https://statusinvest.com.br/acoes/busca-avancada
FII_FUNDAMENTUS_SHEET_NAME=file_name
ACAO_STATUSINVEST_SHEET_NAME=file_name
```
