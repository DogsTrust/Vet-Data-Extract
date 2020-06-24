import re
import tabula as tb
import pandas as pd
from datetime import datetime as dt
#from nltk.tokenize import word_tokenize

#function to convert df column into array
def col_to_array(col):
    output = []
    for i in col:
        output.append(i)
    return output

#function to lowercase list and remove null values
def lower(x):
    out = []
    out_2 = []
    for i in x:
        i = str(i).lower()
        out.append(i)
    for j in out:
        if len(re.findall('nan', str(j))) > 0:
            j = re.sub('nan', ' ', j)
            out_2.append(j)
        else:
            out_2.append(j)
    return out_2

#function to tokenize each element in list
def tokenize_list(x):
    out = []
    for i in x:
        tokenized_by_word = word_tokenize(i)
        out.append(tokenized_by_word)
    return out


#date and time
now = dt.now()
dt_string = now.strftime("%Y%m%d%H%M")

#file paths
file_name = '1'
file_path_in = r'M:\PDF Data Extraction\Vet Record Examples (1)\Vet Record Examples\{}.pdf'.format(file_name)
file_path_out = r'M:\PDF Data Extraction\Vet Record Examples (1)\Vet Record Text Output\{}_{}_output.csv'.format(file_name,dt_string)

#output to csv
data = tb.convert_into(file_path_in, file_path_out, pages = 'all')

#read pdf into DataFrame
df = pd.read_csv(r'M:\PDF Data Extraction\Vet Record Examples (1)\Vet Record Text Output\{}_{}_output.csv'.format(file_name,dt_string))

#select free text column
df_txt = df.iloc[:,1]

#put free text column into an array
df_txt_arr = col_to_array(df_txt)

#lowercase and noise removal
df_clean = lower(df_txt_arr)

#tokenization
#print(tokenize_list(df_clean))

#lemmatization





