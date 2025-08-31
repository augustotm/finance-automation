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

### [:open_file_folder: 02-yahoo-finance-python](./02-yahoo-finance-python)

This project use Yahoo Finance API and CoinGecko API to get trading data.

### [:open_file_folder: 03-compound-interest-calculator](./03-compound-interest-calculator)

This project has a compound interest calculator to get to obtain the performance of investments according to interest rate and inflation. The calculator also allows you to define the timeframe for analysis and the growth of your assets based on your age.

You need to create a `.env.tkinter` file to define environment variables.

1. Create a `.env.tkinter` file to add variables in the project folder ([03-compound-interest-calculator](./03-compound-interest-calculator)).

2. Create the following variables. These variables define the default values that the calculator will set.

```ini
INVEST_INICIAL=0
APORTE_MENSAL=1000
PLR_ANUAL=10000
BONUS_ANUAL=20000
INTEREST_ANUAL=0.09
INFLATION_ANUAL=0.045
LIST_TEMPO=Ano
QTD_TEMPO=10
GRANUL_TEMPO=Idade
NASC_DIA=01
NASC_MES=01
NASC_ANO=1999
```