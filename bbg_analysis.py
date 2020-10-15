import pandas as pd
import openpyxl as xl
from series_hacienda import line_plot, plot_comparative_bars

data = pd.ExcelFile('demo bbg.xlsx')
data.sheet_names

# Bloomberg Tickers
bbg_tickers = {'exportaciones': 'ARBABEXP Index', 'importaciones': 'ARBABIMP Index',
               'saldo_comercial':'ARBABAL Index', }

# Example of storing a particular sheet in a df
df = pd.read_excel(data, data.sheet_names[0], index_col=0, parse_dates=True)

# Store multiple sheets in a dictionary
sheets_dict = {}
for sheet in data.sheet_names:
    dataframe = pd.read_excel(data, sheet, index_col=0, parse_dates=True)
    sheets_dict[sheet] = dataframe
sheets_dict.keys()

# Test bar plots
columns = df.columns.values
exportaciones = df.loc[:,columns[0]].reset_index().set_index('index')
importaciones = df.loc[:,columns[1]].reset_index().set_index('index')
trade_balance = df.loc[:,columns[2]].reset_index().set_index('index')

expos1 = exportaciones.loc['2018':'2020',:]
impos1 = importaciones.loc['2018':'2020',:]
trade1 = trade_balance.loc['2019':'2020',:]

plot_comparative_bars(expos1)
plot_comparative_bars(impos1)

# Test line plots
cols_money = df_money_base.columns.values
base_total = df_money_base.loc['2019':'2020',cols_money[2]].reset_index().dropna().set_index('index')
line_plot(base_total)

## Trade balance analysis
trade_balance = sheets_dict['trade balance']
trade_balance_cols = trade_balance.columns.values
# Filter last 3 years
expos = trade_balance.loc['2018':'2019',trade_balance_cols[0]].reset_index().set_index('index')
expos.rename(columns={expos.columns.values[0]:'Exportaciones'},inplace=True)
impos = trade_balance.loc['2018':'2019',trade_balance_cols[1]].reset_index().set_index('index')
impos.rename(columns={trade_balance_cols[1]:'Importaciones'},inplace=True)
saldo_comercial = trade_balance.loc['2018':'2019',trade_balance_cols[2]].reset_index().set_index('index').rename(columns={trade_balance_cols[0]:'Saldo Balanza Comercial'},inplace=True)
