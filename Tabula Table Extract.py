import tabula as tb
import pandas as pd
from datetime import datetime as dt

#date and time
now = dt.now()
dt_string = now.strftime("%Y%m%d%H%M")

#file paths
file_name = '1'
file_path_in = r'M:\PDF Data Extraction\Vet Record Examples (1)\Vet Record Examples\{}.pdf'.format(file_name)
file_path_out = r'M:\PDF Data Extraction\Vet Record Examples (1)\Vet Record Text Output\{}_{}_output.csv'.format(file_name,dt_string)

data = tb.convert_into(file_path_in, file_path_out)
