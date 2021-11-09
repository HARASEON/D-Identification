#-*-coding:utf-8-*-
import pandas as pd
import pydp as dp
import statistics
import numpy as np
import hashlib
from pprint import pprint
from random import randint
import csv

hashed_name = []
masked_id = []
masked_loan = []
masked_age = []
masked_address = []
age = []
dp_salary = []
dp_credit = []

dataset = pd.read_csv('./aa.csv', encoding='utf-8')
print(dataset)
original_dataset = pd.DataFrame(dataset)

print("\n==================================Deidentification===================================")

# Data encryption(SHA256)
o_name = original_dataset[['Name']]
#print(o_name)

for i in range(len(o_name)):
    a = o_name.loc[i,'Name']
    print(a)
    b = hashlib.sha256(a.encode()).hexdigest()
    hashed_name.append(b)
    #dataset['Name'] = b

dataset['Name'] = hashed_name

# print(dataset)


# Data masking with symbol('*')
m_id = original_dataset[['id']]
m_address = original_dataset[['주소']]
#print(m_id)
#print(m_address)
m_salary = original_dataset[['Salary (천원)']]
m_loan = original_dataset[['대출']]
m_credit = original_dataset[['신용지수']]
m_age = original_dataset[['age']]

for i in range(len(m_id)):
    a = m_id.loc[i,'id']
    #print(a)
    if a < 21000:
        a ='20***'
        masked_id.append(a)
    else:
        b ='21***'
        #print(a)
        masked_id.append(b)

dataset['id'] = masked_id

for i in range(len(m_address)):
    a =  m_address.loc[i,'주소']
    b1 = a.split(' ')[0]
    masked_address.append(b1 + " *** *** ##")

dataset['주소'] = masked_address
pprint(dataset)
'''
for i in range(len(m_loan)):
    a =  m_loan.loc[i,'대출']
    masked_loan.append("#")

dataset['대출'] = masked_loan
'''
for i in range(len(m_age)):
    a = m_age.loc[i,'age']
    a = str(a)[0]
    masked_age.append(a + "#")

dataset['age'] = masked_age


# Data including noise( Salary(천원),  신용지수)
m_age = original_dataset[['age']]
m_salary = original_dataset[['Salary (천원)']]
m_credit = original_dataset[['신용지수']]

print(type(m_salary))

for i in range(len(m_salary)):
    a2 = m_salary.loc[i,'Salary (천원)']
    a2 = int(a2.replace(",",""))
    a4 = m_credit.loc[i,'신용지수']

    a2 += randint(1000,5000)
    a4 += randint(10,30)

    c = round(a2, 0)
    c = str(c)[:2] + "," + str(c)[-3:]
    e = round(a4, 0)

    dp_salary.append(c)
    dp_credit.append(e)

dataset['Salary (천원)'] = dp_salary
dataset['신용지수'] = dp_credit

pprint(dataset)

#f2 = open("D-identification_hw1.csv", "w")
dataset.to_csv("D-identification_hw1.csv", sep=",")
