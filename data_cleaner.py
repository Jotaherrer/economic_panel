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


def excel_prueba(df, df_origin, metricas_powerbi = False):
    """
    Export BBG modified data to Excel. Params:
    - df: dictionary with modified data from BBG.
    - df_origin: original excel file with data from BBG.
    """
    for k,v in info.items():
        sheet = df_origin.sheet_names[k]
        if (os.path.exists('datos_powerbi.xlsx')) & (metricas_powerbi == False):
            wb = xw.Book('datos_powerbi.xlsx')
            ws = wb.sheets(sheet)
            ws.range('A1').expand().value = df[k]
            print('Carga exitosa de datos sheet', sheet, 'en el archivo datos_powerbi','!')
        elif (os.path.exists('Panel Económico.xlsx')) & (metricas_powerbi == True):
            wb = xw.Book('Panel Económico.xlsx')
            ws = wb.sheets(sheet)
            ws.range('A1').expand().value = df[k]
            print('Carga exitosa de datos sheet', sheet, 'en el archivo datos_medidas', '!')
    else:
        print('Job Finished!')


if __name__ == '__main__':
        # Data import
        data = pd.ExcelFile('./demo bbg2.xlsx')
        #data.sheet_names

        # Tickers identification
        bbg_tickers = {'anual': {'ARGQPYYX INDEX':'pbi_anual'},
                    'cuatrimestral': {'ARBPCURR Index': 'bop_cuenta_corriente',
                                      'ARB6FINA Index': 'bop_cuenta_financiera',
                                      'ARB6CAPI Index': 'bop_cuenta_capital',
                                      'ARB6ERRO Index': 'bop_cuenta_error',
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
                                      'ARUEEMPL Index': 'empleo',
                                      'ARDSFIRE Index': 'resultado_fciero_menos_priva',
                                      'ARDSSUMM Index': 'resultado_primario',
                                      'ARDSREVE Index': 'ingresos_fiscal',
                                      'ARDSEXPD Index': 'gasto_primario'},
                    'mensual': {'ARBABEXP Index': 'export_mensual',
                                'ARBABIMP Index': 'import_mensual',
                                'ARBABAL Index': 'balance_comercial',
                                'ARRMCURR Index': 'cc_1',
                                'ARNMCURR Index': 'cc_2',
                                'ARNMCPTL Index': 'cc_3',
                                'ARNCNINX Index': 'ipc_nacional',
                                'ARCONACT Index': 'isac_general_estac',
                                'ARCOYOY Index': 'constr_mom_año_anterior',
                                'ARCONNAC Index': 'isac_general_no_estac',
                                'ARCOMOM Index': 'constr_mom',
                                'ARCOTRND Index': 'trend_constr',
                                'ARCOTRNM Index': 'trend_constr_mom',
                                'ARSCYOY Index': 'ventas_retail',
                                'ARTXTOTL Index': 'recaudacion',
                                'ARFBFIRS Index': 'inversion_extr_dir',
                                'ARVSARTL Index': 'patentamientos',
                                'ARVHTOTL Index': 'produccion_autos',
                                'ARDMSUMM Index': 'resultado_primario',
                                'ARDMFIRE IndeX': 'resultado_fciero_menos_priva',
                                'ARCMTOTL Index': 'despachos_cemento',
                                'AREMORMO Index': 'emae_mensual_yoy',
                                'AREMDEMO Index': 'emae_mensual_mom'},
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
                                'ARRVIRFS Index': 'reservas_brutas',
                                'CRB CMDT Index': 'crb_commodities',
                                'CRB RIND Index': 'crb_raw_industrials',
                                'SPGSCITR Index': 'daily_commodities2',
                                'SPGSAGTR Index': 'daily_agro',
                                'S 1 COMDTY': 'daily_soybean',
                                'SPX Index': 'daily_spx',
                                'DIA US Equity': 'daily_dji',
                                'VIX Index': 'daily_vix',
                                'XAU CURNCY': 'daily_gold',
                                'CL1 COMDTY': 'daily_oil',
                                'XLE US Equity': 'daily_energy',
                                'XLF US Equity': 'daily_financial',
                                'XLI US Equity': 'daily_industrial',
                                'XLK US Equity': 'daily_technology',
                                'XLV US Equity': 'daily_healthcare',
                                'XLY US Equity': 'daily_consumer_discreationary',
                                'XLP US Equity': 'daily_consumer_staples',
                                'XLU US Equity': 'daily_utilities',
                                'XBI US Equity': 'daily_biotech',
                                'MERVAL': 'daily_merval',
                                'GGAL': 'daily_galicia',
                                'BBAR': 'daily_bbva',
                                'BMA': 'daily_macro',
                                'CEPU': 'daily_cepu',
                                'PAM': 'daily_pam',
                                'YPF': 'daily_ypf'}}

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

        # Data cleaning 2
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

            # Add year, month and day numbers (Optional)
            # d['year'], d['month'], d['day'] = d.index.year, d.index.month, d.index.day

            i += leng
            n += 1

        # Export modified data to excel
        excel_prueba(info, data, True)