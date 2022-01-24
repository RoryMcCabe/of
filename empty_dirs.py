# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 17:10:24 2020

@author: McCabeR
"""

import glob, os, pandas as pd

filepath='K:/User Centred Data Services/Beta/retail_data/covid_19_rfi/Downloads/TEST (15-04-2020 1015)/Covid_19_RFI/Covid_19_RFI'
listOfEmptyDirs = list()
for (dirpath, dirnames, filenames) in os.walk(filepath):
    if len(dirnames) == 0 and len(filenames) == 0 :
        listOfEmptyDirs.append(dirpath)
print('Empty folders:', listOfEmptyDirs)

source = 'K:/User Centred Data Services/Beta/retail_data/covid_19_rfi/Downloads/TEST (15-04-2020 1015)/Covid_19_RFI/Covid_19_RFI/'
csv_files1 = glob.glob(source + '*/*/*.csv')
csv_files2 = glob.glob(source + '*/*.csv')
csv_files = csv_files1 + csv_files2

skipmask=[csv_files[i].split('/')[8].split('\\')[1][:3]!='Blu' for i in range(len(csv_files))]
csv_files=[csv_files[i] for i in [i for i, val in enumerate(skipmask) if val]]
diff=list(set(csv_files1 + csv_files2) - set(csv_files))
print('\nSkipping', len(diff), 'files from: ', pd.Series([i.split('/')[8].split('\\')[1] for i in diff]).unique())

A=pd.DataFrame()
B=pd.DataFrame()
counta, countb, countnot = 0,0,0

print('Processing...')
for num,file in enumerate(csv_files):
    if 'Industry body' in file:
        print('\nSkipping file: ', file, '\n')
        continue
    else:
        if file.split('/')[8].split('\\')[1][:3] == 'MVV':
            df=pd.read_csv(file,encoding='unicode_escape',sep=';')
        elif file.split('/')[8].split('\\')[1][:3] == 'PFP':
            df=pd.read_csv(file,encoding='unicode_escape', skiprows=1)
        else:
            df = pd.read_csv(file, encoding='unicode_escape')
        df.dropna(how='all', inplace=True, axis='index')
        df.dropna(how='all', inplace=True, axis='columns')
        df.rename(columns=lambda x: x.strip(), inplace=True)
        df.columns = map(str.lower, df.columns)
        df['source'] = file.split('/')[8].split('\\')[3]
        if (num+6) % 66 == 0: print(round((num+6)/6.6),'%...')
        if len(df.columns) > 9: print(num, len(df.columns), file)
        if file.split('/')[8].split('\\')[2][-1]=='A':
            A=A.append(df, sort=True)
            counta+=1
        elif file.split('/')[8].split('\\')[2][-1]=='B':
            B=B.append(df, sort=True)
            countb+=1
        elif file.split('/')[8].split('_')[3][6:9]=='CON':
            A=A.append(df, sort=True)
            counta+=1
        elif file.split('/')[8].split('_')[3][6:9]=='FIN':
            B=B.append(df, sort=True)
            countb+=1        
        else:
            countnot+=1
print('Finished reading in', num+1, 'files')

A.reset_index(inplace=True, drop=True)
B.reset_index(inplace=True, drop=True)

list(A.columns) # 7 + source = correct
list(B.columns) # 25 = 9 + 16 -> 21 = 9+12

A[~A['unnamed: 5'].isnull()] # 228 BG gone 9 Social gone
A[~A['unnamed: 6'].isnull()] # 4 Bryt gone
A[~A['unnamed: 7'].isnull()] # 2 ESB and Zebra gone
A[~A['unnamed: 8'].isnull()] # 2 ESB and Zebra gone
A[~A['unnamed: 9'].isnull()] # 2 ESB and Zebra gone
A[~A['unnamed: 11'].isnull()] # 37 Robin Hood gone
A[~A['01/03/2020'].isnull()] # 80 Robin Hood gone
A[~A['02/03/2020'].isnull()] # 73 Octopus gone
A[~A['43906'].isnull()] # 56 BG gone
A[~A['43913'].isnull()] # 56 BG gone
A[~A['6042020'].isnull()] # 56 BG gone
A[~A['owner'].isnull()] # 9 Bristol gone
A[~A['comment (summary)'].isnull()] # 10 Octopus gone

def chkcol(ab, colname):
    print('\n', ab[~ab[colname].isnull()].supplier.nunique(dropna=False),'\n')
    print(ab[~ab[colname].isnull()].supplier.unique(),'\n')
    print(ab[~ab[colname].isnull()].source.unique())
    print('\n', len(ab[~ab[colname].isnull()]))
    print('\n', ab[~ab[colname].isnull()].index)
    print([len(ab[(~ab[colname].isnull())&(ab.supplier==sup)].isnull()) for sup in ab[~ab[colname].isnull()].supplier.unique() if type(sup)!=float])

chkcol(B, '') # 2 Utilita, (nan) 54+4blank gone
chkcol(B, '08/04/2020 00:00') # 1 2PFP 81
chkcol(B, '58199642.76') # 1 PFP 53
chkcol(B, 'date\tsupplier\tsection\tquestion\tunit\tvalue\tcomment') # 1 2EON 164blank (gone from Ecotricity)
chkcol(B, 'gbp') # 1 PFP 53
chkcol(B, 'revenue') # 1 PFP 53
chkcol(B, 'text') # 1 PFP 28
chkcol(B, 'unnamed: 6') # 2 Green NW 29, YGP 1 gone
chkcol(B, 'unnamed: 7') # 5 EON 3, Green NW 1, SO 1blank, DESL 3, 2Zebra 2 gone

B[~B['unnamed: 12'].isnull()] # 1 Utilita gone
B[~B['unnamed: 13'].isnull()] # 7 Utilita gone
B[~B['unnamed: 14'].isnull()] # 6 Utilita gone
B[~B['eur'].isnull()] # 38 PFP gone
B[~B['value (â£m)'].isnull()] # 16 Npower gone
B[~B['ate'].isnull()] # 54 Opus gone

def analyse(ab):
    print('\nNon-String Rows:', ab.shape[0] - len(ab.select_dtypes(include='object')))
    input("Press Enter to continue...")
    print('\n# Unique:\n', ab.nunique())
    print('\n...plus NaN:\n', A.nunique(dropna=False) - A.nunique())
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
    print('\nTotal Suppliers:', ab.supplier.nunique())

analyse(A)
# all str, 22+1 dates and 7+1 units, no unary, no unique, 2 full: section and source,
# balance..workforce and AM..Zog, 4 close: 1d 7q 1sup 1u, 89 suppliers
analyse(B)
# all str, 16+1 dates and 4+1 units, 3 unary, no unique, 1 full: source,
# -24mil..70mil and AM..Zog, none close, 73 suppliers

A[A.supplier.isnull()].source.unique() # 1
B[B.supplier.isnull()].source.unique() # 7

A.supplier.append(B.supplier).nunique() # 97
supl = pd.Series([csv_files[i].lower().split('/')[8].split('\\')[1:3] for i in range(549)]).value_counts().sort_index()

len(A[A.value.str.contains(',')==True])
A.loc[A.unit!='text'].value=A.loc[A.unit!='text'].value
'123,456'.str.replace(',','')
len(A[A.value.str.contains(',')==True])

A[A.unit!='text'].value.str.replace('%','',inplace=True)
A[A.unit!='text'].value.str.replace('-','',inplace=True)
B[B.unit!='text'].value.str.replace(',','',inplace=True)
B[B.unit!='text'].value.str.replace('%','',inplace=True)
B[B.unit!='text'].value.str.replace('-','',inplace=True)
A.unit.value_counts(dropna=False) # 4 good and 4 other: 9x0 and 1x147 for Opal, a Y in Regent and a n in Opus
val=A.value
val[val<0] # error => includes str
val2=pd.to_numeric(val, errors='coerce').dropna() # 14611/24354 = 60%, 14576/23794 = 61%
valnum=pd.to_numeric(A.value[A.unit=='num'], errors='coerce').dropna() # 100*len(valnum)/sum(A.unit=='num') = 69%
valpc=pd.to_numeric(A.value[A.unit=='percent'], errors='coerce').dropna() # 100*len(valpc)/sum(A.unit=='percent') = 65%
valgbp=pd.to_numeric(A.value[A.unit=='GBP'], errors='coerce').dropna() # 100*len(valgbp)/sum(A.unit=='GBP') = 60%
valtext=pd.to_numeric(A.value[A.unit=='text'], errors='coerce').dropna() # 100*len(valtext)/sum(A.unit=='text') = 0% good
val2[val2<0] # empty => no negative values
val2.value_counts().sort_index() # range 0 to 23000000

afilled=A[A.value.notnull()==True].reset_index(drop=True)
sum([isinstance(afilled.value[i],(float, int)) for i in range(len(afilled))]) # 540 = 3.5%
bfilled=B[B.value.notnull()==True].reset_index(drop=True)
sum([isinstance(bfilled.value[i],(float, int)) for i in range(len(bfilled))]) # 2342 = 75.3%
afillnotnum=afilled[[not isinstance(afilled.value[i],(float, int)) for i in range(len(afilled))]] # 14673
len(afillnotnum.value.unique()) # 2669 comma-ed numbers, y, dash and tabs?
bfillnotnum=bfilled[[not isinstance(bfilled.value[i],(float, int)) for i in range(len(bfilled))]] # 767
len(bfillnotnum.value.unique()) # 213 comma-ed numbers, y, dash and tabs

afillnotnum[afillnotnum.value.str.contains('-')].supplier.unique() # 372 RH
afillnotnum[afillnotnum.value.str.contains('%')].supplier.unique() # 8 So
afillnotnum[afillnotnum.value.str.contains(',')].supplier.unique() # 12 Nabuh, Oct, Regent
afillnotnum[afillnotnum.value=='N'].supplier.unique() # 20 BG, Orbit, RH, SP, UP
afillnotnum[afillnotnum.value=='Y'].supplier.unique() # 192...
afillnotnum[afillnotnum.value=='Yes'].supplier.unique() # 18 x7...
afillnotnum[afillnotnum.value=='y'].supplier.unique() # 1 Opal
afillnotnum[afillnotnum.value=='No'].supplier.unique() # 1 SP
afillnotnum[afillnotnum.value=='TBC'].supplier.unique() # 3 Nabuh
afillnotnum[afillnotnum.value.str.contains('TPP')].supplier.unique() # 5 Nabuh

bfillnotnum[bfillnotnum.value.str.contains('-')].supplier.unique() # 107 x7...
bfillnotnum[bfillnotnum.value.str.contains('%')].supplier.unique() # 2 Bristol
bfillnotnum[bfillnotnum.value.str.contains(',')].supplier.unique() # 70 Bristol, Opal, Regent
bfillnotnum[bfillnotnum.value==' Not performed '].supplier.unique() # 30 Orsted
bfillnotnum[bfillnotnum.value=='Y'].supplier.unique() # 6 Pozitive
bfillnotnum[bfillnotnum.value=='None'].supplier.unique() # 10 Igloo
bfillnotnum[bfillnotnum.value.str.contains('Wales')].supplier.unique() # 1 Orsted

mask=val2.value_counts().sort_index()>50 # 2803
import matplotlib.pyplot as plt
plt.hist(val2.value_counts().sort_index()[mask])

list(A.date.unique()) # 44...42...44...41+nan ... 22+nan
list(B.date.unique()) # 18...17 incl 1 not in A ... 14+nan including 3/30/2020 and 4/6/2020
ABdates = list(A.date.append(B.date).dropna().unique()) # 42 without nan ... 24
ABdates.sort()
A[A.date=='09/03/2020 '].supplier.unique() # 1 Green Supplier gone
A[A.date=='03-08-2020'].supplier.unique() # 1 Blue Green gone
A[A.date=='04-05-2020'].supplier.unique() # 1 Blue Green gone
A[A.date=='15/3/2020'].supplier.unique() # 1 Blue Green gone
A[A.date=='2/24/2020'].supplier.unique() # 1 BPG gone
A[A.date=='2020-02-24'].source.unique() # 1 Foxglove gone
A[A.date=='2020-03-16'].source.unique() # 2 Crown, Foxglove gone
A[A.date=='2020-03-23'].source.unique() # 2 Crown, Foxglove gone
A[A.date=='2020-03-30'].source.unique() # 2 Crown, Foxglove gone
A[A.date=='2020-04-06'].source.unique() # 1 Crown gone
A[A.date=='22/3/2020'].supplier.unique() # 1 Blue Green gone
A[A.date=='23/03/2019'].supplier.unique() # 1 Nabuh gone
A[A.date=='29/2/2020'].supplier.unique() # 1 Blue Green gone
A[A.date=='29/3/2020'].supplier.unique() # 1 Blue Green gone
A[A.date=='3/16/2020'].supplier.unique() # 1 BPG gone
A[A.date=='3/2/2020'].supplier.unique() # 1 BPG gone
A[A.date=='3/23/2020'].supplier.unique() # 1 BPG gone
A[A.date=='3/30/2020'].supplier.unique() # 4 Axpo, BPG, EON, Opus gone
A[A.date=='3/9/2020'].supplier.unique() # 1 BPG gone
A[A.date=='4/6/2020'].source.unique() # 1 EON gone

def chkdate(ab, dateval):
    print('\n', ab[ab.date==dateval].supplier.nunique(dropna=False),'\n')
    print(ab[ab.date==dateval].supplier.unique(),'\n')
    print(ab[ab.date==dateval].source.unique())
    print('\n', len(ab[ab.date==dateval].isnull()))
    print('\n', ab[ab.date==dateval].isnull().index)
    print([len(ab[(ab.date==dateval)&(ab.supplier==sup)].isnull()) for sup in ab[ab.date==dateval].supplier.unique()])

chkdate(B, '2020-04-08') # 1 British Gas gone
chkdate(B, '2020-03-30') # 1 = 1Crown 54 gone
chkdate(B, '3/30/2020') # 5 = 1BPG 54, 1Bristol 54, 1Bryt 29, 2Effortless 83, 1Electroroute 54 gone
# 11 = BPG 54, Bristol 54, Bryt 29, Crown 54, 2Effortless 83, Electroroute 54, So 29, Utilita 54, YGP 29, DESL 29, Zebra 54 gone
chkdate(B, '4/6/2020') # 3 = 1EON 29, 1GreenNW 29, 1Zebra 54 gone

import datetime as dt
#dt.date.strftime
ad=A[A.date.notna()].reset_index(drop=True) # drop 1
ad['date2']=[dt.datetime.strptime(ad.date[i],"%d/%m/%Y") for i in range(len(ad))]

A.to_csv('H:/cor_A2.csv', index=False) # Fri 19:38
B.to_csv('H:/cor_B2.csv', index=False) # Fri 19:38
#pd.DataFrame(csv_files).to_csv('H:/cor_suppliers.csv', index=False)