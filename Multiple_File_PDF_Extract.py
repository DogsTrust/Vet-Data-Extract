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

#Function to test file name format
def name_format(file_list):
    To_be_converted = []
    Not_to_be_converted = []
    for file in file_list:
        if re.search('O\d+\sV\d+\sD\d+\s\dyrs\s\dm', file) != None:
            To_be_converted.append(file)
        else:
            Not_to_be_converted.append(file)
    return To_be_converted, Not_to_be_converted

#Function to move files to error list
def error_append(file_list, input_path, error_list):
    for file in file_list:
        error_list.append(input_path + '\\' + file)
        print('{} Error - Incorrect File Name Format'.format(file))

#date and time
now = dt.now()
dt_string = now.strftime("%Y%m%d%H%M")

#File Paths - Change these if you run somewhere else
Drive = 'M:\\'
input_path = os.path.join(Drive,'PDF Data Extraction','Vet Record Examples (1)','Vet Record Examples')
output_path = os.path.join(Drive, 'PDF Data Extraction', 'Vet Record Examples (1)', 'Vet Record Text Multiple Output','Processed Vet Records')
error_path = os.path.join(Drive, 'PDF Data Extraction', 'Vet Record Examples (1)', 'Vet Record Text Multiple Output\Error Folder')
success_path = os.path.join(Drive, 'PDF Data Extraction', 'Vet Record Examples (1)', 'Vet Record Text Multiple Output\Success Folder')
filelist = os.listdir(input_path)


#error checking
error_list = []
success_list = []
#Check file name has correct format
conversion_list = (name_format(filelist))[0]
error_append((name_format(filelist))[1], input_path, error_list)

for i in conversion_list:
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























