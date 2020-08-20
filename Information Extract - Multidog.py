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


#
# #Search file for key term
# for file in search_file:
#Find most recent file in processed files
search_files = []
for title in titles:
    for file in file_list:
        if re.search(title_search, file) != None:
            search_files.append(re.search(title_search, file).string)


        for search_file in search_files:
            #list of found phrases
            phrase_find = []
            # File shit
            path = processed_files + '\\' + file
            f = open(path)
            file_string = f.read()
            #Split file into lines
            file_split = file_string.splitlines()
            #Return all instances of search phrase
            phrase_find.append(regexline(file_split, str(search_term)))
            f.close()

print(phrase_find)

