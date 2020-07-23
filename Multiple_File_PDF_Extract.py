from pdfminer3.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer3.converter import TextConverter
from pdfminer3.layout import LAParams
from pdfminer3.pdfpage import PDFPage
from io import StringIO
from datetime import datetime as dt
import os
import func_timeout as to
import re
import shutil as si

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

#Function to  move files
def file_move(file_list, destination):
    for file in file_list:
        si.move(file, destination)


#date and time
now = dt.now()
dt_string = now.strftime("%Y%m%d%H%M")

#File Paths
Drive = 'M:\\'
input_path = os.path.join(Drive,'PDF Data Extraction','Vet Record Examples (1)','Vet Record Examples')
output_path = os.path.join(Drive, 'PDF Data Extraction', 'Vet Record Examples (1)', 'Vet Record Text Multiple Output')
error_path = os.path.join(Drive, 'PDF Data Extraction', 'Vet Record Examples (1)', 'Vet Record Text Multiple Output\Error Folder')
success_path = os.path.join(Drive, 'PDF Data Extraction', 'Vet Record Examples (1)', 'Vet Record Text Multiple Output\Success Folder')
filelist = os.listdir(input_path)


#error checking
error_list = []
success_list = []
for i in filelist:
    path = input_path + '\{}'.format(i)
    file = os.path.splitext(i)[0]
    try:
        text = to.func_timeout(15, convert_pdf_to_txt, args=(path,))
        x = re.search("[a-zA-Z]", text)
        if x == None:
            error_list.append(str(path))
            print('{} Error - Empty Document'.format(file))
            continue
        else:
            f = open(output_path + '\{}_{}.txt'.format(file, dt_string), 'w+')
            f.write(text)
            f.close()
            success_list.append(str(path))
            print('{} Success'.format(file))
    except to.exceptions.FunctionTimedOut:
        error_list.append(str(path))
        print('{} conversion timed out'.format(file))
        # NOTE - This UnicodeEncodeError Try/Except is a bodge until I can sort out encoding
    except UnicodeEncodeError:
        error_list.append(str(path))
        print('{} Error - Unicode Encode Error'.format(file))

#move files that errored out to error folder
file_move(error_list, error_path)
#move successfull file to success folder
file_move(success_list, success_path)























