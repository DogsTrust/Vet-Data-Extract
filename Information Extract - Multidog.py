#import libraries
import pandas as pd
import os
import re
import numpy as np
from datetime import datetime as dt

#Function to pull out all lines containing a given word
def regexline(i, exp):
    output = []
    expU = exp.upper()
    expl = exp.lower()
    expT = exp.capitalize()
    if len(re.findall(expU, i)) > 0:
        output.append(i)
    if len(re.findall(expl, i)) > 0:
        output.append(i)
    if len(re.findall(expT, i)) > 0:
        output.append(i)
    return output

#Drives and File Paths
Drive = 'C:\\'
master_excel = os.path.join(Drive, 'Python', 'Vet Record Project' ,'Master_Record.xlsx')
processed_files = os.path.join(Drive, 'Python', 'Vet Record Project', 'Vet Record Text Multiple Output', 'Processed Vet Records')
file_list = os.listdir(processed_files)
output = os.path.join(Drive, 'Python', 'Vet Record Project', 'Vet Record Text Multiple Output', 'Search Output')

#Read In Master Excel
df = pd.read_excel(master_excel)

#Find Unique DogID's and VetId's
unique_dogids = df.DogId.unique()
unique_vetids = df.VetId.unique()

#column names to be used in df_main
col_names = df.columns

#date and time
now = dt.now()
dt_string = now.strftime("%Y%m%d%H%M")

#dataframe to hold most recent vet record for each vet and dog id
df_main = pd.DataFrame(columns = col_names)
df['Total_Age'] = df['Age_Years'] + (df['Age_Months']/12)

for dogid in unique_dogids:
    #Dog ID filter
    df1 = df[df['DogId'] == dogid]
    vetids = np.unique(((df1['VetId']).tolist()))
    for vetid in vetids:
        #Age Filter
        vet_filter = df1[df1['VetId'] == vetid]
        df2 = (vet_filter[vet_filter['Total_Age'] == vet_filter.Total_Age.max()])
        df_main = df_main.append(df2)
#User search for DogID and search term
search_term = 'Vacc' #str(input('Enter Search Term: '))


#Recreate most recent file names From Master Sheet
length = len(df_main.index)
titles = []
for i in range(length):
    col_ids = df_main.iloc[i]
    if col_ids[3] == 0.0:
        title_search = 'O' + str(int(col_ids[1])) + ' V' + str(int(col_ids[2])) + ' D' + str(
            int(col_ids[0])) + ' ' + str(int(col_ids[4])) + 'm'
    elif col_ids[4] == 0.0:
        title_search = 'O' + str(int(col_ids[1])) + ' V' + str(int(col_ids[2])) + ' D' + str(
            int(col_ids[0])) + ' ' + str(int(col_ids[3])) + 'yr'
    else:
        title_search = 'O' + str(int(col_ids[1])) + ' V' + str(int(col_ids[2])) + ' D' + str(
            int(col_ids[0])) + ' ' + str(int(col_ids[3])) + 'yr ' + str(int(col_ids[4])) + 'm'
    titles.append(title_search)

##Search for most recent files in processed files
file_search = []
#look through processed files
for file in file_list:
    #check against most recent titles
    for title in titles:
        if re.search(title, str(file)) != None:
            file_search.append(file)

#df_out = pd.DataFrame(columns=['DogID','OwnerID','VetID','Dog Age (Yrs)', ,'Date','Search Result'])

# list of found phrases
phrase_find = []
matches = []
for item in file_search:
    # File
    path = processed_files + '\\' + item
    f = open(path)
    file_string = f.read()
    #Split file into lines
    file_split = file_string.splitlines()

    Dog_ID = (re.search('D\d{4}', item).group())[1:]
    Owner_ID = (re.search('O\d{4}',item).group())[1:]
    Vet_ID = (re.search('V\d{3}', item).group())[1:]
    if (re.search('\d+yr',item)) != None:
        Dog_Age_Years = (re.search('\d+yr',item).group())
    else:
        Dog_Age_Years = 0
    if (re.search('\d+m',item)) != None:
        Dog_Age_Months = (re.search('\d+m',item).group())
    else:
        Dog_Age_Months = 0

    # Create ditionary so that each line in filesplit has a line_id
    line_dict = {}
    line_number = 0
    for line in file_split:
        line_dict[line_number] = line
        line_number += 1

    # Return list of all dates in the file
    dates = [0]
    item_list = line_dict.items()
    for item in item_list:
        if re.search('\d+/\d+/\d+', str(item[1])) != None:
            dates.append(item[0])

    for num in range(len(dates) - 1):
        ran = dates[num: num + 2]
        lin_search = np.linspace(ran[0], ran[1] - 1, ran[1] - ran[0])
        first_date = (line_dict[lin_search[0]])
        for lin in lin_search:
            Term_Found = regexline(line_dict[lin], str(search_term))
            if len(Term_Found) > 0:
                for entry in range(len(Term_Found)):
                    matches.append([Dog_ID, Owner_ID, Vet_ID, Dog_Age_Years, Dog_Age_Months, first_date, Term_Found[entry]])

df_out = pd.DataFrame(matches, columns=['Dog_ID', 'Owner_ID', 'Vet_ID', 'Dog_Age_Years', 'Dog_Age_Months', 'Date', 'Search Result'])
df_out.to_csv(output + '\Multi_Dog_Search_{}_{}.csv'.format(search_term, dt_string), index=False)
f.close()
