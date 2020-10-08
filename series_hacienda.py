"""
Script de descarga de datos sobre series de tiempo Ministerio de Hacienda. Link de descarga:
https://www.economia.gob.ar/datos/
"""
# Imports
import os, pandas as pd
import api_min_hac as mh
import matplotlib.pyplot as plt

# Funciones

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


def plot_time_series(pandas_dataframe):
    """
    Return simple line plot to visualize trends
    """
    data = pandas_dataframe

    fig, ax = plt.subplots(figsize=(14,10))

    plt.plot(data, color='salmon',linewidth=2)
    plt.title(data.columns.values)
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

    # Nuevo Dataset
    series_ok = series_hacienda.iloc[43:]
    series_ok = series_ok[series_ok['serie_actualizada'] == 'True']
    columns = series_hacienda.columns
    series_ok.info()
    series_ok.head()

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

    series_nuevo = series_ok.loc[:,['serie_id','serie_titulo', 'serie_unidades','serie_indice_inicio','serie_indice_final', 'consultas_total']]
    series_nuevo.sort_values('serie_indice_final', ascending=True)


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
