#-*-coding:utf-8-*-
import pandas as pd
import pydp as dp
import statistics
import numpy as np
import hashlib
from pprint import pprint
from pyope.ope import OPE
import csv


hashed_name = []
masked_id = []
stat_loan = []
masked_age = []
masked_address = []
age = []
stat_salary = []
c_credit = []

dataset = pd.read_csv('./aa.csv', encoding='utf-8')
print(dataset)
original_dataset = pd.DataFrame(dataset)



print("\n==================================Deidentification===================================\n")

# Data encryption(SHA256)
# name
o_name = original_dataset[['Name']]

for i in range(len(o_name)):
    a = o_name.loc[i,'Name']
    print(a)
    b = hashlib.sha256(a.encode()).hexdigest()
    hashed_name.append(b)
    #dataset['Name'] = b

dataset['Name'] = hashed_name
print("1st step: encrypting name\n", dataset)


# Data masking with symbol('*')
# rounding id, age
m_id = original_dataset[['id']]
m_address = original_dataset[['주소']]
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


for i in range(len(m_age)):
    a = m_age.loc[i,'age']
    a = str(a)[0]
    masked_age.append(a + "#")

dataset['age'] = masked_age
print("2nd step: rounding\n",dataset)


# aggregated data by median
# Salary
tem_list = []
for i in range(len(m_salary)):
    a = m_salary.loc[i,'Salary (천원)']
    a = int(a.replace(",",""))
    tem_list.append(a)
    array=np.array(tem_list)

c = np.median(array) # data type : float64

for i in range(len(m_salary)):
    d = int(round(c,0)) #trasform from float to int
    e = str(d)[:2] + "," + str(d)[-3:]
    stat_salary.append(e)

dataset['Salary (천원)'] = stat_salary

# 대출
tem1_list = []

for i in range(len(m_loan)):
    b=m_loan.loc[i,'대출'] # 값만 추출
    tem1_list.append(b)
    array1 = np.array(tem1_list)
e = np.median(array1)
for i in range(len(m_loan)):
    f= int(e)
    stat_loan.append(f)
dataset['대출'] = stat_loan

print("3rd step: aggregated data\n", dataset)


# ope encoding
# credit
print("\n==================================================Order Preserving Encryption================================================\n")

m_credit = original_dataset[['신용지수']]
random_key = OPE.generate_key()
cipher = OPE(random_key)
for i in range(len(m_credit)):
    a = m_credit.loc[i,'신용지수']
    b = hex(cipher.encrypt(i))
    c_credit.append(b)

dataset['신용지수'] = c_credit
print(dataset)

# deletion by Degree
print("\n========================================================Deletion by degree=========================================================\n")
edited_dataset = dataset.drop([dataset.index[3],dataset.index[6]])
print(edited_dataset)

edited_dataset.to_csv("Quiz.csv", sep=",")

