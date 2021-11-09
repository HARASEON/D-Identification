#-*-coding:utf-8-*-
import pandas as pd
from pandas import DataFrame
import numpy as np
from pprint import pprint
from random import randint
import csv
from pyope.ope import OPE


dataset = pd.read_csv('./aa.csv', encoding='utf-8')
print(dataset,"\n")
original_dataset = pd.DataFrame(dataset)
sort_value = original_dataset.sort_values(by='신용지수',ascending = True)
print("sorted table by 신용지수\n",sort_value)


# ope encoding
# credit
print("\n==================================================Order Preserving Encryption================================================\n")
c_credit = []
o_credit = []
d_credit = []
m_credit = original_dataset[['신용지수']]
n_credit = sort_value[['신용지수']]
'''
for i in range(len(m_credit)):
    a = m_credit.loc[i,'신용지수']
    if a <= 710:
        a += randint(-1000, -757)
    elif a <= 720:
        a += randint(-756, -506)
    elif a <= 740:
        a += randint(-505, -255)
    elif a <= 820:
        a += randint(-254, -4)
    elif a <= 880:
        a += randint(-3, 247)
    elif a <= 910:
        a += randint(248, 498)
    elif a <= 920:
        a += randint(499, 749)
    else:
        a += randint(750, 1000)
    b = round(a,0)
    c_credit.append(b)
'''
# using package
random_key = OPE.generate_key()
cipher = OPE(random_key)
for i in range(len(m_credit)):
    a = m_credit.loc[i,'신용지수']
    b=hex(cipher.encrypt(i))
    d_credit.append(b)

#assert cipher.decrypt(cipher.encrypt(1337)) == 1337
#dataset['신용지수'] = c_credit
dataset['신용지수'] = d_credit
pprint(dataset)
dataset.to_csv("ope.csv", sep=",")
