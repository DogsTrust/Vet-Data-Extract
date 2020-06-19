from pdfminer3.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer3.converter import TextConverter
from pdfminer3.layout import LAParams
from pdfminer3.pdfpage import PDFPage
from io import StringIO
from datetime import datetime as dt

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

#file paths
file_name = '1'
file_path = r'M:\PDF Data Extraction\Vet Record Examples (1)\Vet Record Examples\{}.pdf'.format(file_name)

#date and time
now = dt.now()
dt_string = now.strftime("%Y%m%d%H%M")

#print(convert_pdf_to_txt(file_path))
# create and write to text file
f = open(r'M:\PDF Data Extraction\Vet Record Examples (1)\Vet Record Text Output\{}_{}.txt'.format(file_name, dt_string), 'w')
f.write = (convert_pdf_to_txt(file_path))
f.close()

