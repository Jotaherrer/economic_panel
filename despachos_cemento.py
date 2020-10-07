# Imports
import pandas as pd
from pandas.tseries.offsets import Day, MonthEnd
import datetime as dt
import plotly.express as px


# Create functions

def create_url(date):
    """
    Creates a URL to download concrete sales stocks.
    - date: Input date in string format YYYYMM. E.g. 202008, 202009, 202010
    """
    link = f'http://afcp.info/ESTADISTICAS/DESPACHO-MENSUAL/P{date}/P{date}.html'
    return link


def read_webpage(link):
    """
    Imports concret sales from AFCP returning 2 dataframes,  monthly sales
    """
    data = pd.read_html(link)
    data2 = data[0].dropna(how='all').loc[:,:6].reset_index(drop='index')


    data_tables = data2.loc[:17, :].reset_index(drop='index')
    data_anual = data2.loc[18:35,:].reset_index(drop='index')
    return data_tables, data_anual


def prepare_data(tables):
    """
    Data-cleaning process that returs data, months and years.
    """
    # Split information
    monthly_sales, annual_sales = tables[0],tables[1]

    # Format data
    months = annual_sales[0][2:14].values
    years = annual_sales.loc[1,1:].values

    # Rename cols and create pandas dataframe
    sales_data = annual_sales.iloc[2:14,1:]
    sales_data.rename(columns={1:'2015',2:'2016',3:'2017',4:'2018',5:'2019',6:'2020'},inplace=True)
    sales = {}
    for y in sales_data.columns:
        sales[y] = pd.Series(sales_data[y]).map(lambda x: x.replace('.', ''))
    sales_df = pd.DataFrame(sales)

    # Replace symbols in cols
    for i in range(len(sales_df['2020'].values)):
        if sales_df['2020'].values[i][:3] == '(1)':
            sales_df['2020'].values[i] = sales_df['2020'].values[i].replace('(1) ','')

        elif sales_df['2020'].values[i][:3] == '(2)':
            sales_df['2020'].values[i] = sales_df['2020'].values[i].replace('(2) ','')

        elif sales_df['2020'].values[i] == '-':
            sales_df['2020'].values[i] = 0

    # Convert str to floats
    for col in sales_df.columns:
        sales_df[col] = sales_df[col].values.astype(float)

    # Add total columsn
    sales_df['monthly_avg'] = round(sales_df.iloc[:,:].sum(axis=1) / len(years),2)

    return sales_df, months, years


if __name__ == '__main__':

    # Set up date
    today = dt.datetime.today()
    today_prev = today - Day(30)
    today_str = today.strftime('%Y%m')
    today_str_prev = today_prev.strftime('%Y%m')

    # Prepare data
    url = create_url(today_str_prev)
    html = read_webpage(url)
    data = prepare_data(html)

    # Plot 2020
    fig = px.bar(data[0], x=data[1], y='2020', color = '2020',
                 labels={'2020':'Mill. Ton.','x':'2020'}, height=500)
    fig.show()

    # Plot side-by-side bar chart