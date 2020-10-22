import PyPDF2 as p
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.layout import LAParams
from pdfminer.converter import TextConverter
from io import StringIO
from pdfminer.pdfpage import PDFPage

import calendar


# Create function to read PDF files (EMAE)
def get_pdf_file_content(path_to_pdf):
    resource_manager = PDFResourceManager(caching=True)
    out_text=StringIO()
    laParams = LAParams()
    text_converter = TextConverter(resource_manager, out_text, laparams=laParams)

    fp = open(path_to_pdf, 'rb')

    interpreteter = PDFPageInterpreter(resource_manager, text_converter)

    for page in PDFPage.get_pages(fp, pagenos=set(), maxpages=0, password='', caching=True, check_extractable= True):
        interpreteter.process_page(page)

    text = out_text.getvalue()

    fp.close()
    text_converter.close()
    out_text.close()

    return text


def get_filtered_data(data_indec, month_start, semester):
    """
    """
    dias = ['LU', 'MA', 'MI', 'JU', 'VI']
    meses_1 = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio']
    meses_2 = ['Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

    if semester == 2:
        for m in meses_2:
            if month_start == 'Julio':
                mes_inicio = data_indec.find(month_start)
                mes_fin = data_indec.find(meses_2[1])
            elif month_start == 'Agosto':
                mes_inicio = data_indec.find(month_start)
                mes_fin = data_indec.find(meses_2[2])
            elif month_start == 'Septiembre':
                mes_inicio = data_indec.find(month_start)
                mes_fin = data_indec.find(meses_2[3])
            elif month_start == 'Octubre':
                mes_inicio = data_indec.find(month_start)
                mes_fin = data_indec.find(meses_2[4])
            elif month_start == 'Noviembre':
                mes_inicio = data_indec.find(month_start)
                mes_fin = data_indec.find(meses_2[5])
            elif month_start == 'Diciembre':
                mes_inicio = data_indec.find(month_start)
        info = data_indec[mes_inicio:mes_fin]


    elif semester == 1:
        for m in meses_1:
            if month_start == 'Enero':
                mes_inicio = data_indec.find(month_start)
                mes_fin = data_indec.find(meses_1[1])
            elif month_start == 'Febrero':
                mes_inicio = data_indec.find(month_start)
                mes_fin = data_indec.find(meses_1[2])
            elif month_start == 'Marzo':
                mes_inicio = data_indec.find(month_start)
                mes_fin = data_indec.find(meses_1[3])
            elif month_start == 'Abril':
                mes_inicio = data_indec.find(month_start)
                mes_fin = data_indec.find(meses_1[4])
            elif month_start == 'Mayo':
                mes_inicio = data_indec.find(month_start)
                mes_fin = data_indec.find(meses_1[5])
            elif month_start == 'Junio':
                mes_inicio = data_indec.find(month_start)
        info = data_indec[mes_inicio:mes_fin]

    elif semester is not type(int):
        print('Pasa un número de semestre en formato numérico')


    return info



if __name__ == '__main__':

    archivo = './emae_09_2036477D631A.pdf'
    directory = os.listdir()
    data = get_pdf_file_content(archivo)

    # Busca cuadros con actividad economica
    data.find('Cuadro 1.')
    print(data[1002:1300])
    # Resumen destacado
    data.find('Durante julio, el Estimador')
    print(data[4573:5890])


    archivo2 = './calendario_indec_2020_2.pdf'
    data2 = get_pdf_file_content(archivo2)

    get_filtered_data(data2, 'Julio', 2)
    get_filtered_data(data2, 'Agosto', 2)

    julio = get_filtered_data(data2, 'Julio', 2)