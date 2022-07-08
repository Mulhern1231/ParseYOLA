import pandas as pd
import xlwings as xw
import os

d = {
    "phone": 0,
    "url":   0,
    "views": 0,
    "price": 0,
    "name":  0,
    "date":  0,
    "profile_url": 0,
    "data-reg":    0,
    "rating":      0,
    "rating_cnt":  0,
    "active":      0,
    "profile_url": 0,
    "sold":        0,
}

newExel = pd.DataFrame(data=d, index=[0])




df = pd.read_excel('output.xlsx')
    
ReadFile = open('Link.txt', 'r')
wr = open('Link.txt', 'a')

linkListFile = []
for line in ReadFile:
    linkListFile.append(line.replace("\n", ""))

for iexel in range(len(df)):
    exel = str(df.iloc[iexel, 2])
    found = False
    for i in linkListFile:
        if str(df.iloc[iexel, 2]) == i:
            found = True
    if found == False:
        print(f"NEW - {str(df.iloc[iexel, 2])}")
        wr.write(str(df.iloc[iexel, 2]) + '\n')
        
        lineListAppend = []
        for Xindex in range(1, 13):
            lineListAppend.append(df.iloc[iexel, Xindex])
        newExel.loc[len(newExel)] = lineListAppend
print(newExel)
writer = pd.ExcelWriter('OUTFinal.xlsx')
df.to_excel(writer)
writer.save()
