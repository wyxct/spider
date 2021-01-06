import csv
import re

file = "data.csv"

with open(file, 'r') as f:
    reader = csv.DictReader(f)
    nam=[]
    nat = []
    ind = []
    wee=[]
    nam1=[]
    nat1=[]
    ind1=[]
    wee1=[]

    for row in reader :
        nat.append(row['NATIONAL POLLING AVERAGE'])
        ind.append(row['INDIVIDUAL CONTRIBUTIONS'])
        wee.append(row['WEEKLY NEWS COVERAGE'])
        nam.append(row['Qualified for the November debate'])
for name in nam:
    nam1.append(name)

for num in nat:
    result=re.findall(r"\d+\.?\d*", num)
    nat1.append(result[0])

for num in ind:
    result=re.findall(r"\d+\.?\d*", num)
    ind1.append(result[0])

for num in wee:
    result=re.findall(r"\d+\.?\d*", num)
    wee1.append(result[0])
print(nam1)
print(nat1)
print(ind1)
print(wee1)