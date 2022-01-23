# -*- coding: utf-8 -*-
"""
Created on Wed Sep 09 16:54:52 2020

@author: McCabeR
"""

import glob, pandas as pd, copy, numpy as np, matplotlib.pyplot as plt, seaborn as sns # os, datetime as dt
#from ast import literal_eval

sub='11v3'
Lsource = 'K:/User Centred Data Services/Beta/retail_data/covid_19_rfi/New RFI/Download/Leading Indicators/'
Csource = 'K:/User Centred Data Services/Beta/retail_data/covid_19_rfi/New RFI/Download/Complementary Indicators/'
lead_xl_files = glob.glob(Lsource + '*/*.xlsx')
comp_xl_files = glob.glob(Csource + '*/*.xlsx')

L=pd.DataFrame()
C=pd.DataFrame()
rtab, countsp, countone = 0,0,0
spfile = []

print('Processing Leading indicators...')
for num,file in enumerate(lead_xl_files):
    try:
        df = pd.read_excel(file, encoding='unicode_escape')
    except:
        rtab+=1
    df.columns = map(str.lower, df.columns)
    if len(df.columns)==1:
        print('\nOne column in:', num, file.split('/')[7].split('\\')[2], '\n')
        countone+=1
    if ' ' in file.split('/')[7].split('\\')[2]:
        countsp+=1
        spfile.append(file.split('/')[7].split('\\')[2])
    df = df[~df.qnumber.isnull()]
    df['source'] = file.split('/')[7].split('\\')[2]
    #if any(df.source.str.contains('SSE')): continue
    #if any(df.source.str.contains('POWERSHOP')): continue
    df.drop(columns=['supplier','date'], inplace=True)
    df.dropna(how='all', inplace=True, axis='index') # drop empty rows
    df.dropna(how='all', inplace=True, axis='columns') # drop empty columns
    df.rename(columns=lambda x: x.strip(), inplace=True)
    L=L.append(df, sort=True)
    print(num,df.shape)
print('Finished reading in', num+1, 'files')
L.reset_index(inplace=True, drop=True)
print(L.source.nunique())

print('Processing Complementary indicators...')
for num,file in enumerate(comp_xl_files):
    try:
        df = pd.read_excel(file, encoding='unicode_escape')
    except:
        rtab+=1
    df.columns = map(str.lower, df.columns)
    if len(df.columns)==1:
        print('\nOne column in:', num, file.split('/')[7].split('\\')[2], '\n')
        countone+=1
    if ' ' in file.split('/')[7].split('\\')[2]:
        countsp+=1
        spfile.append(file.split('/')[7].split('\\')[2])
    df = df[~df.qnumber.isnull()]
    df['source'] = file.split('/')[7].split('\\')[2]
    #if any(df.source.str.contains('SSE')): continue
    #if any(df.source.str.contains('POWERSHOP')): continue
    df.drop(columns=['supplier','date'], inplace=True)
    df.dropna(how='all', inplace=True, axis='index') # drop empty rows
    df.dropna(how='all', inplace=True, axis='columns') # drop empty columns
    df.rename(columns=lambda x: x.strip(), inplace=True)
    C=C.append(df, sort=True)
    print(num,df.shape)
print('Finished reading in', num+1, 'files')
C.reset_index(inplace=True, drop=True)
print(C.source.nunique())

## Cleaning ##

rtab, countsp, countone # 0,6,0 - 14 when Crown changed 20-2(and Crown) fixes on 16Oct to 20 (525,323) to 36-2BG, 50, 52, 54, 56, 58
spfile # (9,9,6,6) 14x2,11x2

print('No extra L columns:', len(L.columns) == 9)
print('No extra C columns:', len(C.columns) == 9)
list(L.columns) # 9 = 10-2+1, no PShop extras
list(C.columns) # 9

def chkcol(ab, colname):
    print('\n', ab[~ab[colname].isnull()]['supplier name'].nunique(dropna=False),'\n')
    print(ab[~ab[colname].isnull()]['supplier name'].unique(),'\n')
    print(ab[~ab[colname].isnull()].source.unique())
    print('\n', len(ab[~ab[colname].isnull()]))
    print('\n', ab[~ab[colname].isnull()].index)
    print([len(ab[(~ab[colname].isnull())&(ab['supplier name']==sup)].isnull()) for sup in ab[~ab[colname].isnull()]['supplier name'].unique() if type(sup)!=float])

chkcol(L, 'unnamed: 8') # Oct lead 23/11

L.applymap(lambda x: x.strip() if type(x)==str else x)
C.applymap(lambda x: x.strip() if type(x)==str else x)

print('Only three -> two spaced files:', len(pd.Series([spfile[i].split('_')[0] for i in range(len(spfile))]).unique()) == 2) # from 3
pd.Series([spfile[i].split('_')[0] for i in range(len(spfile))]).unique() # CNG, CE, UWH, not CE from 13/11/20

## Data spot check ##

sum(L.value[L['supplier name']=='EON'].notnull()) # 0
sum(L.value[L['supplier name']=='E.ON'].notnull()) # 12..104...181

## Multiple tests ##

def analyse(ab):
    print('\nNon-String Rows:', ab.shape[0] - len(ab.select_dtypes(include='object')))
    input("Press Enter to continue...")
    print('\n# Unique:\n', ab.nunique())
    print('\n...plus NaN:\n', ab.nunique(dropna=False) - ab.nunique())
    input("Press Enter to continue...")
    print('\nUnary Columns:', sum(ab.nunique()==1))
    input("Press Enter to continue...")
    print('\nUnique Columns:', [col for col in ab.columns if ab[col].is_unique])
    input("Press Enter to continue...")
    print('\nContains Nulls:\n', ab.isnull().any())
    input("Press Enter to continue...")
    print('\nMixed Type or Min and Max:')
    for i in range(ab.shape[1]):
        if not pd.Series([type(i) for i in ab.iloc[:,i]]).nunique() == 1: print('<Mixed column>')
        elif ab[ab.columns[i]].nunique() != 0: print('Col:', ab.columns[i], '\nmin:', min(ab.iloc[:,i].dropna()), '\nmax:', max(ab.iloc[:,i].dropna()))
        else: print('<Empty column>')
    input("Press Enter to continue...")
    print('\nInfo:')
    print(ab.info())
    input("Press Enter to continue...")
    print('\nTotal Suppliers:', ab['supplier name'].nunique())

#analyse(L)
#analyse(C)

## Blank suppliers ##

print('No empty L supplier names:', L[L['supplier name'].isnull()].source.nunique() == 0)
print('No empty C supplier names:', C[C['supplier name'].isnull()].source.nunique() == 0)

## Supplier totals and standard names ##

L['supplier name'].append(C['supplier name']).nunique() # 22

## Symbols in values ##

L.value.dtype # float64
C.value.dtype # float64 / not object

## Units ##

L.unit.value_counts(dropna=False) # num
L.source[L.unit.isnull()].nunique()  # 0

C.unit.value_counts(dropna=False) # num and GBP
C.source[C.unit.isnull()].unique() # []

## Values ##

L.value[L.value<0] # []
L.value[pd.to_numeric(L.value, errors='coerce').isnull()].unique() # [nan]
C.value[C.value<0] # []
C.value[C['value'].apply(lambda x: isinstance(x,str))] # 90 rows to []
C.value[C['value'].apply(lambda x: isinstance(x,str))].unique() # 2 values to []
C.source[C['value'].apply(lambda x: isinstance(x,str))].unique() # 3 Haven, 1 Oct to []
C.source[C['value']=='-']#.unique() # Oct 8 x 2 rows to []
C.source[C['value']=='\xa0']#.unique() # Haven 7, 8, 9 x 88 rows to []
len(C.source[(C['value']=='\xa0')&(C.source=='HAVENPOWER_COMPLEMENTARYINDICATORS_01_07_2020.xlsx')]) # 33 to 0
len(C.source[(C['value']=='\xa0')&(C.source=='HAVENPOWER_COMPLEMENTARYINDICATORS_01_08_2020.xlsx')]) # 33 to 0
len(C.source[(C['value']=='\xa0')&(C.source=='HAVENPOWER_COMPLEMENTARYINDICATORS_01_09_2020.xlsx')]) # 22 to 0
len(C.source[(C['value']=='\xa0')&(C.source=='BESUTILITIES_COMPLEMENTARYINDICATORS_01_05_2021.xlsx')]) # 30 to 0

## Questions ##

print('No extra L questions:', len(L['question (linked to market segment)'].unique()) == 13)
print('No extra C questions:', len(C['question (linked to market segment)'].unique()) == 57)

## First plot ##

sorted(L.value[L.qnumber==13][L.value[L.qnumber==13].notnull()])
plt.plot(L.value[L.qnumber==13][L.value[L.qnumber==13].notnull()])

## Date formats ##

L['reporting period start'].unique()
C['reporting period start'].unique()

## Value ranges ##

aval=list(L.value.dropna().unique())
[(i,aval[i]) for i in range(len(aval)) if not aval[i]] # 1 and 0.0
aval2=list(pd.Series(aval).astype(float))
[i for i in range(len(aval)) if aval[i]=='N/a'] # []
[i for i in range(len(aval)) if aval[i]==0.0] # [1]
[i for i in range(len(aval)) if aval[i]==' '] # []
L.source[L.value==' '].unique() # []
aval2.sort()
[L.unit[i] for i in range(len(L)) if L.value[i] in [str(i) for i in aval2[:3]]] # []
bval=list(C.value.dropna().unique())
[(i,bval[i]) for i in range(len(bval)) if not bval[i]] # 1 and 0.0
bval2=list(pd.Series(bval).astype(float))
[i for i in range(len(bval)) if bval[i]=='N/a'] # []
[i for i in range(len(bval)) if bval[i]==0.0] # [1]
[i for i in range(len(bval)) if bval[i]==' '] # []
[i for i in range(len(bval)) if bval[i]=='-'] # [] 2257
C.source[C.value==' '].unique() # []
bval2.sort()
[C.unit[i] for i in range(len(C)) if C.value[i] in [str(i) for i in bval2[:3]]] # []
aval2[::len(aval2)-1] # 0.0 to 373,406.0 to 386,487
bval2[::len(bval2)-1] # 0.0 to 66,562,962 to 70,486,599.0 to 82,498,698 to 93,588,801 to 94,322,381 to 103,070,973 to 105,686,867

## Save files ##

L.to_csv('H:/Cov RFI/cor_Lead'+sub+'FULL.csv', index=False, columns=df.columns)
C.to_csv('H:/Cov RFI/cor_Comp'+sub+'FULL.csv', index=False, columns=df.columns)

## Heat maps ##

sns.set()

Lresp = pd.DataFrame()
for s in L['supplier name'].unique():
    for d in L['reporting period start'].unique():
        if any(L.value[(L['supplier name']==s) & (L['reporting period start']==d)].notnull()): Lresp.loc[s,d]=sum(L.value[(L['supplier name']==s) & (L['reporting period start']==d)].notnull())
lcol = list(pd.to_datetime(Lresp.columns,format='%d/%m/%Y'))
lcol.sort()
#Lresp=Lresp[pd.DatetimeIndex(lcol).strftime('%d/%m/%Y %H:%M:%S')]
Lresp=Lresp[lcol]

Lresp.min().min(), Lresp.max().max()
Lresp[Lresp.max(axis=1)==Lresp.max().max()], Lresp.columns[Lresp.max()==Lresp.max().max()]

fig, ax = plt.subplots(figsize=(20,40))
ax.tick_params(right=True, top=True, labelright=True, labeltop=True)
Lhmap = sns.heatmap(Lresp, annot=True, vmin=0, center=Lresp.max().max()/2, linewidths=.5, cbar_kws = dict(use_gridspec=False,location="top"))
plt.text(0,-12,'Number of non-null values per supplier per submission date for Leading aggregation', fontsize=30)
fig.savefig('H:/Cov RFI/Sub'+sub+'_Lead_heatmap.png')

subLfreq = [Lresp.iloc[i].count() for i in range(len(Lresp))]
pd.Series(subLfreq).value_counts(sort=False) # 1 @ 8 = BES - all 9

Lcount=Lresp.count()
fig = plt.figure(figsize=(10,10))
plt.xticks(np.arange(len(Lcount)), Lcount.index, rotation=45)
plt.xlabel('Submission Date')
plt.ylabel('Number of Suppliers that Responded to L')
plt.title('L Response Rate')
plt.plot(Lcount)
fig.savefig('H:/Cov RFI/Sub'+sub+'_L_rrate.png')

Cresp = pd.DataFrame()
for s in C['supplier name'].unique():
    for d in C['reporting period start'].unique():
        if any(C.value[(C['supplier name']==s) & (C['reporting period start']==d)].notnull()): Cresp.loc[s,d]=sum(C.value[(C['supplier name']==s) & (C['reporting period start']==d)].notnull())
ccol = list(pd.to_datetime(Cresp.columns,format='%d/%m/%Y'))
ccol.sort()
#Cresp=Lresp[pd.DatetimeIndex(lcol).strftime('%d/%m/%Y %H:%M:%S')]
Cresp=Cresp[ccol]

Cresp.min().min(), Cresp.max().max()
Cresp[Cresp.max(axis=1)==Cresp.max().max()], Cresp.columns[Cresp.max()==Cresp.max().max()]

fig, ax = plt.subplots(figsize=(20,40))
ax.tick_params(right=True, top=True, labelright=True, labeltop=True)
Chmap = sns.heatmap(Cresp, annot=True, vmin=0, center=Cresp.max().max()/2, linewidths=.5, cbar_kws = dict(use_gridspec=False,location="top"))
plt.text(0,-12,'Number of non-null values per supplier per submission date for Comp aggregation', fontsize=30)
fig.savefig('H:/Cov RFI/Sub'+sub+'_Comp_heatmap.png')

subCfreq = [Cresp.iloc[i].count() for i in range(len(Cresp))]
pd.Series(subCfreq).value_counts(sort=False) # 1 @ 5 = BES - all 6

Ccount=Cresp.count()
fig = plt.figure(figsize=(10,10))
plt.xticks(np.arange(len(Ccount)), Ccount.index, rotation=45)
plt.xlabel('Submission Date')
plt.ylabel('Number of Suppliers that Responded to C')
plt.title('C Response Rate')
plt.plot(Ccount)
fig.savefig('H:/Cov RFI/Sub'+sub+'_C_rrate.png')

Lresp.index.difference(Cresp.index) # []
Cresp.index.difference(Lresp.index) # []

def PCfail(type, pc):
    a = Lresp.iloc[:,-1][Lresp.iloc[:,-1] < 13*pc]
    b = Cresp.iloc[:,-1][Cresp.iloc[:,-1] < 57*pc]
    if type == 'L': print('\n', len(a), 'had less than', int(pc*100), '% values in the last submission:\n\n', a)
    elif type == 'C': print('\n', len(b), 'had less than', int(pc*100), '% values in the last submission:\n\n', b)
    else: print('Type Error')

PCfail('L', 0.75)
PCfail('C', 0.75)
PCfail('L', 0.5) # OVO, Shell, SSE down to 2s
PCfail('C', 0.5) # Opus, Shell, SSE add Total - O + CNG, Haven

## End Full / Start Partial for EUK ##

skipeuk = pd.Series(['avro energy','contract natural gas','corona','crown energy','gazprom','haven power','opus','sse','total gas and power'])

Lpar=pd.DataFrame()
Cpar=pd.DataFrame()
rtab, countsp, countone, countskip = 0,0,0,0
spfile = []

print('Processing Leading EUK indicators...')
for num,file in enumerate(lead_xl_files):
    try:
        df = pd.read_excel(file, encoding='unicode_escape')
    except:
        rtab+=1
    df.columns = map(str.lower, df.columns)
    if len(df.columns)==1:
        print('\nOne column in:', num, file.split('/')[7].split('\\')[2], '\n')
        countone+=1
    if ' ' in file.split('/')[7].split('\\')[2]:
        countsp+=1
        spfile.append(file.split('/')[7].split('\\')[2])
    df = df[~df.qnumber.isnull()]
    df['source'] = file.split('/')[7].split('\\')[2]
    #if any(df.source.str.contains('SSE')): continue
    #if any(df.source.str.contains('POWERSHOP')): continue
    df.drop(columns=['supplier','date'], inplace=True)
    df.dropna(how='all', inplace=True, axis='index') # drop empty rows
    df.dropna(how='all', inplace=True, axis='columns') # drop empty columns
    df.rename(columns=lambda x: x.strip(), inplace=True)
    if skipeuk.isin([df['supplier name'][0].lower()]).any():
        countskip+=1
    else:
        Lpar=Lpar.append(df, sort=True)
    print(num, df.shape)
print('Finished reading in', num+1, 'files')
Lpar.reset_index(inplace=True, drop=True)
print(Lpar.source.nunique()) # 45 = 15x3 to 150 +14, 178 from 16/4 no hav or opus

print('Processing Complementary EUK indicators...')
for num,file in enumerate(comp_xl_files):
    try:
        df = pd.read_excel(file, encoding='unicode_escape')
    except:
        rtab+=1
    df.columns = map(str.lower, df.columns)
    if len(df.columns)==1:
        print('\nOne column in:', num, file.split('/')[7].split('\\')[2], '\n')
        countone+=1
    if ' ' in file.split('/')[7].split('\\')[2]:
        countsp+=1
        spfile.append(file.split('/')[7].split('\\')[2])
    df = df[~df.qnumber.isnull()]
    df['source'] = file.split('/')[7].split('\\')[2]
    #if any(df.source.str.contains('SSE')): continue
    #if any(df.source.str.contains('POWERSHOP')): continue
    df.drop(columns=['supplier','date'], inplace=True)
    df.dropna(how='all', inplace=True, axis='index') # drop empty rows
    df.dropna(how='all', inplace=True, axis='columns') # drop empty columns
    df.rename(columns=lambda x: x.strip(), inplace=True)
    if skipeuk.isin([df['supplier name'][0].lower()]).any():
        countskip+=1
    else:
        Cpar=Cpar.append(df, sort=True)
    print(num, df.shape)
print('Finished reading in', num+1, 'files')
Cpar.reset_index(inplace=True, drop=True)
print(Cpar.source.nunique()) # 30 = 15x2 to 45 to 90, 114, 126, 138, 150, 179, 186

rtab, countsp, countone, countskip # 0,6,0 to 0,20,0,56 (5+3=8x7) 0,34,0,119 46,207 126 of 48/216, 50/225, 52/234, 54/242, 56/250, 58/258

list(L.columns) # 9 = 10-2+1, no PShop extras
list(C.columns) # 9

L.applymap(lambda x: x.strip() if type(x)==str else x)
C.applymap(lambda x: x.strip() if type(x)==str else x)

#Lpar['supplier name'].nunique() # 13
#Lpar['supplier name'].unique() # no Haven or Opus

Lpar.to_csv('H:/Cov RFI/cor_Lead'+sub+'EUK.csv', index=False, columns=df.columns)
Cpar.to_csv('H:/Cov RFI/cor_Comp'+sub+'EUK.csv', index=False, columns=df.columns)

## End Partial / Start QFiltered for CAB ##

Lcab = copy.copy(L)
Lcab.shape # (286,9) (572,9) (858,9) 1144 1430 1716 2002 2275 2574 2860 3133 ... 3952
Lcab=Lcab[~Lcab.qnumber.isin([3,6,9,12])]
Lcab.shape # (198,9) (396,9) (594,9) 792 990 1188 1386 1575 1782 1980 2169 ... 2736
Lcab.qnumber.unique()

Ccab = copy.copy(C)
Ccab.shape # (1254,9) (2508,9) 3762 5016 6213 7524 ... 11115 12312 13509 14706 15846 16986 18126
Ccab=Ccab[~Ccab.qnumber.isin([3,6,9,12,22,23,26,29,32,35,38,42,46,50])]
Ccab.shape # (946,9) (1892,9) 2838 3784 4687 5676 ... 8385 9288 10191 11094 11954 12814 13674
Ccab.qnumber.unique()

Lcab.to_csv('H:/Cov RFI/cor_Lead'+sub+'CAB.csv', index=False, columns=df.columns)
Ccab.to_csv('H:/Cov RFI/cor_Comp'+sub+'CAB.csv', index=False, columns=df.columns)

## End ##

# replace field that's entirely space (or empty) with NaN
print(df.replace(r'^\s*$', np.nan, regex=True))