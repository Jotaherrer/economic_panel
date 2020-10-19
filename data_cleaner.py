# Imports
import os, pandas as pd
import xlwings as xw
import numpy as np

# Define Functions
def clean_df(dataframe):
    """
    Filter dataframes extracted from BBG.
    """
    len_cols, cols = len(dataframe.columns), dataframe.columns
    selection = [cols[i] for i in range(len_cols) if ~i % 2]
    dataframe_mod = dataframe.loc[:, [x for x in selection]]
    return dataframe_mod


def excel_prueba(df, df_origin):
    """
    Export BBG modified data to Excel. Params:
    - df: dictionary with modified data from BBG.
    - df_origin: original excel file with data from BBG.
    """
    for k,v in info.items():
        sheet = df_origin.sheet_names[k]
        if os.path.exists('prueba.xlsx'):
            wb = xw.Book('prueba.xlsx')
            ws = wb.sheets(sheet)
            ws.range('A1').expand().value = df[k]
            print('Carga exitosa de datos sheet', sheet, '!')
    else:
        print('Job Finished!')


if __name__ == '__main__':
        # Data import
        data = pd.ExcelFile('./demo bbg2.xlsx')
        #data.sheet_names

        # Tickers identification
        bbg_tickers = {'anual': {'ARGQPYYX INDEX':'pbi_anual'},
                    'cuatrimestral': {'ARBPCURR Index': 'cuenta_corriente',
                                        'ARB6FINA Index': 'cuenta_financiera',
                                        'ARB6CAPI Index': 'cuenta_capital',
                                        'ARB6ERRO Index': 'cuenta_error',
                                        'ARPDTOTL Index': 'deuda_total_gobierno',
                                        'ARGQPYOX Index': 'pbi_consolidad_yoy',
                                        'ARSQPRIY Index': 'pbi_consumo_privado_yoy',
                                        'ARSQPUYY Index': 'pbi_gasto_gobierno_yoy',
                                        'ARSQFIVY Index': 'pbi_construccion_yoy',
                                        'ARGQGYOX Index': 'pbi_agro_yoy',
                                        'ARGQIYOX Index': 'pbi_pesca_yoy',
                                        'ARGQYNOX Index': 'pbi_mineria_yoy',
                                        'ARGQMYOX Index': 'pbi_manufactura_yoy',
                                        'ARGQUYOX Index': 'pbi_electricidad_yoy',
                                        'ARGQCYOX Index': 'pbi_construccion_yoy',
                                        'ARGQRYOX INDEX': 'pbi_wholesale_retail_yoy',
                                        'ARGQHYOX Index': 'pbi_hoteles_yoy',
                                        'ARGQTYOX Index': 'pbi_transporte_yoy',
                                        'ARGQFYOX Index': 'pbi_interm_fin_yoy',
                                        'ARGQBYOX Index': 'pbi_real_estate_yoy',
                                        'ARGQDYOX Index': 'pbi_admin_publica_yoy',
                                        'ARGQEYOX Index': 'pbi_educacion_yoy',
                                        'ARGQGOOY Index': 'pbi_salud_yoy',
                                        'ARGQOTHY Index': 'pbi_otros_yoy',
                                        'ARGQDOMY Index': 'pbi_pers_domes_yoy',
                                        'ARUERATE Index': 'desempleo',
                                        'ARUEEMPL Index': 'empleo'},
                    'mensual': {'ARBABEXP Index': 'export_mensual',
                                'ARBABIMP Index': 'import_mensual',
                                'ARBABAL Index': 'balance_comercial',
                                'ARBAEYOY Index': 'export_mensual_yoy',
                                'ARRMCURR Index': 'cc_1',
                                'ARNMCURR Index': 'cc_2',
                                'ARNMCPTL Index': 'cc_3',
                                'ARC6INCM Index': 'ipc_nacional',
                                'ARC6INDM Index': 'ipc_nucleo',
                                'ARIPNSYO Index': 'act_industrial_yoy',
                                'ARICGEN Index': 'capacidad_instalada',
                                'ARSCYOY Index': 'ventas_retail',
                                    'ARCCIND Index': 'confianza_consumidor',
                                    'ARTXTOTL Index': 'recaudacion',
                                    'ARFBFIRS Index': 'inversion_extr_dir',
                                    'ARVSARTL Index': 'patentamientos',
                                    'ARVHTOTL Index': 'produccion_autos'},
                    'diario': {'ARVAM1PY Index': 'm1_yoy',
                                'ARVAM2PY Index': 'm2_yoy',
                                'ARVAM3PY Index': 'm3_yoy',
                                'ARMBEXDP Index': 'monetary_circulation',
                                'ARMBCURR Index': 'current_account_deposits',
                                'BADLARPP INDEX': 'badlar',
                                'ARLLELIQ Index': 'leliq',
                                'ARDRPESO Index': 'duration_depositos_ars',
                                'ARDRT30U Index': 'duration_depositos_usd_30_dias',
                                'ARDRT90U Index': 'duration_depositos_usd_90_dias',
                                'ARRVIRFS Index': 'reservas_brutas'}}

        tickers_list = []
        for period, tickers in bbg_tickers.items():
            for ticker, values in tickers.items():
                tickers_list.append((ticker, values))

        # Data cleaning 1
        info = {}
        for i in range(len(data.sheet_names)):
            df = pd.read_excel(data, data.sheet_names[i], index_col=0, parse_dates=True)
            df = clean_df(df)
            info[i] = df

        # Data cleaning 2 + export to excel
        i = 0
        n = 1
        for d in info.values():
            # Replace tickers
            leng = len(d.columns)
            if i == 0:
                d.columns = [x[1] for x in tickers_list[i:leng]]
                print('ok vuelta', n)
            else:
                d.columns = [x[1] for x in tickers_list[i:i+leng]]
                print('ok vuelta', n)

            # Drop NaT date:
            if pd.isnull(d.index[0]) == True:
                d.drop(d.index[0], inplace=True)
                print('ok drop first row in file', n)
            else:
                print('primer linea no posee errores')

            i += leng
            n += 1

        # Export modified data to excel
        excel_prueba(info, data)