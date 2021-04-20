# import libraries
import pandas as pd
import os
import re
import numpy as np
from datetime import datetime as dt
from nltk.tokenize import word_tokenize

import xlrd


# Function to pull out all lines containing a given word
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

# Drives and File Paths
Drive = 'C:\\'
master_excel = os.path.join(Drive, 'Python', 'Vet Record Project', 'Master_Record.xlsx')
processed_files = os.path.join(Drive, 'Python', 'Vet Record Project',
                               'Vet Record Text Multiple Output', 'Processed Vet Records')
file_list = os.listdir(processed_files)
output = os.path.join(Drive, 'Python', 'Vet Record Project', 'Vet Record Text Multiple Output', 'Search Output')

#date and time
now = dt.now()
dt_string = now.strftime("%Y%m%d%H%M")

# Read In Master Excel
df = pd.read_excel(master_excel)

# Find Unique DogID's and VetId's
unique_dogids = df.DogId.unique()
unique_vetids = df.VetId.unique()

# User search for DogID and search term
dogid =  int(input('Enter DogID: ' ))
search_term = str(input('Enter Search Term: '))
df['Total_Age'] = df['Age_Years'] + (df['Age_Months']/12)

# Filter df by Unique DogId's and VetId's
df_dogid_filter = (df[df['DogId'] == dogid])

#Get individual vet id's for given dog id's
vetids = np.unique(((df_dogid_filter['VetId']).tolist()))

titles = []
for vetid in vetids:
    vet_filter = df_dogid_filter[df_dogid_filter['VetId']==vetid]
    max_age_filter = (vet_filter[vet_filter['Total_Age'] == vet_filter.Total_Age.max()])
    # Recreate most recent file name From Master Sheet
    length = len(max_age_filter.index)
    for i in range(length):
        col_ids = max_age_filter.iloc[i]
        if col_ids[3] == 0.0:
            title_search = 'O' + str(int(col_ids[1])) + ' V' + str(int(col_ids[2])) + ' D' + str(int(col_ids[0])) + ' ' + str(int(col_ids[4])) + 'm'
        elif col_ids[4] == 0.0:
            title_search = 'O' + str(int(col_ids[1])) + ' V' + str(int(col_ids[2])) + ' D' + str(int(col_ids[0])) + ' ' + str(int(col_ids[3])) + 'yr'
        else:
            title_search = 'O' + str(int(col_ids[1])) + ' V' + str(int(col_ids[2])) + ' D' + str(int(col_ids[0])) + ' ' + str(int(col_ids[3])) + 'yr ' + str(int(col_ids[4])) + 'm'
        titles.append(title_search)

# Find most recent file in processed files
search_file = []
matches = []
for file in file_list:
    # check against most recent titles
    for title in titles:
        if re.search(title_search, file) != None:
            search_file.append(re.search(title_search, file).string)

# Search file for key term
for file in search_file:
    # list of found phrases
    phrase_find = []
    # list of dates to split search
    dates = [0]

    # File gubbins
    path = processed_files + '\\' + file
    f = open(path)
    file_string = f.read()

    # Split file into lines
    file_split = file_string.splitlines()

    Dog_ID = (re.search('D\d{4}', file).group())[1:]
    Owner_ID = (re.search('O\d{4}', file).group())[1:]
    Vet_ID = (re.search('V\d{3}', file).group())[1:]
    if (re.search('\d+yr', file)) != None:
        Dog_Age_Years = (re.search('\d+yr', file).group())
    else:
        Dog_Age_Years = 0
    if (re.search('\d+m', file)) != None:
        Dog_Age_Months = (re.search('\d+m', file).group())
    else:
        Dog_Age_Months = 0

    # Create ditionary so that each line in filesplit has a line_id
    line_dict = {}
    line_number = 0
    for line in file_split:
        line_dict[line_number] = line
        line_number += 1

    # Return list of all dates in the file
    item_list = line_dict.items()
    for item in item_list:
        if re.search('\d+/\d+/\d+', str(item[1])) != None:
            dates.append(item[0])

    out = []
    for num in range(len(dates) - 1):
        ran = dates[num: num + 2]
        lin_search = np.linspace(ran[0], ran[1] -1, ran[1] - ran[0])
        first_date = (line_dict[lin_search[0]])

        for lin in lin_search:
            search = regexline(line_dict[lin], str(search_term))
            if len(search) > 0:
                for entry in range(len(search)):
                    matches.append([Dog_ID, Owner_ID, Vet_ID, Dog_Age_Years, Dog_Age_Months, first_date, search[entry]])
            else:
                continue

df_out = pd.DataFrame(matches, columns=['Dog_ID', 'Owner_ID', 'Vet_ID', 'Dog_Age_Years', 'Dog_Age_Months', 'Date', 'Search Result'])
df_out.to_csv(output + '\Single_Dog_Search_{}_{}_{}.csv'.format(dogid, search_term, dt_string), index=False)
f.close()



