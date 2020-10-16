import pandas as pd
import openpyxl as xl
import datetime as dt
import matplotlib.pyplot as plt
from series_hacienda import line_plot, plot_comparative_bars

data = pd.ExcelFile('demo bbg.xlsx')
data.sheet_names

# Bloomberg Tickers
bbg_tickers = {'exportaciones': 'ARBABEXP Index', 'importaciones': 'ARBABIMP Index', 'saldo_comercial':'ARBABAL Index',
               'saldo_cc':'ARBPCURR Index', 'saldo_cf':'ARBGFINA Index', 'saldo_ca':'ARBGCAPI Index', ''}

# Store multiple sheets in a dictionary
sheets_dict = {}
for sheet in data.sheet_names:
    dataframe = pd.read_excel(data, sheet, index_col=0, parse_dates=True)
    sheets_dict[sheet] = dataframe
sheets_dict.keys()

# Test line plots
cols_money = df_money_base.columns.values
base_total = df_money_base.loc['2019':'2020',cols_money[2]].reset_index().dropna().set_index('index')
line_plot(base_total)

# Sample Bar Plot
def bar_plot(df, title, datos_de_panel=True):
    """
    Returns sample bar plot. Pass a dataframe with dates in the index
    """
    if datos_de_panel == True:
        # Set date
        year, month, day = df.index.year.values[0], df.index.month.values[0], df.index.day.values[0]
        date = dt.datetime(year,month,day)
        date = date.strftime('%d-%m-%Y')
        # Set y values
        try:
            # Flatten if numpy array
            y_vals = df.values.flatten('F')
        except:
            # Extract values
            y_vals = df.values
        # Set x values
        x_vals = range(len(y_vals))
        #
        labels = [x for x in df.columns.values]
        # Create figure
        fig,ax = plt.subplots(figsize=(12,8))
        plt.bar(x_vals, y_vals, edgecolor='red', label=date, color='steelblue')
        ax.set_xticks(x_vals)
        ax.set_xticklabels(labels, fontsize='13', rotation=90)
        plt.legend(loc='best', fontsize='13')
        plt.title(title, fontsize='13')
        plt.show()
    else:
        pass


""" Trade balance """
trade_balance = sheets_dict['trade balance']
trade_balance_cols = trade_balance.columns.values
# Filter last 3 years
expos = trade_balance.loc['2018':'2020',trade_balance_cols[0]].reset_index().set_index('index')
expos.rename(columns={expos.columns.values[0]:'Exportaciones'},inplace=True)
impos = trade_balance.loc['2018':'2020',trade_balance_cols[1]].reset_index().set_index('index')
impos.rename(columns={trade_balance_cols[1]:'Importaciones'},inplace=True)
saldo_comercial = trade_balance.loc['2018':'2020',trade_balance_cols[2]].reset_index().set_index('index')
saldo_comercial.rename(columns={trade_balance_cols[0]:'Saldo Balanza Comercial'},inplace=True)
# Plot comparatives
plot_comparative_bars(expos)
plot_comparative_bars(impos)
plot_comparative_bars(saldo_comercial)

""" Public Accounts """
public_accounts = sheets_dict['public accounts']
public_accounts.rename(columns={public_accounts.columns.values[0]:'Saldo Cuenta Corriente',
                                public_accounts.columns.values[1]:'Saldo Cuenta Financiera',
                                public_accounts.columns.values[2]:'Saldo Cuenta Capital',
                                public_accounts.columns.values[3]:'Saldo Error'},inplace=True)
public_accounts.dropna(how='all', subset = public_accounts.columns.values[1:-2], inplace=True)
# Filter last 3 years
saldo_cc = public_accounts.loc["2018":'2020','Saldo Cuenta Corriente'].reset_index().set_index('index')
saldo_ca = public_accounts.loc["2018":'2020','Saldo Cuenta Capital'].reset_index().set_index('index')
saldo_cf = public_accounts.loc["2018":'2020','Saldo Cuenta Financiera'].reset_index().set_index('index')
# Plot trend line
line_plot(saldo_cc)
line_plot(saldo_ca)
line_plot(saldo_cf)

""" GDP  """
gdp_sector = sheets_dict['gdp_sector']
gdp_labels = ['Agro y Ganando', 'Pesca', 'Mineria', 'Manufactura', 'Energía, Gas y Agua', 'Construcción', 'Ventas Retail y Mayoristas',
              'Hoteles y Restaurantes', 'Transporte y Descarga', 'Intermediación Financiera', 'Real Estate', 'Admin. Pública',
              'Educación', 'Salud', 'Otros', "Servicio Doméstico"]

for i in range(len(gdp_sector.columns.values)):
    gdp_sector.rename(columns={gdp_sector.columns.values[i]:gdp_labels[i]},inplace=True)

last_values = gdp_sector.loc['2020-06']
test_values = gdp_sector.loc['2019-06']
int_fin = gdp_sector.loc['2019':'2020','Intermediación Financiera'].reset_index().set_index('index')
# Plot bars
bar_plot(test_values, 'PBI por sector', datos_de_panel=True)
bar_plot(last_values, 'PBI por sector', datos_de_panel=True)
bar_plot(int_fin, 'PBI por sector', datos_de_panel=False)
