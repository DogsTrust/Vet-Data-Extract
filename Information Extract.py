import pandas as pd
import os
import xlrd

Drive = 'M:\\'
master_excel = os.path.join(Drive, 'PDF Data Extraction','Vet Record Examples (1)','Master_Record.xlsx')
df = pd.read_excel(master_excel, dtype=str, engine='xlrd')
unique_dogids = df.DogId.unique()
unique_vetids = df.VetId.unique()

dogid = input('Enter DogID:' )

df_dogid_filter = (df[df['DogId']==dogid])
for vetid in unique_vetids:
    max_age_filter = (df_dogid_filter[df_dogid_filter['Age_Months']==df_dogid_filter.Age_Months.max()])
length = len(max_age_filter.index)

for i in range(length):
    col_ids = max_age_filter.iloc[i]
    title_search = 'O'+col_ids[1]+' V'+col_ids[2]+' D'+col_ids[0]+' '+col_ids[3]





