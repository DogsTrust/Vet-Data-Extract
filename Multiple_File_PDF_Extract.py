from pdfminer3.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer3.converter import TextConverter
from pdfminer3.layout import LAParams
from pdfminer3.pdfpage import PDFPage
from io import StringIO
from datetime import datetime as dt
import os

#Function to convert pdf to text file
def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text

#date and time
now = dt.now()
dt_string = now.strftime("%Y%m%d%H%M")

#path to files
input_path = r'M:\PDF Data Extraction\Vet Record Examples (1)\Vet Record Examples'
output_path = r'M:\PDF Data Extraction\Vet Record Examples (1)\Vet Record Text Multiple Output'

filelist = os.listdir(input_path)

for i in filelist:
    path = input_path + '\{}'.format(i)
    file = os.path.splitext(i)[0]
    f = open(
        r'\\dtdata\user$\AdamWilliams\PDF Data Extraction\Vet Record Examples (1)\Vet Record Text Multiple Output\{}_{}.txt'.format(file,dt_string),
        'w+')
    text = convert_pdf_to_txt(path)
    f.write(text)
    f.close()






