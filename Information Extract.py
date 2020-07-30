#import libraries
import pandas as pd
import os
import re
import xlrd

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

#User search for DogID and search term
dogid = input('Enter DogID:' )
#search_term = input('Enter Search Term: ')

#Filter df by Unique DogId's and VetId's
df_dogid_filter = (df[df['DogId']==dogid])
for vetid in unique_vetids:
    max_age_filter = (df_dogid_filter[df_dogid_filter['Age_Months']==df_dogid_filter.Age_Months.max()])

#Recreate most recent file name From Master Sheet
length = len(max_age_filter.index)
for i in range(length):
    col_ids = max_age_filter.iloc[i]
    title_search = 'O'+col_ids[1]+' V'+col_ids[2]+' D'+col_ids[0]+' '+col_ids[3]

#Find most recent file in processed files
search_file = []
for file in file_list:
    if re.search(title_search, file) != None:
        search_file.append(re.search(title_search, file).string)










