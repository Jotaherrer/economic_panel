import PyPDF2 as p
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.layout import LAParams
from pdfminer.converter import TextConverter
from io import StringIO
from pdfminer.pdfpage import PDFPage


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
