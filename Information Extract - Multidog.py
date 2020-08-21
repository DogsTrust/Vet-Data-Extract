#import libraries
import pandas as pd
import os
import re
import numpy as np
from nltk.tokenize import word_tokenize

import xlrd

#Function to pull out all lines containing a given word
def regexline(list, exp):
    output = []
    expU = exp.upper()
    expl = exp.lower()
    expT = exp.capitalize()
    for i in list:
        if len(re.findall(expU, i)) > 0:
            output.append(i)
        if len(re.findall(expl, i)) > 0:
            output.append(i)
        if len(re.findall(expT, i)) > 0:
            output.append(i)
    return output


#Drives and File Paths
Drive = 'M:\\'
master_excel = os.path.join(Drive, 'PDF Data Extraction','Vet Record Examples (1)','Master_Record.xlsx')
processed_files = os.path.join(Drive, 'PDF Data Extraction','Vet Record Examples (1)', 'Vet Record Text Multiple Output','Processed Vet Records')
file_list = os.listdir(processed_files)

#Read In Master Excel
df = pd.read_excel(master_excel, dtype=str, engine='xlrd')

#Find Unique DogID's and VetId's
unique_dogids = df.DogId.unique()
unique_vetids = df.VetId.unique()

#column names to be used in df_main
col_names = df.columns

#dataframe to hold most recent vet record for each vet and dog id
df_main = pd.DataFrame(columns = col_names)
for dogid in unique_dogids:
    #Dog ID filter
    df1 = df[df['DogId'] == dogid]
    for vetid in unique_vetids:
        #Age Filter
        df2 = df1[df1['Age_Months'] == df1.Age_Months.max()]
    df_main = df_main.append(df2)

#User search for DogID and search term
search_term = input('Enter Search Term: ')


#Recreate most recent file names From Master Sheet
length = len(df_main.index)
titles = []
for i in range(length):
    col_ids = df_main.iloc[i]
    title_search = 'O'+col_ids[1]+' V'+col_ids[2]+' D'+col_ids[0]+' '+col_ids[3]
    titles.append(title_search)

#Search for most recent files in processed files
file_search = []
#look through processed files
for file in file_list:
    #check against most recent titles
    for title in titles:
        if re.search(title, str(file)) != None:
            file_search.append(file)


df_out = pd.DataFrame(columns=['DogID','OwnerID','VetID','Dog Age','Phrase Date','Search Phrase'])

# list of found phrases
phrase_find = []
for item in file_search:
    # File shit
    path = processed_files + '\\' + item
    f = open(path)
    file_string = f.read()
    #Split file into lines
    file_split = file_string.splitlines()
    #
    Dog_ID = (re.search('D\d{4}', item).group())[1:]
    Owner_ID = (re.search('O\d{4}',item).group())[1:]
    Vet_ID = (re.search('V\d{3}', item).group())[1:]
    Dog_Age = re.search('\d+yrs\s\d+m',item).group()
    Term_Found = regexline(file_split, str(search_term))
    for Term in Term_Found:
        #Return all instances of search phrase
        add_to_master = [Dog_ID, Owner_ID, Vet_ID, Dog_Age, ' ', Term]
        print(add_to_master)
    f.close()






