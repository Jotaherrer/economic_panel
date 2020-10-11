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
        unidades = dataframe['serie_unidades'].values[level]
        db_data = mh.get_data([data],limit=5000).reset_index()
        db_data = db_data.set_index('index')
        col_name = db_data.columns.values[0]
        db_data.rename(columns={col_name:str(col_name+' - Unidad:'+unidades)},inplace=True)
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
    Returns a comparative bar chart with an output of desired years. Computes up to 5 years.
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
    color_bars, bar_width = 0.1, 0.8
    colors = ['steelblue', 'green','peru','salmon','yellow']
    color_lines = ['blue','yellowgreen','orange','red','yellow']
    #color_lines = [(0,0.2,0.3,1),(0,0.2,0.3,0.8),(0,0.2,0.3,0.6),(0.,0.2,0.3,0.4),(0,0.2,0.3,0.2)] # Gradient of reds
    labels_range = np.arange(int(x_values[0][0])+2,int(x_values[-1][-1])+2,len(years))

    # Plot bars in for loop
    for i in range(len(years)):
        rgba_color = color_bars + i * 0.2
        rgba_color = (0.2,rgba_color+0.1,rgba_color,1)

        plt.bar(x_values[i], y_values[i], width=bar_width, color=colors[i], label=years.values[i], edgecolor='purple')
        plt.plot(x_values[i], y_values[i], color=color_lines[i],marker='s',markersize='10',linewidth='3', label=years.values[i])

    # Setting "x" ticks
    ax.set_xticks(labels_range)
    ax.set_xticklabels(months, fontsize='13')
    for tick in ax.get_xticklabels():
        tick.set_rotation(40)
    # Setting "y" ticks
    numbers = []
    for e in y_values:
        for n in e:
            numbers.append(n)
    non_zeros = [x for x in numbers if x != 0]
    min, max = (0.90 * np.min(non_zeros)), (1.1 * np.max(non_zeros))
    y_ticks = np.linspace(round(min,0),round(max,0),10)
    ax.set_yticks(y_ticks)

    # Setting labels and preview
    plt.title(f'Comparativa de valores correspondientes a los últimos {len(years)} años de {pandas_df.columns.values[0]}',fontsize=15)
    plt.subplots_adjust(bottom= 0.2, top = 0.98)
    plt.xlabel('Mes')
    plt.ylim((min,max))
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

    # Filtro de series mas vistas y plotteo
    most_viewed_titles = get_most_viewed_series(10, series_ok)
    most_viewed_ids = get_most_viewed_ids(10, series_ok)

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
    b = get_information(cemento,0).loc['2017':'2020',:]
    c = get_information(supers,0).loc['2016':'2020',:]

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

    # Testing Bar Plots
    plot_comparative_bars(c)
    plot_comparative_bars(a)
    plot_comparative_bars(b)

    # Testing RGBA colors
    plt.bar([1,2,3,4], [1,2,3,4], color=(1,0.7,0.7,0.5))
    plt.bar([5,6,7,8], [1,2,3,4], color=(0,0.2,0.2,0.5))
    plt.bar([9,10,11,12], [1,2,3,4], color=(1,0.2,0.2,0.5))
    plt.bar([13,14,15,16], [1,2,3,4], color=(0,0.7,0.7,0.5))
    plt.show()

    plt.bar([1,2,3,4], [1,2,3,4], color=(1,0.1,0.5,0.5))
    plt.bar([5,6,7,8], [1,2,3,4], color=(1,0.3,0.5,0.5))
    plt.bar([9,10,11,12], [1,2,3,4], color=(1,0.5,0.5,0.5))
    plt.bar([13,14,15,16], [1,2,3,4], color=(1,0.7,0.5,0.5))
    plt.show()

    plt.bar([1,2,3,4], [1,2,3,4],     color=(0,0.1,0.3,1))
    plt.bar([5,6,7,8], [1,2,3,4],     color=(0,0.3,0.5,1))
    plt.bar([9,10,11,12], [1,2,3,4],  color=(0,0.5,0.7,1))
    plt.bar([13,14,15,16], [1,2,3,4], color=(0,0.7,0.9,1))
    plt.show()

    # Creating plot formulas
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




