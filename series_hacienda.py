"""
Script de descarga de datos sobre series de tiempo Ministerio de Hacienda. Link de descarga:
https://www.economia.gob.ar/datos/
"""
# Imports
import os, pandas as pd
import api_min_hac as mh
import matplotlib.pyplot as plt
import numpy as np

# Funciones

def get_information(dataframe, level):
    """
    Returns a dataframe with information from the database. Params:
    - dataframe: input a pandas dataframe that contains a column named 'serie_titulo',
    that corresponds to the government's database format.
    - level: index number to identify a series.
    """
    try:
        data = dataframe['serie_id'].values[level]
        db_data = mh.get_data([data],limit=5000).reset_index()
        db_data = db_data.set_index('index')
    except:
        db_data = 'Input an dataframe with the appropiate format'
    return db_data


def get_most_viewed_series(amount, dataset):
    """
    Returns most consulted series in the database
    """
    return dataset.sort_values('consultas_total', ascending=False)[:amount]['serie_titulo'].values


def get_most_viewed_ids(amount, dataset):
    """
    Returns most consulted series in the database
    """
    return dataset.sort_values('consultas_total', ascending=False)[:amount]['serie_id'].values



def plot_comparative_bars(pandas_df):
    """
    Return simple bar plot to compare desired years
    """
    # Distribute data by years
    years = pandas_df.groupby(pandas_df.index.year).count().index
    months = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio',
              'Agosto','Septiembre','Octubre','Noviembre','Diciembre']
    data_dict = {}
    for y in years:
        data_dict[y] = pandas_df.loc[str(y)]

    # Create X and Y values for bar plots
    x_values = []
    y_values = []
    for i in range(1, len(data_dict.keys())+1):
        x_values_sample = [len(years) * element + 0.8*i for element in range(12)]
        x_values.append(x_values_sample)

    for y in data_dict.keys():
        y_values_sample = data_dict[y].values
        y_values_sample = y_values_sample.flatten('F')
        if y == 2020:
            length = len(y_values_sample)
            missings = 12 - length
            y_values_sample = np.pad(y_values_sample,(0,missings),'constant')
        y_values.append(y_values_sample)


    # Create Figure
    fig, ax = plt.subplots(figsize=(16,10))
    color_bars = ['green','salmon','peru','steelblue','lime']
    color_lines = ['yellowgreen','red','orange','blue','purple']
    labels_range = np.arange(int(x_values[0][0])+2,int(x_values[-1][-1])+2,len(years))

    for i in range(len(years)):
        plt.bar(x_values[i], y_values[i], label=years.values[i],color=color_bars[i],edgecolor=color_lines[i])
        plt.plot(x_values[i], y_values[i], color=color_lines[i],marker='*',linewidth='3')

    ax.set_xticks(labels_range)
    ax.set_xticklabels(months, fontsize='13')
    for tick in ax.get_xticklabels():
        tick.set_rotation(40)

    plt.title(f'Comparativa valores últimos {len(years)} años de {pandas_df.columns.values[0]}',fontsize=15)
    plt.legend(loc='best')
    plt.show()


if __name__ == '__main__':
    # Download info from stata database
    series_hacienda = pd.read_stata('./series-tiempo-metadatos.dta')

    # Testing de funcionalidad de series con API
    i = 0
    for ident in series_hacienda:
        try:
            data = mh.get_data([ident], start_date='2015-01')
            print('Serie OK numero',i)
            i += 1
        except:
            print('Serie no encontrada numero',i)
            i += 1

    # Nuevo Dataset con filtro de serie actualizada
    series_ok = series_hacienda.iloc[43:]
    series_ok = series_ok[series_ok['serie_actualizada'] == 'True']
    columns = series_hacienda.columns
    series_ok.info()
    series_ok.head()

    # URLs de descarga de control con archivo .CSV
    urls = series_ok.loc[:,'distribucion_url_descarga'].values
    urls_ids_control = series_ok.loc[:,'serie_id'].values
    f = open('urls_csv.txt','a')
    i = 0
    for u in urls:
        i += 1
        f.write(f"URL número {i}: {u}\n")
    f.close()

    # Features por columna
    series_ok.iloc[0]
    series_ok.catalogo_id.unique()
    series_ok.dataset_id.unique()
    series_ok.distribucion_id.unique()
    series_ok.indice_tiempo_frecuencia.unique()
    series_ok.serie_unidades.unique()
    series_ok.distribucion_url_descarga.unique()

    # Explore dataset
    series_id = series_ok['serie_id']
    series_titulos = series_ok['serie_titulo']
    test = mh.get_data(['92.1_RID_0_0_32'], start_date='2015-01')

    series_ok.sort_values('serie_indice_final', ascending=True)
    series_ok.describe()

    # Filtro de series mas vistas y plotteo
    most_viewed_titles = get_most_viewed_series(10, series_ok)
    most_viewed_ids = get_most_viewed_ids(10, series_ok)

    info = pd.DataFrame(mh.get_data([most_viewed_ids[0]],start_date=2015, limit=3000))
    info2 = pd.DataFrame(mh.get_data([most_viewed_ids[1]],start_date=2015, limit=3000))

    info_dic = {}

    for code in most_viewed_ids:
        info = pd.DataFrame(mh.get_data([code],start_date=2015, limit=3000))
        info_dic[info.columns.values[0]] = info

    info_dic.keys()
    info_dic

    plot_time_series(info_dic[most_viewed_titles[0]])

    for i in range(len(most_viewed_titles)):
        plot_time_series(info_dic[most_viewed_titles[i]])


    # Create new df for selected columns
    series_nuevo = series_ok.loc[:,['serie_id','serie_titulo', 'serie_unidades','serie_descripcion','serie_indice_inicio','serie_indice_final', 'consultas_total']]


    # Filtro por conceptos especificos
    ipc = series_nuevo[series_nuevo['serie_titulo'].str.contains('ipc')].sort_values('consultas_total',ascending=False)
    emae = series_nuevo[series_nuevo['serie_titulo'].str.contains('emae')].sort_values('consultas_total',ascending=False)
    industria = series_nuevo[series_nuevo['serie_titulo'].str.contains('industria')].sort_values('consultas_total',ascending=False)
    cemento = series_nuevo[series_nuevo['serie_titulo'].str.contains('cemento')].sort_values('consultas_total',ascending=False)
    construccion = series_nuevo[series_nuevo['serie_titulo'].str.contains('construccion')].sort_values('consultas_total',ascending=False)
    bienes_cap = series_nuevo[series_nuevo['serie_titulo'].str.contains('capital')].sort_values('consultas_total',ascending=False)
    supers = series_nuevo[series_nuevo['serie_descripcion'].str.contains('supermercados')].sort_values('consultas_total',ascending=False)
    patentamientos = series_nuevo[series_nuevo['serie_titulo'].str.contains('automotores')].sort_values('consultas_total',ascending=False)
    salario = series_nuevo[series_nuevo['serie_titulo'].str.contains('salario')].sort_values('consultas_total',ascending=False)
    empleo =  series_nuevo[series_nuevo['serie_descripcion'].str.contains('empleo')].sort_values('consultas_total',ascending=False)
    depositos = series_nuevo[series_nuevo['serie_descripcion'].str.contains('sector privado')].sort_values('consultas_total',ascending=False)
    base_monetaria = series_nuevo[series_nuevo['serie_titulo'].str.contains('base_monetaria')].sort_values('consultas_total',ascending=False)
    educacion = series_nuevo[series_nuevo['serie_titulo'].str.contains('educacion')].sort_values('consultas_total',ascending=False)
    turismo = series_nuevo[series_nuevo['serie_titulo'].str.contains('turismo')].sort_values('consultas_total',ascending=False)
    reservas = series_nuevo[series_nuevo['serie_titulo'].str.contains('reservas')].sort_values('consultas_total',ascending=False)
    recaudacion = series_nuevo[series_nuevo['serie_titulo'].str.contains('recaudacion')].sort_values('consultas_total',ascending=False)
    tcrm = series_nuevo[series_nuevo['serie_titulo'].str.contains('tipo_cambio_real_multilateral')].sort_values('consultas_total',ascending=False)
    tcr_paises = series_nuevo[series_nuevo['serie_titulo'].str.contains('tipo_cambio_real_canada')].sort_values('consultas_total',ascending=False)
    expos = series_nuevo[series_nuevo['serie_titulo'].str.contains('exportaciones')].sort_values('consultas_total',ascending=False)
    impos = series_nuevo[series_nuevo['serie_titulo'].str.contains('importaciones')].sort_values('consultas_total',ascending=False)
    def_prim = series_nuevo[series_nuevo['serie_titulo'].str.contains('resultado_primario')].sort_values('consultas_total',ascending=False)


    # Revision de una serie en particular
    get_information(recaudacion,0).loc['2015':'2020',:].plot()
    get_information(base_monetaria,0).loc['2015':'2020',:].plot()
    get_information(reservas,0).loc['2015':'2020',:].plot()
    get_information(tc,0).loc['2010':'2020',:].plot()
    get_information(expos,1).loc['2019':'2020',:].plot()
    get_information(impos,0).loc['2019':'2020',:].plot(kind='bar')
    get_information(def_prim,0).loc['2016':'2020',:].plot(kind='bar')


    # Testing plotting function
    a = get_information(def_prim,0)
    years = a.groupby(a.index.year).count().index
    b = get_information(cemento,0).loc['2016':'2020',:]
    years2 = b.groupby(b.index.year).count().index
    c = get_information(supers,0).loc['2016':'2020',:]
    years3 = c.groupby(c.index.year).count().index

    x = {}
    for y in years3:
        x[y] = c.loc[str(y)]

    x_vals = []
    for i in range(1, len(x.keys())+1):
        x_values_sample = [3 * element + 0.8*i for element in range(12)]
        x_vals.append(x_values_sample)

    y_vals = []
    for y in x.keys():
        y_values_sample = x[y].values
        y_values_sample = y_values_sample.flatten('F')
        if y == 2020:
            length = len(y_values_sample)
            missings = 12 - length
            y_values_sample = np.pad(y_values_sample,(0,missings),'constant')
        y_vals.append(y_values_sample)


    def plot_time_series_bar(pandas_df):
        """
        Return simple bar plot to compare desired years
        """
        # Distribute data by years
        years = pandas_df.groupby(pandas_df.index.year).count().index
        months = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio',
                  'Agosto','Septiembre','Octubre','Noviembre','Diciembre']
        data_dict = {}
        for y in years:
            data_dict[y] = pandas_df.loc[str(y)]

        # Create X and Y values for bar plots
        x_values = []
        y_values = []
        for i in range(1, len(data_dict.keys())+1):
            x_values_sample = [len(years) * element + 0.8*i for element in range(12)]
            x_values.append(x_values_sample)

        for y in data_dict.keys():
            y_values_sample = data_dict[y].values
            y_values_sample = y_values_sample.flatten('F')
            if y == 2020:
                length = len(y_values_sample)
                missings = 12 - length
                y_values_sample = np.pad(y_values_sample,(0,missings),'constant')
            y_values.append(y_values_sample)


        # Create Figure
        fig, ax = plt.subplots(figsize=(16,10))
        color_bars = ['green','salmon','peru','steelblue','lime']
        color_lines = ['yellowgreen','red','orange','blue','purple']
        labels_range = np.arange(int(x_values[0][0])+2,int(x_values[-1][-1])+2,len(years))

        for i in range(len(years)):
            plt.bar(x_values[i], y_values[i], label=years.values[i],color=color_bars[i],edgecolor=color_lines[i])
            plt.plot(x_values[i], y_values[i], color=color_lines[i],marker='*',linewidth='3')

        ax.set_xticks(labels_range)
        ax.set_xticklabels(months, fontsize='13')
        for tick in ax.get_xticklabels():
            tick.set_rotation(40)

        plt.title(f'Comparativa valores últimos {len(years)} años de {pandas_df.columns.values[0]}',fontsize=15)
        plt.legend(loc='best')
        plt.show()




