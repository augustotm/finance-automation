import pandas as pd
from openpyxl.utils.cell import range_boundaries

#######################
### Extract tables from sheet
#######################

# https://www.reddit.com/r/learnpython/comments/pwjqok/load_excel_named_table_into_dataframe/
def extract_tables(ws):
    dfs_tmp = {}

    for name, table_range in ws.tables.items():
        # Get position of data table
        min_col, min_row, max_col, max_row = range_boundaries(table_range)

        # Convert tablet to DataFrame
        table = ws.iter_rows(min_row, max_row, min_col, max_col, values_only=True)
        header = next(table)
        df = pd.DataFrame(table, columns=header)

        dfs_tmp[name] = df

    return dfs_tmp

#######################
### Extract tables from sheet
#######################

def get_table_excel(workbook, sheet_name, table_name):

    sheet_index = [i for i,sheet in enumerate(workbook.worksheets) if sheet.title == sheet_name][0]

    df = extract_tables(workbook.worksheets[sheet_index])[table_name]

    return df