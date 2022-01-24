# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 17:37:44 2019

@author: McCabeR
"""

import pandas as pd
import glob
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

contacts = pd.read_excel('h:\cb_contacts.xlsx')
supl = contacts['Stdname'][0:63] # std names and no yellow
supl = supl.drop(supl.index[[3, 26, 36]]) # 3 red
supl = supl.reset_index(drop=True)
supl[60] = 'Powershop'
answered = ['British Gas', 'EDF', 'E.ON', 'npower', 'Scottish Power', 'SSE']
totsup = len(answered)
sizes = ['large', 'medium', 'small']
cat=len(sizes) # 3
large = list(supl.iloc[[7, 14, 16, 35, 46, 50]]) # 6
medium = list(supl.iloc[[2, 8, 10, 18, 24, 36, 40, 56]]) # 8
small = list(supl.drop([7, 14, 16, 35, 46, 50, 2, 8, 10, 18, 24, 36, 40, 56])) # remaining 46+1

input_dir = 'H:/Credit_Balance/Large/'
output_dir = 'H:/Credit_Balance/Large/'
returns_list = glob.glob(input_dir + '**/*.xlsx', recursive=True)

returns_agg = pd.DataFrame()
for file in returns_list:
    cb_multi = pd.ExcelFile(file)
    data = pd.read_excel(cb_multi, 'DatAgg')
    data['source'] = data.iloc[0,7] # use std names
    if data.iloc[0,7] in large:
        data['size'] = 'large'
    elif data.iloc[0,7] in medium:
        data['size'] = 'medium'
    else:
        data['size'] = 'small'
    returns_agg = pd.concat([returns_agg, data], sort=False)
returns_agg.reset_index(drop=True, inplace=True)

ts1 = np.where(returns_agg.Date == np.datetime64('2017-10-01'), True, False)
ts2 = np.where(returns_agg.Date == np.datetime64('2018-04-01'), True, False)
ts3 = np.where(returns_agg.Date == np.datetime64('2018-10-01'), True, False)

## Open

# +TOG
a11 = [returns_agg.loc[ts1 & (returns_agg['source'] == supl) & (returns_agg['+/-/0/N'] == '+') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'O') & (returns_agg['Gr/Nt'] == 'Gr'),'Value(£)'] for supl in answered]
a12 = [returns_agg.loc[ts2 & (returns_agg['source'] == supl) & (returns_agg['+/-/0/N'] == '+') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'O') & (returns_agg['Gr/Nt'] == 'Gr'),'Value(£)'] for supl in answered]
a13 = [returns_agg.loc[ts3 & (returns_agg['source'] == supl) & (returns_agg['+/-/0/N'] == '+') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'O') & (returns_agg['Gr/Nt'] == 'Gr'),'Value(£)'] for supl in answered]

# +TON
a21 = [returns_agg.loc[ts1 & (returns_agg['source'] == supl) & (returns_agg['+/-/0/N'] == '+') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'O') & (returns_agg['Gr/Nt'] == 'Nt'),'Value(£)'] for supl in answered]
a22 = [returns_agg.loc[ts2 & (returns_agg['source'] == supl) & (returns_agg['+/-/0/N'] == '+') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'O') & (returns_agg['Gr/Nt'] == 'Nt'),'Value(£)'] for supl in answered]
a23 = [returns_agg.loc[ts3 & (returns_agg['source'] == supl) & (returns_agg['+/-/0/N'] == '+') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'O') & (returns_agg['Gr/Nt'] == 'Nt'),'Value(£)'] for supl in answered]

# -TOG
a31 = [returns_agg.loc[ts1 & (returns_agg['source'] == supl) & (returns_agg['+/-/0/N'] == '-') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'O') & (returns_agg['Gr/Nt'] == 'Gr'),'Value(£)'] for supl in answered]
a32 = [returns_agg.loc[ts2 & (returns_agg['source'] == supl) & (returns_agg['+/-/0/N'] == '-') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'O') & (returns_agg['Gr/Nt'] == 'Gr'),'Value(£)'] for supl in answered]
a33 = [returns_agg.loc[ts3 & (returns_agg['source'] == supl) & (returns_agg['+/-/0/N'] == '-') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'O') & (returns_agg['Gr/Nt'] == 'Gr'),'Value(£)'] for supl in answered]

# -TON
a41 = [returns_agg.loc[ts1 & (returns_agg['source'] == supl) & (returns_agg['+/-/0/N'] == '-') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'O') & (returns_agg['Gr/Nt'] == 'Nt'),'Value(£)'] for supl in answered]
a42 = [returns_agg.loc[ts2 & (returns_agg['source'] == supl) & (returns_agg['+/-/0/N'] == '-') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'O') & (returns_agg['Gr/Nt'] == 'Nt'),'Value(£)'] for supl in answered]
a43 = [returns_agg.loc[ts3 & (returns_agg['source'] == supl) & (returns_agg['+/-/0/N'] == '-') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'O') & (returns_agg['Gr/Nt'] == 'Nt'),'Value(£)'] for supl in answered]

# Ratio ON
a51 = [np.divide(a21[i], a41[i], out = np.zeros_like(a21[i]), where = a41[i]!=0) for i in range(totsup)]
a52 = [np.divide(a22[i], a42[i], out = np.zeros_like(a22[i]), where = a42[i]!=0) for i in range(totsup)]
a53 = [np.divide(a23[i], a43[i], out = np.zeros_like(a23[i]), where = a43[i]!=0) for i in range(totsup)]

# Sum OG
a61 = [np.add(a11[i], a31[i]) for i in range(totsup)]
a62 = [np.add(a12[i], a32[i]) for i in range(totsup)]
a63 = [np.add(a13[i], a33[i]) for i in range(totsup)]

# Sum ON
a71 = [np.add(a21[i], a41[i]) for i in range(totsup)]
a72 = [np.add(a22[i], a42[i]) for i in range(totsup)]
a73 = [np.add(a23[i], a43[i]) for i in range(totsup)]

# Avg OG
ogcusts1 = [returns_agg.loc[ts1 & (returns_agg['source'] == supl) & (returns_agg['+/-/0/N'] != 'N') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'O') & (returns_agg['Gr/Nt'] == 'Gr'),'Count'].sum() for supl in answered]
ogcusts2 = [returns_agg.loc[ts2 & (returns_agg['source'] == supl) & (returns_agg['+/-/0/N'] != 'N') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'O') & (returns_agg['Gr/Nt'] == 'Gr'),'Count'].sum() for supl in answered]
ogcusts3 = [returns_agg.loc[ts3 & (returns_agg['source'] == supl) & (returns_agg['+/-/0/N'] != 'N') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'O') & (returns_agg['Gr/Nt'] == 'Gr'),'Count'].sum() for supl in answered]
a81 = [np.divide(a61[i], ogcusts1[i], out = np.zeros_like(a61[i]), where = ogcusts1[i]!=0) for i in range(totsup)]
a82 = [np.divide(a62[i], ogcusts2[i], out = np.zeros_like(a62[i]), where = ogcusts2[i]!=0) for i in range(totsup)]
a83 = [np.divide(a63[i], ogcusts3[i], out = np.zeros_like(a63[i]), where = ogcusts3[i]!=0) for i in range(totsup)]

# Avg ON
oncusts1 = [returns_agg.loc[ts1 & (returns_agg['source'] == supl) & (returns_agg['+/-/0/N'] != 'N') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'O') & (returns_agg['Gr/Nt'] == 'Nt'),'Count'].sum() for supl in answered]
oncusts2 = [returns_agg.loc[ts2 & (returns_agg['source'] == supl) & (returns_agg['+/-/0/N'] != 'N') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'O') & (returns_agg['Gr/Nt'] == 'Nt'),'Count'].sum() for supl in answered]
oncusts3 = [returns_agg.loc[ts3 & (returns_agg['source'] == supl) & (returns_agg['+/-/0/N'] != 'N') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'O') & (returns_agg['Gr/Nt'] == 'Nt'),'Count'].sum() for supl in answered]
a91 = [np.divide(a71[i], oncusts1[i], out = np.zeros_like(a71[i]), where = oncusts1[i]!=0) for i in range(totsup)]
a92 = [np.divide(a72[i], oncusts2[i], out = np.zeros_like(a72[i]), where = oncusts2[i]!=0) for i in range(totsup)]
a93 = [np.divide(a73[i], oncusts3[i], out = np.zeros_like(a73[i]), where = oncusts3[i]!=0) for i in range(totsup)]

## Closed

# +TCG
b11 = [returns_agg.loc[ts1 & (returns_agg['source'] == supl) & (returns_agg['+/-/0/N'] == '+') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'C') & (returns_agg['Gr/Nt'] == 'Gr'),'Value(£)'] for supl in answered]
b12 = [returns_agg.loc[ts2 & (returns_agg['source'] == supl) & (returns_agg['+/-/0/N'] == '+') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'C') & (returns_agg['Gr/Nt'] == 'Gr'),'Value(£)'] for supl in answered]
b13 = [returns_agg.loc[ts3 & (returns_agg['source'] == supl) & (returns_agg['+/-/0/N'] == '+') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'C') & (returns_agg['Gr/Nt'] == 'Gr'),'Value(£)'] for supl in answered]

# +TCN
b21 = [returns_agg.loc[ts1 & (returns_agg['source'] == supl) & (returns_agg['+/-/0/N'] == '+') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'C') & (returns_agg['Gr/Nt'] == 'Nt'),'Value(£)'] for supl in answered]
b22 = [returns_agg.loc[ts2 & (returns_agg['source'] == supl) & (returns_agg['+/-/0/N'] == '+') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'C') & (returns_agg['Gr/Nt'] == 'Nt'),'Value(£)'] for supl in answered]
b23 = [returns_agg.loc[ts3 & (returns_agg['source'] == supl) & (returns_agg['+/-/0/N'] == '+') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'C') & (returns_agg['Gr/Nt'] == 'Nt'),'Value(£)'] for supl in answered]

# -TCG
b31 = [returns_agg.loc[ts1 & (returns_agg['source'] == supl) & (returns_agg['+/-/0/N'] == '-') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'C') & (returns_agg['Gr/Nt'] == 'Gr'),'Value(£)'] for supl in answered]
b32 = [returns_agg.loc[ts2 & (returns_agg['source'] == supl) & (returns_agg['+/-/0/N'] == '-') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'C') & (returns_agg['Gr/Nt'] == 'Gr'),'Value(£)'] for supl in answered]
b33 = [returns_agg.loc[ts3 & (returns_agg['source'] == supl) & (returns_agg['+/-/0/N'] == '-') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'C') & (returns_agg['Gr/Nt'] == 'Gr'),'Value(£)'] for supl in answered]

# -TCN
b41 = [returns_agg.loc[ts1 & (returns_agg['source'] == supl) & (returns_agg['+/-/0/N'] == '-') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'C') & (returns_agg['Gr/Nt'] == 'Nt'),'Value(£)'] for supl in answered]
b42 = [returns_agg.loc[ts2 & (returns_agg['source'] == supl) & (returns_agg['+/-/0/N'] == '-') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'C') & (returns_agg['Gr/Nt'] == 'Nt'),'Value(£)'] for supl in answered]
b43 = [returns_agg.loc[ts3 & (returns_agg['source'] == supl) & (returns_agg['+/-/0/N'] == '-') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'C') & (returns_agg['Gr/Nt'] == 'Nt'),'Value(£)'] for supl in answered]

# Ratio CN
b51 = [np.divide(b21[i], b41[i], out = np.zeros_like(b21[i]), where = b41[i]!=0) for i in range(totsup)]
b52 = [np.divide(b22[i], b42[i], out = np.zeros_like(b22[i]), where = b42[i]!=0) for i in range(totsup)]
b53 = [np.divide(b23[i], b43[i], out = np.zeros_like(b23[i]), where = b43[i]!=0) for i in range(totsup)]

# Sum CG
b61 = [np.add(b11[i], b31[i]) for i in range(totsup)]
b62 = [np.add(b12[i], b32[i]) for i in range(totsup)]
b63 = [np.add(b13[i], b33[i]) for i in range(totsup)]

# Sum CN
b71 = [np.add(b21[i], b41[i]) for i in range(totsup)]
b72 = [np.add(b22[i], b42[i]) for i in range(totsup)]
b73 = [np.add(b23[i], b43[i]) for i in range(totsup)]

# Avg CG
cgcusts1 = [returns_agg.loc[ts1 & (returns_agg['source'] == supl) & (returns_agg['+/-/0/N'] != 'N') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'C') & (returns_agg['Gr/Nt'] == 'Gr'),'Count'].sum() for supl in answered]
cgcusts2 = [returns_agg.loc[ts2 & (returns_agg['source'] == supl) & (returns_agg['+/-/0/N'] != 'N') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'C') & (returns_agg['Gr/Nt'] == 'Gr'),'Count'].sum() for supl in answered]
cgcusts3 = [returns_agg.loc[ts3 & (returns_agg['source'] == supl) & (returns_agg['+/-/0/N'] != 'N') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'C') & (returns_agg['Gr/Nt'] == 'Gr'),'Count'].sum() for supl in answered]
b81 = [np.divide(b61[i], cgcusts1[i], out = np.zeros_like(b61[i]), where = cgcusts1[i]!=0) for i in range(totsup)]
b82 = [np.divide(b62[i], cgcusts2[i], out = np.zeros_like(b62[i]), where = cgcusts2[i]!=0) for i in range(totsup)]
b83 = [np.divide(b63[i], cgcusts3[i], out = np.zeros_like(b63[i]), where = cgcusts3[i]!=0) for i in range(totsup)]

# Avg CN
cncusts1 = [returns_agg.loc[ts1 & (returns_agg['source'] == supl) & (returns_agg['+/-/0/N'] != 'N') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'C') & (returns_agg['Gr/Nt'] == 'Nt'),'Count'].sum() for supl in answered]
cncusts2 = [returns_agg.loc[ts2 & (returns_agg['source'] == supl) & (returns_agg['+/-/0/N'] != 'N') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'C') & (returns_agg['Gr/Nt'] == 'Nt'),'Count'].sum() for supl in answered]
cncusts3 = [returns_agg.loc[ts3 & (returns_agg['source'] == supl) & (returns_agg['+/-/0/N'] != 'N') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'C') & (returns_agg['Gr/Nt'] == 'Nt'),'Count'].sum() for supl in answered]
b91 = [np.divide(b71[i], cncusts1[i], out = np.zeros_like(b71[i]), where = cncusts1[i]!=0) for i in range(totsup)]
b92 = [np.divide(b72[i], cncusts2[i], out = np.zeros_like(b72[i]), where = cncusts2[i]!=0) for i in range(totsup)]
b93 = [np.divide(b73[i], cncusts3[i], out = np.zeros_like(b73[i]), where = cncusts3[i]!=0) for i in range(totsup)]

## LMST

# +TOG by size
c11 = [returns_agg.loc[ts1 & (returns_agg['size'] == lms) & (returns_agg['+/-/0/N'] == '+') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'O') & (returns_agg['Gr/Nt'] == 'Gr'),'Value(£)'] for lms in ['large', 'medium', 'small']]
c12 = [returns_agg.loc[ts2 & (returns_agg['size'] == lms) & (returns_agg['+/-/0/N'] == '+') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'O') & (returns_agg['Gr/Nt'] == 'Gr'),'Value(£)'] for lms in ['large', 'medium', 'small']]
c13 = [returns_agg.loc[ts3 & (returns_agg['size'] == lms) & (returns_agg['+/-/0/N'] == '+') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'O') & (returns_agg['Gr/Nt'] == 'Gr'),'Value(£)'] for lms in ['large', 'medium', 'small']]
# +TCG by size
c14 = [returns_agg.loc[ts1 & (returns_agg['size'] == lms) & (returns_agg['+/-/0/N'] == '+') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'C') & (returns_agg['Gr/Nt'] == 'Gr'),'Value(£)'] for lms in ['large', 'medium', 'small']]
c15 = [returns_agg.loc[ts2 & (returns_agg['size'] == lms) & (returns_agg['+/-/0/N'] == '+') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'C') & (returns_agg['Gr/Nt'] == 'Gr'),'Value(£)'] for lms in ['large', 'medium', 'small']]
c16 = [returns_agg.loc[ts3 & (returns_agg['size'] == lms) & (returns_agg['+/-/0/N'] == '+') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'C') & (returns_agg['Gr/Nt'] == 'Gr'),'Value(£)'] for lms in ['large', 'medium', 'small']]

# +TON by size
c21 = [returns_agg.loc[ts1 & (returns_agg['size'] == lms) & (returns_agg['+/-/0/N'] == '+') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'O') & (returns_agg['Gr/Nt'] == 'Nt'),'Value(£)'] for lms in ['large', 'medium', 'small']]
c22 = [returns_agg.loc[ts2 & (returns_agg['size'] == lms) & (returns_agg['+/-/0/N'] == '+') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'O') & (returns_agg['Gr/Nt'] == 'Nt'),'Value(£)'] for lms in ['large', 'medium', 'small']]
c23 = [returns_agg.loc[ts3 & (returns_agg['size'] == lms) & (returns_agg['+/-/0/N'] == '+') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'O') & (returns_agg['Gr/Nt'] == 'Nt'),'Value(£)'] for lms in ['large', 'medium', 'small']]
# +TCN by size
c24 = [returns_agg.loc[ts1 & (returns_agg['size'] == lms) & (returns_agg['+/-/0/N'] == '+') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'C') & (returns_agg['Gr/Nt'] == 'Nt'),'Value(£)'] for lms in ['large', 'medium', 'small']]
c25 = [returns_agg.loc[ts2 & (returns_agg['size'] == lms) & (returns_agg['+/-/0/N'] == '+') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'C') & (returns_agg['Gr/Nt'] == 'Nt'),'Value(£)'] for lms in ['large', 'medium', 'small']]
c26 = [returns_agg.loc[ts3 & (returns_agg['size'] == lms) & (returns_agg['+/-/0/N'] == '+') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'C') & (returns_agg['Gr/Nt'] == 'Nt'),'Value(£)'] for lms in ['large', 'medium', 'small']]

# -TOG by size
c31 = [returns_agg.loc[ts1 & (returns_agg['size'] == lms) & (returns_agg['+/-/0/N'] == '-') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'O') & (returns_agg['Gr/Nt'] == 'Gr'),'Value(£)'] for lms in ['large', 'medium', 'small']]
c32 = [returns_agg.loc[ts2 & (returns_agg['size'] == lms) & (returns_agg['+/-/0/N'] == '-') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'O') & (returns_agg['Gr/Nt'] == 'Gr'),'Value(£)'] for lms in ['large', 'medium', 'small']]
c33 = [returns_agg.loc[ts3 & (returns_agg['size'] == lms) & (returns_agg['+/-/0/N'] == '-') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'O') & (returns_agg['Gr/Nt'] == 'Gr'),'Value(£)'] for lms in ['large', 'medium', 'small']]
# -TCG by size
c34 = [returns_agg.loc[ts1 & (returns_agg['size'] == lms) & (returns_agg['+/-/0/N'] == '-') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'C') & (returns_agg['Gr/Nt'] == 'Gr'),'Value(£)'] for lms in ['large', 'medium', 'small']]
c35 = [returns_agg.loc[ts2 & (returns_agg['size'] == lms) & (returns_agg['+/-/0/N'] == '-') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'C') & (returns_agg['Gr/Nt'] == 'Gr'),'Value(£)'] for lms in ['large', 'medium', 'small']]
c36 = [returns_agg.loc[ts3 & (returns_agg['size'] == lms) & (returns_agg['+/-/0/N'] == '-') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'C') & (returns_agg['Gr/Nt'] == 'Gr'),'Value(£)'] for lms in ['large', 'medium', 'small']]

# -TON by size
c41 = [returns_agg.loc[ts1 & (returns_agg['size'] == lms) & (returns_agg['+/-/0/N'] == '-') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'O') & (returns_agg['Gr/Nt'] == 'Nt'),'Value(£)'] for lms in ['large', 'medium', 'small']]
c42 = [returns_agg.loc[ts2 & (returns_agg['size'] == lms) & (returns_agg['+/-/0/N'] == '-') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'O') & (returns_agg['Gr/Nt'] == 'Nt'),'Value(£)'] for lms in ['large', 'medium', 'small']]
c43 = [returns_agg.loc[ts3 & (returns_agg['size'] == lms) & (returns_agg['+/-/0/N'] == '-') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'O') & (returns_agg['Gr/Nt'] == 'Nt'),'Value(£)'] for lms in ['large', 'medium', 'small']]
# -TCN by size
c44 = [returns_agg.loc[ts1 & (returns_agg['size'] == lms) & (returns_agg['+/-/0/N'] == '-') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'C') & (returns_agg['Gr/Nt'] == 'Nt'),'Value(£)'] for lms in ['large', 'medium', 'small']]
c45 = [returns_agg.loc[ts2 & (returns_agg['size'] == lms) & (returns_agg['+/-/0/N'] == '-') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'C') & (returns_agg['Gr/Nt'] == 'Nt'),'Value(£)'] for lms in ['large', 'medium', 'small']]
c46 = [returns_agg.loc[ts3 & (returns_agg['size'] == lms) & (returns_agg['+/-/0/N'] == '-') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'C') & (returns_agg['Gr/Nt'] == 'Nt'),'Value(£)'] for lms in ['large', 'medium', 'small']]

# Ratio ON by size
c51 = [np.divide(c21[i], c41[i], out = np.zeros_like(c21[i]), where = c41[i]!=0) for i in range(cat)]
c52 = [np.divide(c22[i], c42[i], out = np.zeros_like(c22[i]), where = c42[i]!=0) for i in range(cat)]
c53 = [np.divide(c23[i], c43[i], out = np.zeros_like(c23[i]), where = c43[i]!=0) for i in range(cat)]
# Ratio CN by size
c54 = [np.divide(c24[i], c44[i], out = np.zeros_like(c24[i]), where = c44[i]!=0) for i in range(cat)]
c55 = [np.divide(c25[i], c45[i], out = np.zeros_like(c25[i]), where = c45[i]!=0) for i in range(cat)]
c56 = [np.divide(c26[i], c46[i], out = np.zeros_like(c26[i]), where = c46[i]!=0) for i in range(cat)]

# Sum OG by size
c61 = [np.add(c11[i], c31[i]) for i in range(cat)]
c62 = [np.add(c12[i], c32[i]) for i in range(cat)]
c63 = [np.add(c13[i], c33[i]) for i in range(cat)]
# Sum CG by size
c64 = [np.add(c14[i], c34[i]) for i in range(cat)]
c65 = [np.add(c15[i], c35[i]) for i in range(cat)]
c66 = [np.add(c16[i], c36[i]) for i in range(cat)]

# Sum ON by size
c71 = [np.add(c21[i], c41[i]) for i in range(cat)]
c72 = [np.add(c22[i], c42[i]) for i in range(cat)]
c73 = [np.add(c23[i], c43[i]) for i in range(cat)]
# Sum CN by size
c74 = [np.add(c24[i], c44[i]) for i in range(cat)]
c75 = [np.add(c25[i], c45[i]) for i in range(cat)]
c76 = [np.add(c26[i], c46[i]) for i in range(cat)]

# Avg OG by size
oglmscusts1 = [returns_agg.loc[ts1 & (returns_agg['size'] == lms) & (returns_agg['+/-/0/N'] != 'N') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'O') & (returns_agg['Gr/Nt'] == 'Gr'),'Count'].sum() for lms in sizes]
oglmscusts2 = [returns_agg.loc[ts2 & (returns_agg['size'] == lms) & (returns_agg['+/-/0/N'] != 'N') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'O') & (returns_agg['Gr/Nt'] == 'Gr'),'Count'].sum() for lms in sizes]
oglmscusts3 = [returns_agg.loc[ts3 & (returns_agg['size'] == lms) & (returns_agg['+/-/0/N'] != 'N') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'O') & (returns_agg['Gr/Nt'] == 'Gr'),'Count'].sum() for lms in sizes]
c81 = [np.divide(c61[i], oglmscusts1[i], out = np.zeros_like(c61[i]), where = oglmscusts1[i]!=0) for i in range(cat)]
c82 = [np.divide(c62[i], oglmscusts2[i], out = np.zeros_like(c62[i]), where = oglmscusts2[i]!=0) for i in range(cat)]
c83 = [np.divide(c63[i], oglmscusts3[i], out = np.zeros_like(c63[i]), where = oglmscusts3[i]!=0) for i in range(cat)]

# Avg CG by size
cglmscusts1 = [returns_agg.loc[ts1 & (returns_agg['size'] == lms) & (returns_agg['+/-/0/N'] != 'N') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'C') & (returns_agg['Gr/Nt'] == 'Gr'),'Count'].sum() for lms in sizes]
cglmscusts2 = [returns_agg.loc[ts2 & (returns_agg['size'] == lms) & (returns_agg['+/-/0/N'] != 'N') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'C') & (returns_agg['Gr/Nt'] == 'Gr'),'Count'].sum() for lms in sizes]
cglmscusts3 = [returns_agg.loc[ts3 & (returns_agg['size'] == lms) & (returns_agg['+/-/0/N'] != 'N') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'C') & (returns_agg['Gr/Nt'] == 'Gr'),'Count'].sum() for lms in sizes]
c84 = [np.divide(c64[i], cglmscusts1[i], out = np.zeros_like(c64[i]), where = cglmscusts1[i]!=0) for i in range(cat)]
c85 = [np.divide(c65[i], cglmscusts2[i], out = np.zeros_like(c65[i]), where = cglmscusts2[i]!=0) for i in range(cat)]
c86 = [np.divide(c66[i], cglmscusts3[i], out = np.zeros_like(c66[i]), where = cglmscusts3[i]!=0) for i in range(cat)]

# Avg ON by size
onlmscusts1 = [returns_agg.loc[ts1 & (returns_agg['size'] == lms) & (returns_agg['+/-/0/N'] != 'N') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'O') & (returns_agg['Gr/Nt'] == 'Nt'),'Count'].sum() for lms in sizes]
onlmscusts2 = [returns_agg.loc[ts2 & (returns_agg['size'] == lms) & (returns_agg['+/-/0/N'] != 'N') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'O') & (returns_agg['Gr/Nt'] == 'Nt'),'Count'].sum() for lms in sizes]
onlmscusts3 = [returns_agg.loc[ts3 & (returns_agg['size'] == lms) & (returns_agg['+/-/0/N'] != 'N') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'O') & (returns_agg['Gr/Nt'] == 'Nt'),'Count'].sum() for lms in sizes]
c91 = [np.divide(c71[i], onlmscusts1[i], out = np.zeros_like(c71[i]), where = onlmscusts1[i]!=0) for i in range(cat)]
c92 = [np.divide(c72[i], onlmscusts2[i], out = np.zeros_like(c72[i]), where = onlmscusts2[i]!=0) for i in range(cat)]
c93 = [np.divide(c73[i], onlmscusts3[i], out = np.zeros_like(c73[i]), where = onlmscusts3[i]!=0) for i in range(cat)]

# Avg CN by size
cnlmscusts1 = [returns_agg.loc[ts1 & (returns_agg['size'] == lms) & (returns_agg['+/-/0/N'] != 'N') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'C') & (returns_agg['Gr/Nt'] == 'Nt'),'Count'].sum() for lms in sizes]
cnlmscusts2 = [returns_agg.loc[ts2 & (returns_agg['size'] == lms) & (returns_agg['+/-/0/N'] != 'N') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'C') & (returns_agg['Gr/Nt'] == 'Nt'),'Count'].sum() for lms in sizes]
cnlmscusts3 = [returns_agg.loc[ts3 & (returns_agg['size'] == lms) & (returns_agg['+/-/0/N'] != 'N') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'C') & (returns_agg['Gr/Nt'] == 'Nt'),'Count'].sum() for lms in sizes]
c94 = [np.divide(c74[i], cnlmscusts1[i], out = np.zeros_like(c74[i]), where = cnlmscusts1[i]!=0) for i in range(cat)]
c95 = [np.divide(c75[i], cnlmscusts2[i], out = np.zeros_like(c75[i]), where = cnlmscusts2[i]!=0) for i in range(cat)]
c96 = [np.divide(c76[i], cnlmscusts3[i], out = np.zeros_like(c76[i]), where = cnlmscusts3[i]!=0) for i in range(cat)]

## DF methods
[a11[i].reset_index(drop=True, inplace=True) for i in range(totsup)]
a11=pd.DataFrame(a11, index = answered)
[a12[i].reset_index(drop=True, inplace=True) for i in range(totsup)]
a12=pd.DataFrame(a12, index = answered)
[a13[i].reset_index(drop=True, inplace=True) for i in range(totsup)]
a13=pd.DataFrame(a13, index = answered)
[a21[i].reset_index(drop=True, inplace=True) for i in range(totsup)]
a21=pd.DataFrame(a21, index = answered)
[a22[i].reset_index(drop=True, inplace=True) for i in range(totsup)]
a22=pd.DataFrame(a22, index = answered)
[a23[i].reset_index(drop=True, inplace=True) for i in range(totsup)]
a23=pd.DataFrame(a23, index = answered)
[a31[i].reset_index(drop=True, inplace=True) for i in range(totsup)]
a31=pd.DataFrame(a31, index = answered)
[a32[i].reset_index(drop=True, inplace=True) for i in range(totsup)]
a32=pd.DataFrame(a32, index = answered)
[a33[i].reset_index(drop=True, inplace=True) for i in range(totsup)]
a33=pd.DataFrame(a33, index = answered)
[a41[i].reset_index(drop=True, inplace=True) for i in range(totsup)]
a41=pd.DataFrame(a41, index = answered)
[a42[i].reset_index(drop=True, inplace=True) for i in range(totsup)]
a42=pd.DataFrame(a42, index = answered)
[a43[i].reset_index(drop=True, inplace=True) for i in range(totsup)]
a43=pd.DataFrame(a43, index = answered)
a51=pd.DataFrame(a51, index = answered)
a52=pd.DataFrame(a52, index = answered)
a53=pd.DataFrame(a53, index = answered)
[a61[i].reset_index(drop=True, inplace=True) for i in range(totsup)]
a61=pd.DataFrame(a61, index = answered)
[a62[i].reset_index(drop=True, inplace=True) for i in range(totsup)]
a62=pd.DataFrame(a62, index = answered)
[a63[i].reset_index(drop=True, inplace=True) for i in range(totsup)]
a63=pd.DataFrame(a63, index = answered)
[a71[i].reset_index(drop=True, inplace=True) for i in range(totsup)]
a71=pd.DataFrame(a71, index = answered)
[a72[i].reset_index(drop=True, inplace=True) for i in range(totsup)]
a72=pd.DataFrame(a72, index = answered)
[a73[i].reset_index(drop=True, inplace=True) for i in range(totsup)]
a73=pd.DataFrame(a73, index = answered)
a81=pd.DataFrame(a81, index = answered)
a82=pd.DataFrame(a82, index = answered)
a83=pd.DataFrame(a83, index = answered)
a91=pd.DataFrame(a91, index = answered)
a92=pd.DataFrame(a92, index = answered)
a93=pd.DataFrame(a93, index = answered)

[b11[i].reset_index(drop=True, inplace=True) for i in range(totsup)]
b11=pd.DataFrame(b11, index = answered)
[b12[i].reset_index(drop=True, inplace=True) for i in range(totsup)]
b12=pd.DataFrame(b12, index = answered)
[b13[i].reset_index(drop=True, inplace=True) for i in range(totsup)]
b13=pd.DataFrame(b13, index = answered)
[b21[i].reset_index(drop=True, inplace=True) for i in range(totsup)]
b21=pd.DataFrame(b21, index = answered)
[b22[i].reset_index(drop=True, inplace=True) for i in range(totsup)]
b22=pd.DataFrame(b22, index = answered)
[b23[i].reset_index(drop=True, inplace=True) for i in range(totsup)]
b23=pd.DataFrame(b23, index = answered)
[b31[i].reset_index(drop=True, inplace=True) for i in range(totsup)]
b31=pd.DataFrame(b31, index = answered)
[b32[i].reset_index(drop=True, inplace=True) for i in range(totsup)]
b32=pd.DataFrame(b32, index = answered)
[b33[i].reset_index(drop=True, inplace=True) for i in range(totsup)]
b33=pd.DataFrame(b33, index = answered)
[b41[i].reset_index(drop=True, inplace=True) for i in range(totsup)]
b41=pd.DataFrame(b41, index = answered)
[b42[i].reset_index(drop=True, inplace=True) for i in range(totsup)]
b42=pd.DataFrame(b42, index = answered)
[b43[i].reset_index(drop=True, inplace=True) for i in range(totsup)]
b43=pd.DataFrame(b43, index = answered)
b51=pd.DataFrame(b51, index = answered)
b52=pd.DataFrame(b52, index = answered)
b53=pd.DataFrame(b53, index = answered)
[b61[i].reset_index(drop=True, inplace=True) for i in range(totsup)]
b61=pd.DataFrame(b61, index = answered)
[b62[i].reset_index(drop=True, inplace=True) for i in range(totsup)]
b62=pd.DataFrame(b62, index = answered)
[b63[i].reset_index(drop=True, inplace=True) for i in range(totsup)]
b63=pd.DataFrame(b63, index = answered)
[b71[i].reset_index(drop=True, inplace=True) for i in range(totsup)]
b71=pd.DataFrame(b71, index = answered)
[b72[i].reset_index(drop=True, inplace=True) for i in range(totsup)]
b72=pd.DataFrame(b72, index = answered)
[b73[i].reset_index(drop=True, inplace=True) for i in range(totsup)]
b73=pd.DataFrame(b73, index = answered)
b81=pd.DataFrame(b81, index = answered)
b82=pd.DataFrame(b82, index = answered)
b83=pd.DataFrame(b83, index = answered)
b91=pd.DataFrame(b91, index = answered)
b92=pd.DataFrame(b92, index = answered)
b93=pd.DataFrame(b93, index = answered)

[c11[i].reset_index(drop=True, inplace=True) for i in range(cat)]
c11=pd.DataFrame(c11, index = sizes)
c11=c11.sum(axis=1)
#c11.columns = answered
[c12[i].reset_index(drop=True, inplace=True) for i in range(cat)]
c12=pd.DataFrame(c12, index = sizes)
c12=c12.sum(axis=1)
#c12.columns = answered
[c13[i].reset_index(drop=True, inplace=True) for i in range(cat)]
c13=pd.DataFrame(c13, index = sizes)
c13=c13.sum(axis=1)
#c13.columns = answered
[c14[i].reset_index(drop=True, inplace=True) for i in range(cat)]
c14=pd.DataFrame(c14, index = sizes)
c14=c14.sum(axis=1)
#c14.columns = answered
[c15[i].reset_index(drop=True, inplace=True) for i in range(cat)]
c15=pd.DataFrame(c15, index = sizes)
c15=c15.sum(axis=1)
#c15.columns = answered
[c16[i].reset_index(drop=True, inplace=True) for i in range(cat)]
c16=pd.DataFrame(c16, index = sizes)
c16=c16.sum(axis=1)
#c16.columns = answered

[c21[i].reset_index(drop=True, inplace=True) for i in range(cat)]
c21=pd.DataFrame(c21, index = sizes)
c21=c21.sum(axis=1)
#c21.columns = answered
[c22[i].reset_index(drop=True, inplace=True) for i in range(cat)]
c22=pd.DataFrame(c22, index = sizes)
c22=c22.sum(axis=1)
#c22.columns = answered
[c23[i].reset_index(drop=True, inplace=True) for i in range(cat)]
c23=pd.DataFrame(c23, index = sizes)
c23=c23.sum(axis=1)
#c23.columns = answered
[c24[i].reset_index(drop=True, inplace=True) for i in range(cat)]
c24=pd.DataFrame(c24, index = sizes)
c24=c24.sum(axis=1)
#c24.columns = answered
[c25[i].reset_index(drop=True, inplace=True) for i in range(cat)]
c25=pd.DataFrame(c25, index = sizes)
c25=c25.sum(axis=1)
#c25.columns = answered
[c26[i].reset_index(drop=True, inplace=True) for i in range(cat)]
c26=pd.DataFrame(c26, index = sizes)
c26=c26.sum(axis=1)
#c26.columns = answered

[c31[i].reset_index(drop=True, inplace=True) for i in range(cat)]
c31=pd.DataFrame(c31, index = sizes)
c31=c31.sum(axis=1)
#c31.columns = answered
[c32[i].reset_index(drop=True, inplace=True) for i in range(cat)]
c32=pd.DataFrame(c32, index = sizes)
c32=c32.sum(axis=1)
#c32.columns = answered
[c33[i].reset_index(drop=True, inplace=True) for i in range(cat)]
c33=pd.DataFrame(c33, index = sizes)
c33=c33.sum(axis=1)
#c33.columns = answered
[c34[i].reset_index(drop=True, inplace=True) for i in range(cat)]
c34=pd.DataFrame(c34, index = sizes)
c34=c34.sum(axis=1)
#c34.columns = answered
[c35[i].reset_index(drop=True, inplace=True) for i in range(cat)]
c35=pd.DataFrame(c35, index = sizes)
c35=c35.sum(axis=1)
#c35.columns = answered
[c36[i].reset_index(drop=True, inplace=True) for i in range(cat)]
c36=pd.DataFrame(c36, index = sizes)
c36=c36.sum(axis=1)
#c36.columns = answered

[c41[i].reset_index(drop=True, inplace=True) for i in range(cat)]
c41=pd.DataFrame(c41, index = sizes)
c41=c41.sum(axis=1)
#c41.columns = answered
[c42[i].reset_index(drop=True, inplace=True) for i in range(cat)]
c42=pd.DataFrame(c42, index = sizes)
c42=c42.sum(axis=1)
#c42.columns = answered
[c43[i].reset_index(drop=True, inplace=True) for i in range(cat)]
c43=pd.DataFrame(c43, index = sizes)
c43=c43.sum(axis=1)
#c43.columns = answered
[c44[i].reset_index(drop=True, inplace=True) for i in range(cat)]
c44=pd.DataFrame(c44, index = sizes)
c44=c44.sum(axis=1)
#c44.columns = answered
[c45[i].reset_index(drop=True, inplace=True) for i in range(cat)]
c45=pd.DataFrame(c45, index = sizes)
c45=c45.sum(axis=1)
#c45.columns = answered
[c46[i].reset_index(drop=True, inplace=True) for i in range(cat)]
c46=pd.DataFrame(c46, index = sizes)
c46=c46.sum(axis=1)
#c46.columns = answered

c51 = c21/c41 #pd.DataFrame(c51, index = answered)
c52 = c22/c42 #pd.DataFrame(c52, index = answered)
c53 = c23/c43 #pd.DataFrame(c53, index = answered)
c54 = c24/c44
c55 = c25/c45
c56 = c26/c46

c61 = c11+c31
c62 = c12+c32
c63 = c13+c33
c64 = c14+c34
c65 = c15+c35
c66 = c16+c36

c71 = c21+c41
c72 = c22+c42
c73 = c23+c43
c74 = c24+c44
c75 = c25+c45
c76 = c26+c46

c81 = c61/oglmscusts1
c82 = c62/oglmscusts1
c83 = c63/oglmscusts1
c84 = c64/cglmscusts1
c85 = c65/cglmscusts1
c86 = c66/cglmscusts1

c91 = c71/onlmscusts1
c92 = c72/onlmscusts1
c93 = c73/onlmscusts1
c94 = c74/cnlmscusts1
c95 = c75/cnlmscusts1
c96 = c76/cnlmscusts1

## Outliers

# Empirical Rule
#a11[np.abs(stats.zscore(a11)) > 1] # 68.27 %
#a11[np.abs(stats.zscore(a11)) > 2] # 95.45 % or IQR x 1.5 boxplot / minor outlier
#a11[np.abs(stats.zscore(a11)) > 3] # 99.73 % outlier
#a11[np.abs(stats.zscore(a11)) > 4] # 99.99 % or IQR x 3 major / extreme outlier
def z2outlier(df):
    return df[np.abs(stats.zscore(df)) > 2]

aoutliers=[]

if not(z2outlier(a11).empty): aoutliers.append(['a11', z2outlier(a11).index])
if not(z2outlier(a12).empty): aoutliers.append(['a12', z2outlier(a12).index])
if not(z2outlier(a13).empty): aoutliers.append(['a13', z2outlier(a13).index])
if not(z2outlier(a21).empty): aoutliers.append(['a21', z2outlier(a21).index])
if not(z2outlier(a22).empty): aoutliers.append(['a22', z2outlier(a22).index])
if not(z2outlier(a23).empty): aoutliers.append(['a23', z2outlier(a23).index])
if not(z2outlier(a31).empty): aoutliers.append(['a31', z2outlier(a31).index])
if not(z2outlier(a32).empty): aoutliers.append(['a32', z2outlier(a32).index])
if not(z2outlier(a33).empty): aoutliers.append(['a33', z2outlier(a33).index])
if not(z2outlier(a41).empty): aoutliers.append(['a41', z2outlier(a41).index])
if not(z2outlier(a42).empty): aoutliers.append(['a42', z2outlier(a42).index])
if not(z2outlier(a43).empty): aoutliers.append(['a43', z2outlier(a43).index])
if not(z2outlier(a51).empty): aoutliers.append(['a51', z2outlier(a51).index]) # Bulb
if not(z2outlier(a52).empty): aoutliers.append(['a52', z2outlier(a52).index]) # Bulb
if not(z2outlier(a53).empty): aoutliers.append(['a53', z2outlier(a53).index]) # Bulb
if not(z2outlier(a61).empty): aoutliers.append(['a61', z2outlier(a61).index])
if not(z2outlier(a62).empty): aoutliers.append(['a62', z2outlier(a62).index])
if not(z2outlier(a63).empty): aoutliers.append(['a63', z2outlier(a63).index])
if not(z2outlier(a71).empty): aoutliers.append(['a71', z2outlier(a71).index])
if not(z2outlier(a72).empty): aoutliers.append(['a72', z2outlier(a72).index])
if not(z2outlier(a73).empty): aoutliers.append(['a73', z2outlier(a73).index])
if not(z2outlier(a81).empty): aoutliers.append(['a81', z2outlier(a81).index]) # Bulb
if not(z2outlier(a82).empty): aoutliers.append(['a82', z2outlier(a82).index]) # Bulb
if not(z2outlier(a83).empty): aoutliers.append(['a83', z2outlier(a83).index]) # Bulb
if not(z2outlier(a91).empty): aoutliers.append(['a91', z2outlier(a91).index]) # Bulb
if not(z2outlier(a92).empty): aoutliers.append(['a92', z2outlier(a92).index]) # Bulb
if not(z2outlier(a93).empty): aoutliers.append(['a93', z2outlier(a93).index]) # Bulb

boutliers=[]

if not(z2outlier(b11).empty): boutliers.append(['b11', z2outlier(b11).index])
if not(z2outlier(b12).empty): boutliers.append(['b12', z2outlier(b12).index])
if not(z2outlier(b13).empty): boutliers.append(['b13', z2outlier(b13).index])
if not(z2outlier(b21).empty): boutliers.append(['b21', z2outlier(b21).index])
if not(z2outlier(b22).empty): boutliers.append(['b22', z2outlier(b22).index])
if not(z2outlier(b23).empty): boutliers.append(['b23', z2outlier(b23).index])
if not(z2outlier(b31).empty): boutliers.append(['b31', z2outlier(b31).index])
if not(z2outlier(b32).empty): boutliers.append(['b32', z2outlier(b32).index])
if not(z2outlier(b33).empty): boutliers.append(['b33', z2outlier(b33).index])
if not(z2outlier(b41).empty): boutliers.append(['b41', z2outlier(b41).index])
if not(z2outlier(b42).empty): boutliers.append(['b42', z2outlier(b42).index])
if not(z2outlier(b43).empty): boutliers.append(['b43', z2outlier(b43).index])
if not(z2outlier(b51).empty): boutliers.append(['b51', z2outlier(b51).index]) # Bulb
if not(z2outlier(b52).empty): boutliers.append(['b52', z2outlier(b52).index]) # Bulb
if not(z2outlier(b53).empty): boutliers.append(['b53', z2outlier(b53).index]) # Bulb
if not(z2outlier(b61).empty): boutliers.append(['b61', z2outlier(b61).index])
if not(z2outlier(b62).empty): boutliers.append(['b62', z2outlier(b62).index])
if not(z2outlier(b63).empty): boutliers.append(['b63', z2outlier(b63).index])
if not(z2outlier(b71).empty): boutliers.append(['b71', z2outlier(b71).index])
if not(z2outlier(b72).empty): boutliers.append(['b72', z2outlier(b72).index])
if not(z2outlier(b73).empty): boutliers.append(['b73', z2outlier(b73).index])
if not(z2outlier(b81).empty): boutliers.append(['b81', z2outlier(b81).index]) # Bulb
if not(z2outlier(b82).empty): boutliers.append(['b82', z2outlier(b82).index]) # Bulb
if not(z2outlier(b83).empty): boutliers.append(['b83', z2outlier(b83).index]) # Bulb
if not(z2outlier(b91).empty): boutliers.append(['b91', z2outlier(b91).index]) # Bulb
if not(z2outlier(b92).empty): boutliers.append(['b92', z2outlier(b92).index]) # Bulb
if not(z2outlier(b93).empty): boutliers.append(['b93', z2outlier(b93).index]) # Bulb

coutliers = []

if not(z2outlier(c11).empty): coutliers.append(['c11', z2outlier(c11).index])
if not(z2outlier(c12).empty): coutliers.append(['c12', z2outlier(c12).index])
if not(z2outlier(c13).empty): coutliers.append(['c13', z2outlier(c13).index])
if not(z2outlier(c14).empty): coutliers.append(['c14', z2outlier(c14).index])
if not(z2outlier(c15).empty): coutliers.append(['c15', z2outlier(c15).index])
if not(z2outlier(c16).empty): coutliers.append(['c16', z2outlier(c16).index])
if not(z2outlier(c21).empty): coutliers.append(['c21', z2outlier(c21).index])
if not(z2outlier(c22).empty): coutliers.append(['c22', z2outlier(c22).index])
if not(z2outlier(c23).empty): coutliers.append(['c23', z2outlier(c23).index])
if not(z2outlier(c24).empty): coutliers.append(['c24', z2outlier(c24).index])
if not(z2outlier(c25).empty): coutliers.append(['c25', z2outlier(c25).index])
if not(z2outlier(c26).empty): coutliers.append(['c26', z2outlier(c26).index])
if not(z2outlier(c31).empty): coutliers.append(['c31', z2outlier(c31).index])
if not(z2outlier(c32).empty): coutliers.append(['c32', z2outlier(c32).index])
if not(z2outlier(c33).empty): coutliers.append(['c33', z2outlier(c33).index])
if not(z2outlier(c34).empty): coutliers.append(['c34', z2outlier(c34).index])
if not(z2outlier(c35).empty): coutliers.append(['c35', z2outlier(c35).index])
if not(z2outlier(c36).empty): coutliers.append(['c36', z2outlier(c36).index])
if not(z2outlier(c41).empty): coutliers.append(['c41', z2outlier(c41).index])
if not(z2outlier(c42).empty): coutliers.append(['c42', z2outlier(c42).index])
if not(z2outlier(c43).empty): coutliers.append(['c43', z2outlier(c43).index])
if not(z2outlier(c44).empty): coutliers.append(['c44', z2outlier(c44).index])
if not(z2outlier(c45).empty): coutliers.append(['c45', z2outlier(c45).index])
if not(z2outlier(c46).empty): coutliers.append(['c46', z2outlier(c46).index])
if not(z2outlier(c51).empty): coutliers.append(['c51', z2outlier(c51).index])
if not(z2outlier(c52).empty): coutliers.append(['c52', z2outlier(c52).index])
if not(z2outlier(c53).empty): coutliers.append(['c53', z2outlier(c53).index])
if not(z2outlier(c54).empty): coutliers.append(['c54', z2outlier(c54).index])
if not(z2outlier(c55).empty): coutliers.append(['c55', z2outlier(c55).index])
if not(z2outlier(c56).empty): coutliers.append(['c56', z2outlier(c56).index])
if not(z2outlier(c61).empty): coutliers.append(['c61', z2outlier(c61).index])
if not(z2outlier(c62).empty): coutliers.append(['c62', z2outlier(c62).index])
if not(z2outlier(c63).empty): coutliers.append(['c63', z2outlier(c63).index])
if not(z2outlier(c64).empty): coutliers.append(['c64', z2outlier(c64).index])
if not(z2outlier(c65).empty): coutliers.append(['c65', z2outlier(c65).index])
if not(z2outlier(c66).empty): coutliers.append(['c66', z2outlier(c66).index])
if not(z2outlier(c71).empty): coutliers.append(['c71', z2outlier(c71).index])
if not(z2outlier(c72).empty): coutliers.append(['c72', z2outlier(c72).index])
if not(z2outlier(c73).empty): coutliers.append(['c73', z2outlier(c73).index])
if not(z2outlier(c74).empty): coutliers.append(['c74', z2outlier(c74).index])
if not(z2outlier(c75).empty): coutliers.append(['c75', z2outlier(c75).index])
if not(z2outlier(c76).empty): coutliers.append(['c76', z2outlier(c76).index])
if not(z2outlier(c81).empty): coutliers.append(['c81', z2outlier(c81).index])
if not(z2outlier(c82).empty): coutliers.append(['c82', z2outlier(c82).index])
if not(z2outlier(c83).empty): coutliers.append(['c83', z2outlier(c83).index])
if not(z2outlier(c84).empty): coutliers.append(['c84', z2outlier(c84).index])
if not(z2outlier(c85).empty): coutliers.append(['c85', z2outlier(c85).index])
if not(z2outlier(c86).empty): coutliers.append(['c86', z2outlier(c86).index])
if not(z2outlier(c91).empty): coutliers.append(['c91', z2outlier(c91).index])
if not(z2outlier(c92).empty): coutliers.append(['c92', z2outlier(c92).index])
if not(z2outlier(c93).empty): coutliers.append(['c93', z2outlier(c93).index])
if not(z2outlier(c94).empty): coutliers.append(['c94', z2outlier(c94).index])
if not(z2outlier(c95).empty): coutliers.append(['c95', z2outlier(c95).index])
if not(z2outlier(c96).empty): coutliers.append(['c96', z2outlier(c96).index])

# MAD rule # 95% within simple MAD x 2.5 or ccMAD x 2
#a11[~a11[0].between((a11.mean() - 2*a11.mad())[0], (a11.mean() + 2*a11.mad())[0])]
def mad2outlier(df):
    return a11[~a11[0].between((a11.mean() - 2*a11.mad())[0], (a11.mean() + 2*a11.mad())[0])]

amoutliers=[]

if not(mad2outlier(a11).empty): amoutliers.append(['a11', mad2outlier(a11).index])
if not(mad2outlier(a12).empty): amoutliers.append(['a12', mad2outlier(a12).index])
if not(mad2outlier(a13).empty): amoutliers.append(['a13', mad2outlier(a13).index])
if not(mad2outlier(a21).empty): amoutliers.append(['a21', mad2outlier(a21).index])
if not(mad2outlier(a22).empty): amoutliers.append(['a22', mad2outlier(a22).index])
if not(mad2outlier(a23).empty): amoutliers.append(['a23', mad2outlier(a23).index])
if not(mad2outlier(a31).empty): amoutliers.append(['a31', mad2outlier(a31).index])
if not(mad2outlier(a32).empty): amoutliers.append(['a32', mad2outlier(a32).index])
if not(mad2outlier(a33).empty): amoutliers.append(['a33', mad2outlier(a33).index])
if not(mad2outlier(a41).empty): amoutliers.append(['a41', mad2outlier(a41).index])
if not(mad2outlier(a42).empty): amoutliers.append(['a42', mad2outlier(a42).index])
if not(mad2outlier(a43).empty): amoutliers.append(['a43', mad2outlier(a43).index])
if not(mad2outlier(a51).empty): amoutliers.append(['a51', mad2outlier(a51).index]) # Bulb
if not(mad2outlier(a52).empty): amoutliers.append(['a52', mad2outlier(a52).index]) # Bulb
if not(mad2outlier(a53).empty): amoutliers.append(['a53', mad2outlier(a53).index]) # Bulb
if not(mad2outlier(a61).empty): amoutliers.append(['a61', mad2outlier(a61).index])
if not(mad2outlier(a62).empty): amoutliers.append(['a62', mad2outlier(a62).index])
if not(mad2outlier(a63).empty): amoutliers.append(['a63', mad2outlier(a63).index])
if not(mad2outlier(a71).empty): amoutliers.append(['a71', mad2outlier(a71).index])
if not(mad2outlier(a72).empty): amoutliers.append(['a72', mad2outlier(a72).index])
if not(mad2outlier(a73).empty): amoutliers.append(['a73', mad2outlier(a73).index])
if not(mad2outlier(a81).empty): amoutliers.append(['a81', mad2outlier(a81).index]) # Bulb
if not(mad2outlier(a82).empty): amoutliers.append(['a82', mad2outlier(a82).index]) # Bulb
if not(mad2outlier(a83).empty): amoutliers.append(['a83', mad2outlier(a83).index]) # Bulb
if not(mad2outlier(a91).empty): amoutliers.append(['a91', mad2outlier(a91).index]) # Bulb
if not(mad2outlier(a92).empty): amoutliers.append(['a92', mad2outlier(a92).index]) # Bulb
if not(mad2outlier(a93).empty): amoutliers.append(['a93', mad2outlier(a93).index]) # Bulb

bmoutliers=[]

if not(mad2outlier(b11).empty): bmoutliers.append(['b11', mad2outlier(b11).index])
if not(mad2outlier(b12).empty): bmoutliers.append(['b12', mad2outlier(b12).index])
if not(mad2outlier(b13).empty): bmoutliers.append(['b13', mad2outlier(b13).index])
if not(mad2outlier(b21).empty): bmoutliers.append(['b21', mad2outlier(b21).index])
if not(mad2outlier(b22).empty): bmoutliers.append(['b22', mad2outlier(b22).index])
if not(mad2outlier(b23).empty): bmoutliers.append(['b23', mad2outlier(b23).index])
if not(mad2outlier(b31).empty): bmoutliers.append(['b31', mad2outlier(b31).index])
if not(mad2outlier(b32).empty): bmoutliers.append(['b32', mad2outlier(b32).index])
if not(mad2outlier(b33).empty): bmoutliers.append(['b33', mad2outlier(b33).index])
if not(mad2outlier(b41).empty): bmoutliers.append(['b41', mad2outlier(b41).index])
if not(mad2outlier(b42).empty): bmoutliers.append(['b42', mad2outlier(b42).index])
if not(mad2outlier(b43).empty): bmoutliers.append(['b43', mad2outlier(b43).index])
if not(mad2outlier(b51).empty): bmoutliers.append(['b51', mad2outlier(b51).index]) # Bulb
if not(mad2outlier(b52).empty): bmoutliers.append(['b52', mad2outlier(b52).index]) # Bulb
if not(mad2outlier(b53).empty): bmoutliers.append(['b53', mad2outlier(b53).index]) # Bulb
if not(mad2outlier(b61).empty): bmoutliers.append(['b61', mad2outlier(b61).index])
if not(mad2outlier(b62).empty): bmoutliers.append(['b62', mad2outlier(b62).index])
if not(mad2outlier(b63).empty): bmoutliers.append(['b63', mad2outlier(b63).index])
if not(mad2outlier(b71).empty): bmoutliers.append(['b71', mad2outlier(b71).index])
if not(mad2outlier(b72).empty): bmoutliers.append(['b72', mad2outlier(b72).index])
if not(mad2outlier(b73).empty): bmoutliers.append(['b73', mad2outlier(b73).index])
if not(mad2outlier(b81).empty): bmoutliers.append(['b81', mad2outlier(b81).index]) # Bulb
if not(mad2outlier(b82).empty): bmoutliers.append(['b82', mad2outlier(b82).index]) # Bulb
if not(mad2outlier(b83).empty): bmoutliers.append(['b83', mad2outlier(b83).index]) # Bulb
if not(mad2outlier(b91).empty): bmoutliers.append(['b91', mad2outlier(b91).index]) # Bulb
if not(mad2outlier(b92).empty): bmoutliers.append(['b92', mad2outlier(b92).index]) # Bulb
if not(mad2outlier(b93).empty): bmoutliers.append(['b93', mad2outlier(b93).index]) # Bulb

cmoutliers = []

if not(mad2outlier(c11).empty): cmoutliers.append(['c11', mad2outlier(c11).index])
if not(mad2outlier(c12).empty): cmoutliers.append(['c12', mad2outlier(c12).index])
if not(mad2outlier(c13).empty): cmoutliers.append(['c13', mad2outlier(c13).index])
if not(mad2outlier(c14).empty): cmoutliers.append(['c14', mad2outlier(c14).index])
if not(mad2outlier(c15).empty): cmoutliers.append(['c15', mad2outlier(c15).index])
if not(mad2outlier(c16).empty): cmoutliers.append(['c16', mad2outlier(c16).index])
if not(mad2outlier(c21).empty): cmoutliers.append(['c21', mad2outlier(c21).index])
if not(mad2outlier(c22).empty): cmoutliers.append(['c22', mad2outlier(c22).index])
if not(mad2outlier(c23).empty): cmoutliers.append(['c23', mad2outlier(c23).index])
if not(mad2outlier(c24).empty): cmoutliers.append(['c24', mad2outlier(c24).index])
if not(mad2outlier(c25).empty): cmoutliers.append(['c25', mad2outlier(c25).index])
if not(mad2outlier(c26).empty): cmoutliers.append(['c26', mad2outlier(c26).index])
if not(mad2outlier(c31).empty): cmoutliers.append(['c31', mad2outlier(c31).index])
if not(mad2outlier(c32).empty): cmoutliers.append(['c32', mad2outlier(c32).index])
if not(mad2outlier(c33).empty): cmoutliers.append(['c33', mad2outlier(c33).index])
if not(mad2outlier(c34).empty): cmoutliers.append(['c34', mad2outlier(c34).index])
if not(mad2outlier(c35).empty): cmoutliers.append(['c35', mad2outlier(c35).index])
if not(mad2outlier(c36).empty): cmoutliers.append(['c36', mad2outlier(c36).index])
if not(mad2outlier(c41).empty): cmoutliers.append(['c41', mad2outlier(c41).index])
if not(mad2outlier(c42).empty): cmoutliers.append(['c42', mad2outlier(c42).index])
if not(mad2outlier(c43).empty): cmoutliers.append(['c43', mad2outlier(c43).index])
if not(mad2outlier(c44).empty): cmoutliers.append(['c44', mad2outlier(c44).index])
if not(mad2outlier(c45).empty): cmoutliers.append(['c45', mad2outlier(c45).index])
if not(mad2outlier(c46).empty): cmoutliers.append(['c46', mad2outlier(c46).index])
if not(mad2outlier(c51).empty): cmoutliers.append(['c51', mad2outlier(c51).index])
if not(mad2outlier(c52).empty): cmoutliers.append(['c52', mad2outlier(c52).index])
if not(mad2outlier(c53).empty): cmoutliers.append(['c53', mad2outlier(c53).index])
if not(mad2outlier(c54).empty): cmoutliers.append(['c54', mad2outlier(c54).index])
if not(mad2outlier(c55).empty): cmoutliers.append(['c55', mad2outlier(c55).index])
if not(mad2outlier(c56).empty): cmoutliers.append(['c56', mad2outlier(c56).index])
if not(mad2outlier(c61).empty): cmoutliers.append(['c61', mad2outlier(c61).index])
if not(mad2outlier(c62).empty): cmoutliers.append(['c62', mad2outlier(c62).index])
if not(mad2outlier(c63).empty): cmoutliers.append(['c63', mad2outlier(c63).index])
if not(mad2outlier(c64).empty): cmoutliers.append(['c64', mad2outlier(c64).index])
if not(mad2outlier(c65).empty): cmoutliers.append(['c65', mad2outlier(c65).index])
if not(mad2outlier(c66).empty): cmoutliers.append(['c66', mad2outlier(c66).index])
if not(mad2outlier(c71).empty): cmoutliers.append(['c71', mad2outlier(c71).index])
if not(mad2outlier(c72).empty): cmoutliers.append(['c72', mad2outlier(c72).index])
if not(mad2outlier(c73).empty): cmoutliers.append(['c73', mad2outlier(c73).index])
if not(mad2outlier(c74).empty): cmoutliers.append(['c74', mad2outlier(c74).index])
if not(mad2outlier(c75).empty): cmoutliers.append(['c75', mad2outlier(c75).index])
if not(mad2outlier(c76).empty): cmoutliers.append(['c76', mad2outlier(c76).index])
if not(mad2outlier(c81).empty): cmoutliers.append(['c81', mad2outlier(c81).index])
if not(mad2outlier(c82).empty): cmoutliers.append(['c82', mad2outlier(c82).index])
if not(mad2outlier(c83).empty): cmoutliers.append(['c83', mad2outlier(c83).index])
if not(mad2outlier(c84).empty): cmoutliers.append(['c84', mad2outlier(c84).index])
if not(mad2outlier(c85).empty): cmoutliers.append(['c85', mad2outlier(c85).index])
if not(mad2outlier(c86).empty): cmoutliers.append(['c86', mad2outlier(c86).index])
if not(mad2outlier(c91).empty): cmoutliers.append(['c91', mad2outlier(c91).index])
if not(mad2outlier(c92).empty): cmoutliers.append(['c92', mad2outlier(c92).index])
if not(mad2outlier(c93).empty): cmoutliers.append(['c93', mad2outlier(c93).index])
if not(mad2outlier(c94).empty): cmoutliers.append(['c94', mad2outlier(c94).index])
if not(mad2outlier(c95).empty): cmoutliers.append(['c95', mad2outlier(c95).index])
if not(mad2outlier(c96).empty): cmoutliers.append(['c96', mad2outlier(c96).index])

## Industry Totals

#totlms1 = returns_agg.loc[ts1 & (returns_agg['+/-/0/N'] == '+') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'O') & (returns_agg['Gr/Nt'] == 'Gr'),['Value(£)', 'size']].groupby('size').count().T.reset_index(drop=True).T
#totlms2 = returns_agg.loc[ts2 & (returns_agg['+/-/0/N'] == '+') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'O') & (returns_agg['Gr/Nt'] == 'Gr'),['Value(£)', 'size']].groupby('size').count().T.reset_index(drop=True).T
#totlms3 = returns_agg.loc[ts3 & (returns_agg['+/-/0/N'] == '+') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'O') & (returns_agg['Gr/Nt'] == 'Gr'),['Value(£)', 'size']].groupby('size').count().T.reset_index(drop=True).T

# +TOG
e11 = returns_agg.loc[ts1 & (returns_agg['+/-/0/N'] == '+') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'O') & (returns_agg['Gr/Nt'] == 'Gr'),'Value(£)'].sum()
e12 = returns_agg.loc[ts2 & (returns_agg['+/-/0/N'] == '+') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'O') & (returns_agg['Gr/Nt'] == 'Gr'),'Value(£)'].sum()
e13 = returns_agg.loc[ts3 & (returns_agg['+/-/0/N'] == '+') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'O') & (returns_agg['Gr/Nt'] == 'Gr'),'Value(£)'].sum()

# +TCG
f11 = returns_agg.loc[ts1 & (returns_agg['+/-/0/N'] == '+') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'C') & (returns_agg['Gr/Nt'] == 'Gr'),'Value(£)'].sum()
f12 = returns_agg.loc[ts2 & (returns_agg['+/-/0/N'] == '+') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'C') & (returns_agg['Gr/Nt'] == 'Gr'),'Value(£)'].sum()
f13 = returns_agg.loc[ts3 & (returns_agg['+/-/0/N'] == '+') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'C') & (returns_agg['Gr/Nt'] == 'Gr'),'Value(£)'].sum()

# +TON
e21 = returns_agg.loc[ts1 & (returns_agg['+/-/0/N'] == '+') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'O') & (returns_agg['Gr/Nt'] == 'Nt'),'Value(£)'].sum()
e22 = returns_agg.loc[ts2 & (returns_agg['+/-/0/N'] == '+') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'O') & (returns_agg['Gr/Nt'] == 'Nt'),'Value(£)'].sum()
e23 = returns_agg.loc[ts3 & (returns_agg['+/-/0/N'] == '+') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'O') & (returns_agg['Gr/Nt'] == 'Nt'),'Value(£)'].sum()

# +TCN
f21 = returns_agg.loc[ts1 & (returns_agg['+/-/0/N'] == '+') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'C') & (returns_agg['Gr/Nt'] == 'Nt'),'Value(£)'].sum()
f22 = returns_agg.loc[ts2 & (returns_agg['+/-/0/N'] == '+') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'C') & (returns_agg['Gr/Nt'] == 'Nt'),'Value(£)'].sum()
f23 = returns_agg.loc[ts3 & (returns_agg['+/-/0/N'] == '+') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'C') & (returns_agg['Gr/Nt'] == 'Nt'),'Value(£)'].sum()

# -TOG
e31 = returns_agg.loc[ts1 & (returns_agg['+/-/0/N'] == '-') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'O') & (returns_agg['Gr/Nt'] == 'Gr'),'Value(£)'].sum()
e32 = returns_agg.loc[ts2 & (returns_agg['+/-/0/N'] == '-') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'O') & (returns_agg['Gr/Nt'] == 'Gr'),'Value(£)'].sum()
e33 = returns_agg.loc[ts3 & (returns_agg['+/-/0/N'] == '-') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'O') & (returns_agg['Gr/Nt'] == 'Gr'),'Value(£)'].sum()

# -TCG
f31 = returns_agg.loc[ts1 & (returns_agg['+/-/0/N'] == '-') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'C') & (returns_agg['Gr/Nt'] == 'Gr'),'Value(£)'].sum()
f32 = returns_agg.loc[ts2 & (returns_agg['+/-/0/N'] == '-') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'C') & (returns_agg['Gr/Nt'] == 'Gr'),'Value(£)'].sum()
f33 = returns_agg.loc[ts3 & (returns_agg['+/-/0/N'] == '-') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'C') & (returns_agg['Gr/Nt'] == 'Gr'),'Value(£)'].sum()

# -TON
e41 = returns_agg.loc[ts1 & (returns_agg['+/-/0/N'] == '-') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'O') & (returns_agg['Gr/Nt'] == 'Nt'),'Value(£)'].sum()
e42 = returns_agg.loc[ts2 & (returns_agg['+/-/0/N'] == '-') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'O') & (returns_agg['Gr/Nt'] == 'Nt'),'Value(£)'].sum()
e43 = returns_agg.loc[ts3 & (returns_agg['+/-/0/N'] == '-') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'O') & (returns_agg['Gr/Nt'] == 'Nt'),'Value(£)'].sum()

# -TCN
f41 = returns_agg.loc[ts1 & (returns_agg['+/-/0/N'] == '-') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'C') & (returns_agg['Gr/Nt'] == 'Nt'),'Value(£)'].sum()
f42 = returns_agg.loc[ts2 & (returns_agg['+/-/0/N'] == '-') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'C') & (returns_agg['Gr/Nt'] == 'Nt'),'Value(£)'].sum()
f43 = returns_agg.loc[ts3 & (returns_agg['+/-/0/N'] == '-') & (returns_agg['E/G/DF/T'] == 'T') & (returns_agg['O/C'] == 'C') & (returns_agg['Gr/Nt'] == 'Nt'),'Value(£)'].sum()

# Sum OG
e61 = np.add(e11, e31)
e62 = np.add(e12, e32)
e63 = np.add(e13, e33)

# Sum CG
f61 = np.add(f11, f31)
f62 = np.add(f12, f32)
f63 = np.add(f13, f33)

# Sum ON
e71 = np.add(e21, e41)
e72 = np.add(e22, e42)
e73 = np.add(e23, e43)

# Sum CN
f71 = np.add(f21, f41)
f72 = np.add(f22, f42)
f73 = np.add(f23, f43)

## Output

q1 = pd.DataFrame(['==== Q1 Positive Gross ===='])
q2 = pd.DataFrame(['==== Q2 Positive Net ===='])
q3 = pd.DataFrame(['==== Q3 Negative Gross ===='])
q4 = pd.DataFrame(['==== Q4 Negative Net ===='])
q5 = pd.DataFrame(['==== Q5 Ratio Net ===='])
q6 = pd.DataFrame(['==== Q6 Sum Gross ===='])
q7 = pd.DataFrame(['==== Q7 Sum Net ===='])
q8 = pd.DataFrame(['==== Q8 Average Gross ===='])
q9 = pd.DataFrame(['==== Q9 Average Net ===='])
t1 = pd.DataFrame(['== October 2017 =='])
t2 = pd.DataFrame(['== April 2018 =='])
t3 = pd.DataFrame(['== October 2018 =='])
oo = pd.DataFrame(['## Open ##'])
cc = pd.DataFrame(['## Closed ##'])

aa = pd.concat([q1, t1, a11, t2, a12, t3, a13, q2, t1, a21, t2, a22, t3, a23, q3, t1, a31, t2, a32, t3, a33, q4, t1, a41, t2, a42, t3, a43, q5, t1, a51, t2, a52, t3, a53, q6, t1, a61, t2, a62, t3, a63, q7, t1, a71, t2, a72, t3, a73, q8, t1, a81, t2, a82, t3, a83, q9, t1, a91, t2, a92, t3, a93])
round(aa,2).to_csv(output_dir + 'Section1 Open.csv')
bb = pd.concat([q1, t1, b11, t2, b12, t3, b13, q2, t1, b21, t2, b22, t3, b23, q3, t1, b31, t2, b32, t3, b33, q4, t1, b41, t2, b42, t3, b43, q5, t1, b51, t2, b52, t3, b53, q6, t1, b61, t2, b62, t3, b63, q7, t1, b71, t2, b72, t3, b73, q8, t1, b81, t2, b82, t3, b83, q9, t1, b91, t2, b92, t3, b93])
round(bb,2).to_csv(output_dir + 'Section2 Closed.csv')
ccc = pd.concat([q1, oo, t1, c11, t2, c12, t3, c13, cc, t1, c14, t2, c15, t3, c16, q2, oo, t1, c21, t2, c22, t3, c23, cc, t1, c24, t2, c25, t3, c26, q3, oo, t1, c31, t2, c32, t3, c33, cc, t1, c34, t2, c35, t3, c36, q4, oo, t1, c41, t2, c42, t3, c43, cc, t1, c44, t2, c45, t3, c46, q5, oo, t1, c51, t2, c52, t3, c53, cc, t1, c54, t2, c55, t3, c56, q6, oo, t1, c61, t2, c62, t3, c63, cc, t1, c64, t2, c65, t3, c66, q7, oo, t1, c71, t2, c72, t3, c73, cc, t1, c74, t2, c75, t3, c76, q8, oo, t1, c81, t2, c82, t3, c83, cc, t1, c84, t2, c85, t3, c86, q9, oo, t1, c91, t2, c92, t3, c93, cc, t1, c94, t2, c95, t3, c96])
round(ccc,2).to_csv(output_dir + 'Section3 LMS.csv')

olza = pd.DataFrame(['==== a outliers > z=2 +- 2 x sd ===='])
olzb = pd.DataFrame(['==== b outliers > z=2 +- 2 x sd===='])
olzc = pd.DataFrame(['==== c outliers > z=2 +- 2 x sd ===='])
olma = pd.DataFrame(['==== a outliers +- 2 adj mad ===='])
olmb = pd.DataFrame(['==== b outliers +- 2 adj mad ===='])
olmc = pd.DataFrame(['==== c outliers +- 2 adj mad ===='])

ol = pd.concat([olza, pd.DataFrame(aoutliers), olzb, pd.DataFrame(boutliers), olzc, pd.DataFrame(coutliers), olma, pd.DataFrame(amoutliers), olmb, pd.DataFrame(bmoutliers), olmc, pd.DataFrame(cmoutliers)])
ol.to_csv(output_dir + 'Section4 Outliers.csv')

ef = pd.concat([q1, oo, pd.Series(e11), pd.Series(e12), pd.Series(e13), cc, pd.Series(f11), pd.Series(f12), pd.Series(f13), q2, oo, pd.Series(e21), pd.Series(e22), pd.Series(e23), cc, pd.Series(f21), pd.Series(f22), pd.Series(f23), q3, oo, pd.Series(e31), pd.Series(e32), pd.Series(e33), cc, pd.Series(f31), pd.Series(f32), pd.Series(f33), q4, oo, pd.Series(e41), pd.Series(e42), pd.Series(e43), cc, pd.Series(f41), pd.Series(f42), pd.Series(f43), q6, oo, pd.Series(e61), pd.Series(e62), pd.Series(e63), cc, pd.Series(f61), pd.Series(f62), pd.Series(f63), q7, oo, pd.Series(e71), pd.Series(e72), pd.Series(e73), cc, pd.Series(f71), pd.Series(f72), pd.Series(f73)])
round(ef,2).to_csv(output_dir + 'Section5 Totals.csv')

## Plots

#x = returns_agg.iloc[:,0].unique() #['17-10-01', '18-04-01', '18-10-01']
#y = [e11, e12, e13]
#z = [f11, f12, f13]
#plt.plot(x,y)
#plt.figure()
#plt.plot(x,z)
#plt.figure()
plt.plot(a11)
#plt.figure()
#plt.plot([a11[0], a21[0], a31[0], a41[0]]) # blue flat is Yo, orange incr is Zeb
print('==== Finished ====')