import re

#Function to pull out all lines containing the word vet
def regexline(list, exp):
    output = []
    for i in list:
        if len(re.findall(exp, i)) > 0:
            output.append(i)
    return output


#import file
file = open(r'M:\PDF Data Extraction\Vet Record Examples (1)\Vet Record Text Output\pdf_1.txt', "r")

file_string = file.read()

#split file by lines
file_split = file_string.splitlines()

#Regex for address
Address = "\d+\w?\s\w+\s\w+\n\w+\n\w+\n\w+\d+\s\d+\w+"


result_add = re.findall(Address, file_string)

print(regexline(file_split, 'vet'))

file.close()