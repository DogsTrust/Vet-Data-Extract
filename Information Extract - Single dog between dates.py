#import libraries
import pandas as pd
import os
import re
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

#User search for DogID and search term
dogid = '0004' #input('Enter DogID: ' )
search_term = 'bar' #input('Enter Search Term: ')

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

#Search file for key term
for file in search_file:
    #list of found phrases
    phrase_find = []
    #list of dates to split search
    dates = []

    #File shit
    path = processed_files + '\\' +file
    f = open(path)
    file_string = f.read()

    #Tokenize file
    file_words = word_tokenize(file_string)

    #Split file into lines
    file_split = file_string.splitlines()

    #Create ditionary so that each line in filesplit has a line_id
    dict_list = []
    line_number = 0
    for line in file_split:
        line_dict = {'Line No.':line_number, 'Line':line}
        dict_list.append(line_dict)
        line_number += 1

    #Return list of all dates in the file
    for item in file_words:
        if re.search('\d+/\d+/\d+', str(item)) != None:
            dates.append(item)

    #Create dictionary which searches each element in [Dates] and stores for each element: date, line
    #it appears in, index of this line
    start_date = 0
    end_date = 2
    min_line = 0
    max_line = 0
    use_dates = dates[start_date:end_date]
    search_lines = []
    read_between_lines = []
    #Going forward need to iterate through all dates in date list for all lines greater than max_line
    #on previous iteration

    #Get line values between first two dates in list
    for dict in dict_list:
        value_list = list(dict.values())
        if (len(read_between_lines) < 2):
            if re.search(use_dates[0], value_list[-1]) != None:
                read_between_lines.append(value_list[0])
            if re.search(use_dates[-1], value_list[-1]) != None:
                read_between_lines.append(value_list[0])

    #Get lines between these dates
    for dict in dict_list:
        value_list = list(dict.values())
        if (value_list[0] >= read_between_lines[0]) and (value_list[0] < read_between_lines[-1]):
            search_lines.append(value_list[1])



    #Return all instances of search phrase between these dates
    phrase_find.append([use_dates[0], regexline(search_lines, str(search_term))])
    f.close()



print(phrase_find)







