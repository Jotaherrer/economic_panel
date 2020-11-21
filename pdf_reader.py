import PyPDF2 as p
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.layout import LAParams
from pdfminer.converter import TextConverter
from io import StringIO
from pdfminer.pdfpage import PDFPage


# Create function to read PDF files
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

    archivo = './MISHA INT Statements año 2020.pdf'
    pdf_info = open(archivo, 'rb')
    info = p.PdfFileReader(pdf_info)
    info.isEncrypted
    info.decrypt('1')

    for i in range(100000000):
        try:
            result = info.decrypt(str(i))
            if result == 1:
                break
        except:
            if i % 1000000 == 0:
                print('Decryption failed with password ',i)
            continue

    import string, random

    minimum = 1
    maximum = 10
    wmaximum = 1000000
    alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYX0123456789'
    alphabet = alphabet[:52] + string.digits + string.punctuation

    test_file = open('wl.txt', 'w')
    texto = ''
    for w in range(wmaximum):
        for x in random.sample(alphabet, random.randint(minimum, maximum)):
            texto += x
        test_file.write(texto+'\n')
        print(texto)
        texto = ''
    test_file.close()



    test_file2 = open('wl.txt', 'r')
    for i, l in enumerate(test_file2.readlines()):
        passw = l.strip()
        try:
            result = info.decrypt(passw)
            if result == 1:
                print('Success with word:',passw)
                break
        except:
            if i % 10000 == 0:
                print('Decryption failed with pass', passw)
    test_file2.close()

    import requests, bs4

    res = requests.get('https://www.ef.com/wwen/english-resources/english-vocabulary/top-3000-words/')
    soup = bs4.BeautifulSoup(res.text, 'lxml')
    data = soup.select('p')
    for w in data:
        print(len(w))
    data[-1]
    words = data[-1].text.split()
    print(type(words))