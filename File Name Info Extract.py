from datetime import datetime as dt
import os
import re
import pandas as pd
from openpyxl import load_workbook

#function to isolate ID numbers
def id(lst):
    output = []
    for ids in lst:
        for id in ids:
            output.append(id[1:len(i)])
    return output

#Function to isolate age
def age_fn(lst):
    output = []
    for ids in lst:
        for id in ids:
            output.append(id)
    return output

#Drive and file paths
Drive = 'M:\\'
input_path = os.path.join(Drive,'PDF Data Extraction','Vet Record Examples (1)','Text')
master_excel = os.path.join(Drive, 'PDF Data Extraction','Vet Record Examples (1)','Master_Record.xlsx')

filelist = os.listdir(input_path)
print(filelist)

owner = []
vet = []
dog = []
age = []
for i in filelist:
    owner.append(re.findall('O\d+', str(i)))
    vet.append(re.findall('V\d+', str(i)))
    dog.append(re.findall('D\d+', str(i)))
    age.append(re.findall('\dyrs\s\dm', str(i)))

owner_id = id(owner)
vet_id = id(vet)
dog_id = id(dog)
age = age_fn(age)

print(owner_id, vet_id, dog_id, age)

data = {'DogId':dog_id, 'OwnerId':owner_id, 'VetId':vet_id, 'Age':age}
df= pd.DataFrame(data)

#write to master doc
book = load_workbook(master_excel)
writer = pd.ExcelWriter(master_excel, engine='openpyxl')
writer.book = book
writer.sheets = {ws.title: ws for ws in book.worksheets}
for sheetname in writer.sheets:
    df.to_excel(writer,sheet_name=sheetname, startrow=writer.sheets[sheetname].max_row, index = False,header= False)

writer.save()



