# -*- coding: utf-8 -*-
"""
Created on Mon May 24 18:04:10 2021

@author: McCabeR
"""

import glob, pandas as pd, numpy as np, matplotlib.pyplot as plt

target='2020_Q4'# '2020_Q3' '2020_Q4' '2021_Q1' '2021_Q2'
root='H:/GSoP/fromSP/'
source=root+target+'/'
files = glob.glob(source + '*.xls*')
master_raw, master_fin, master_num=pd.DataFrame(),pd.DataFrame(),pd.DataFrame()
for file in files:
    print('Working on', file[15:])#, '\n', pd.ExcelFile(file).sheet_names)
    try:
        pd.read_excel(file, header=None, sheet_name='Data Input', nrows=1)
    except:
        try:
            pd.read_excel(file, header=None, sheet_name='Sheet1', nrows=1)
        except:
            try:
                pd.read_excel(file, header=None, sheet_name='Octopus Energy', nrows=1)
            except:
                try:
                    pd.read_excel(file, header=None, sheet_name='Q1 2021', nrows=1)                
                except:
                    try:
                        pd.read_excel(file, header=None, sheet_name='Data Input Q1 2021', nrows=1)
                    except:
                        try:
                            pd.read_excel(file, header=None, sheet_name='Q1', nrows=1)
                        except:
                            try:
                                pd.read_excel(file, header=None, sheet_name='Guaranteed Standards - performa', nrows=1)
                            except:
                                try:
                                    pd.read_excel(file, header=None, sheet_name='Q4', nrows=1)
                                except:
                                    try:
                                        pd.read_excel(file, header=None, sheet_name='Data Input Q4', nrows=1)
                                    except:
                                        try:
                                            pd.read_excel(file, header=None, sheet_name='Q3 2020 Guaranteed Standards-Pe', nrows=1)
                                        except:
                                            try:
                                                pd.read_excel(file, header=None, sheet_name='Data Input Q3', nrows=1)
                                            except:
                                                try:
                                                    pd.read_excel(file, header=None, sheet_name='Q3', nrows=1)
                                                except:
                                                    try:
                                                        pd.read_excel(file, header=None, sheet_name='Q1 2020 Octopus Energy (2)', nrows=1)
                                                    except:
                                                        try:
                                                            pd.read_excel(file, header=None, sheet_name='Data Input Q2', nrows=1)
                                                        except:
                                                            sname='Q2'#GSOP Q2 2020'
                                                        else:
                                                            sname='Data Input Q2'
                                                    else:
                                                        sname='Q1 2020 Octopus Energy (2)'
                                                else:
                                                    sname='Q3'
                                            else:
                                                sname='Data Input Q3'
                                        else:
                                            sname='Q3 2020 Guaranteed Standards-Pe'
                                    else:
                                        sname='Data Input Q4'
                                else:
                                    sname='Q4'
                            else:
                                sname='Guaranteed Standards - performa'
                        else:
                            sname='Q1'
                    else:
                        sname='Data Input Q1 2021'
                else:
                    sname='Q1 2021'
            else:
                sname='Octopus Energy'
        else:
            sname='Sheet1'
    else:
        sname='Data Input'
    name=pd.read_excel(file, header=None, sheet_name=sname, nrows=1).iloc[0,1]
    if (name == 'Complete this cell') or (pd.isnull(name)):
        print('\t', file.split('\\')[1].split('.')[0], 'has no name')
        print('\t', 'Setting name as', file.split('\\')[1].split('.')[0], '\n')
        name=file.split('\\')[1].split('.')[0]
    qtr=pd.read_excel(file, header=None, sheet_name=sname, skiprows=1, nrows=1).iloc[0,1]
#    if pd.isnull(qtr):
#        print('\t', file.split('\\')[1].split('.')[0], 'has no qtr')
#        print('\t', 'Setting qtr as', file.split('_')[-2], '\n')
#        qtr=file.split('_')[-2]
    if target=='2021_Q1': qtr=1
    elif target=='2021_Q2': qtr=2
    elif target=='2020_Q3': qtr=3
    elif target=='2020_Q4': qtr=4
    else: print('\tERROR with qtr for',name,qtr)
    end_date=pd.read_excel(file, header=None, sheet_name=sname, skiprows=2, nrows=1).iloc[0,1]
#    if pd.isnull(end_date):
#        print('\t', file.split('\\')[1].split('.')[0], 'has no end_date\n')
#        print('\t', 'Setting end_date', '\n')
    if target=='2021_Q1': end_date='2021-03-31 00:00:00'
    elif target=='2021_Q2': end_date='2021-06-30 00:00:00'
    elif target=='2020_Q3': end_date='2020-09-30 00:00:00'
    elif target=='2020_Q4': end_date='2020-12-31 00:00:00'
    else: print('\tERROR with end_date for',name,qtr,end_date)
    df1_raw=pd.read_excel(file, sheet_name=sname, skiprows=5, nrows=15, usecols='A:G')
    df1_raw.columns=['Category', 'Regulation', 'Subcat',
                     'Cases where the regulation applied (number)', 'Breaches (number)',
                     'Exempt breaches under Regulation 9 (number)', 'Explanatory notes']
    df1_raw.dropna(how='all',inplace=True)
    df1_raw['Source']=name
    df1_raw['Qtr']=qtr
    df1_raw['End_Date']=end_date
    df1_raw.replace({'Micro- businesses':'Micro-businesses'}, inplace=True, regex=True)
    df1_raw.iloc[8,2]='Microbusiness gas appointments'
    df1_raw.iloc[9,2]='Microbusiness electricity appointments'
    df2_fin=pd.read_excel(file, sheet_name=sname, skiprows=25, nrows=13, usecols='A,C:D')
    df2_fin.columns=['Category', 'Subcat', 'Payments due to customers']
    df2_fin.dropna(how='all',inplace=True)
    df2_fin['Source']=name
    df2_fin['Qtr']=qtr
    df2_fin['End_Date']=end_date
    df2_fin.replace({'Reconnections':'Electricity reconnections',
                     'Ddomestics':'Domestics',
                     'prepayment gas meters':'gas prepayment meters'}, inplace=True, regex=True)
    df2_fin.replace({'Number of Additional Standard Payments (in aggregate)':'Number of Additional Standard Payments'}, inplace=True)
    df2_fin.iloc[1,0]=df2_fin.iloc[0,0]
    df2_fin.iloc[2,0]=df2_fin.iloc[0,0]
    df2_fin.iloc[3,0]=df2_fin.iloc[0,0]
    df2_fin.iloc[5,0]=df2_fin.iloc[4,0]
    df2_fin.iloc[6,0]=df2_fin.iloc[4,0]
    df2_fin.iloc[7,0]=df2_fin.iloc[4,0]
    df3_num=pd.read_excel(file, sheet_name=sname, skiprows=41, nrows=10, usecols='A,C:E')
    df3_num.columns=['Category', 'Subcat', 'Breaches as % of cases', 'Exempt breaches as % of breaches']
    df3_num['Source']=name
    df3_num['Qtr']=qtr
    df3_num['End_Date']=end_date
    df3_num.replace({'Reconnections':'Electricity reconnections',
                     'prepayment gas meters':'gas prepayment meters'}, inplace=True, regex=True)
    df3_num.iloc[1,0]=df3_num.iloc[0,0]
    df3_num.iloc[2,0]=df3_num.iloc[0,0]
    df3_num.iloc[3,0]=df3_num.iloc[0,0]
    df3_num.iloc[5,0]=df3_num.iloc[4,0]
    df3_num.iloc[6,0]=df3_num.iloc[4,0]
    df3_num.iloc[7,0]=df3_num.iloc[4,0]
    master_raw = pd.concat([master_raw,df1_raw], ignore_index=True)#, sort=True)
    master_fin = pd.concat([master_fin,df2_fin], ignore_index=True)#, sort=True)
    master_num = pd.concat([master_num,df3_num], ignore_index=True)#, sort=True)
print('Processing',len(files),'files complete')

master_raw = master_raw.apply(lambda x: x.astype(str).str.lower())
master_raw = master_raw.apply(lambda x: x.astype(str).str.strip())
master_fin = master_fin.apply(lambda x: x.astype(str).str.lower())
master_fin = master_fin.apply(lambda x: x.astype(str).str.strip())
master_num = master_num.apply(lambda x: x.astype(str).str.lower())
master_num = master_num.apply(lambda x: x.astype(str).str.strip())

def cleanmaster(m, c1, c2, c3):
    m.Source.replace({'british_gas_guaranteed_standards_q1_2021':'british gas','british_gas_guaranteed_standards_q3_2020':'british gas','british_gas_guaranteed_standards_q4_2020':'british gas',
                      'bulb_guaranteed_standards_q1_2021':'bulb','bulb_guaranteed_standards_q2_2020':'bulb','bulb_guaranteed_standards_q3_2020':'bulb',
                      'green_supplier_guaranteed_standards_q1_2021':'green supplier','green_supplier_guaranteed standards_q2_2020':'green supplier','green_supplier_guaranteed_standards_q3_2020':'green supplier','green_supplier_guaranteed_standards_q4_2020':'green supplier',
                      'opus energy ltd':'opus energy',
                      'ovo energy':'ovo',
                      'pure_planet_guaranteed_standards_q1_2021':'pure planet','pure_planet_guaranteed_standards_q3_2020':'pure planet',
                      'smartestenergy limited':'smartest energy business',
                      'social_energy_guaranteed_standards_q2_2020':'social energy','social_energy_guaranteed_standards_q3_2020':'social energy',
                      'utility_point_guaranteed_standards_q1_2021':'utility point','utility_point_guaranteed_standards_q2_2020':'utility point','utilty_point_guaranteed_standards_q3_2020':'utility point',
                      'verastar_group_guaranteed standards_q2_2020':'verastar','verastar group':'verastar'}, inplace=True, regex=True)
    m.iloc[:,c1] = m.iloc[:,c1].replace('nan', np.nan)
    m.iloc[:,c2].replace({'q1 2021':'1','q1':'1',
                          'q4 2020':'4','q4':'4',
                          'q2 2021':'2','q2':'2',
                          'q3 2020':'3','q3':'3',}, inplace=True, regex=True)
    m.iloc[:,c3].replace({'31.03.21':'2021-03-31 00:00:00',
                          '31.12.20':'2020-12-31 00:00:00',
                          '30.09.20':'2020-09-30 00:00:00',
                          '31/9/2020':'2020-09-30 00:00:00',
                          '31/06/2020':'2020-06-30 00:00:00',
                          '30.06.20':'2020-06-30 00:00:00',
                          '30/092020 00:00:00':'2020-09-30 00:00:00',
                          '19.04.2021':'2021-04-19 00:00:00'}, inplace=True, regex=True)

cleanmaster(master_raw, range(3,10), 8, 9)
for i in (*range(3,6), *range(8,9)): master_raw.iloc[:,i] = pd.to_numeric(master_raw.iloc[:,i])
master_raw.iloc[:,9] =  pd.to_datetime(master_raw.iloc[:,9], format='%Y-%m-%d %H:%M:%S')
print(master_raw.info())

cleanmaster(master_fin, range(2,6), 4, 5)
for i in (*range(2,3), *range(4,5)): master_fin.iloc[:,i] = pd.to_numeric(master_fin.iloc[:,i])
master_fin.iloc[:,5] =  pd.to_datetime(master_fin.iloc[:,5], format='%Y-%m-%d %H:%M:%S')
master_fin.info()

cleanmaster(master_num, range(2,7), 5, 6)
for i in (*range(2,4), *range(5,6)): master_num.iloc[:,i] = pd.to_numeric(master_num.iloc[:,i])
master_num.iloc[:,6] =  pd.to_datetime(master_num.iloc[:,6], format='%Y-%m-%d %H:%M:%S')
master_num.info()

#[master_raw.iloc[:,i].unique() for i in range(master_raw.shape[1])]
#[master_fin.iloc[:,i].unique() for i in range(master_fin.shape[1])]
#[master_num.iloc[:,i].unique() for i in range(master_num.shape[1])]
print(master_raw.iloc[:,3].value_counts(dropna=False).head())
print(master_raw.iloc[:,4].value_counts(dropna=False).head())
print(master_raw.iloc[:,5].value_counts(dropna=False).head())
print(master_fin.iloc[:,2].value_counts(dropna=False).head()) # 2 values (60, 30) have freq between 0 and NaN -> only 3 NaN
print(master_num.iloc[:,2].value_counts(dropna=False).head())
print(master_num.iloc[:,3].value_counts(dropna=False).head())

print('Unique Sources = # files?', master_raw.iloc[:,7].nunique() == len(files))
print('No name left as default?', sum(master_raw.iloc[:,7].str.contains('Complete this cell'))==0)
# Fixed for BG, Bulb, Green S, Social, PurePlanet, UP, Verastar

fig, axs = plt.subplots(4, 1, figsize=(28,20))
axs[0].plot(master_raw.iloc[:,3])
axs[0].set_title('Raw: # cases where reg applied')
axs[1].plot(master_raw.iloc[:,4])
axs[1].set_title('Raw: # breaches')
axs[2].plot(master_raw.iloc[:,5])
axs[2].set_title('Raw: # exempt breaches under reg 9')
axs[3].plot(master_raw.iloc[:,4]-master_raw.iloc[:,5])
axs[3].set_title('Raw: 4-5 = # non-exempt breaches')

peaks = master_raw.iloc[:,3:6].idxmax().unique()
print('\t',target,':\n',master_raw.iloc[peaks,:].Source)

print('Top five values for cases, breaches and exempt with supplier, cat and subcat')
for val in [sorted(zip(master_raw.iloc[:,i].dropna(),master_raw[~master_raw.iloc[:,i].isna()].iloc[:,7],master_raw[~master_raw.iloc[:,i].isna()].iloc[:,0],master_raw[~master_raw.iloc[:,i].isna()].iloc[:,2]),reverse=True)[:5] for i in (3,4,5)]: print('\n\n',*val)

diff = master_raw.iloc[:,4] - master_raw.iloc[:,5] # breaches - exempt
top5 = diff.nlargest() # top 5 values, better than idxmax
print(target,master_raw.iloc[top5.index,[2,7]])
# Q1 OVO, EDF, Bulb, OVO,  SP
# OVO, EDF, EON,  OVO,  EON
# OVO, EON, EDF,  EON,  OVO
# EON, SP,  EDF,  Bulb, EDF

# NOT master=pd.concat([master_raw,master_fin,master_num],sort=True) # all 1254 x 13
master_rf = master_raw.merge(master_fin, how='outer', on=['Category','Subcat','Source','Qtr','End_Date'])
master = master_rf.merge(master_num, how='outer', on=['Category','Subcat','Source','Qtr','End_Date'])
cols=['Category','Regulation','Subcat',
      'Cases where the regulation applied (number)',
      'Breaches (number)',
      'Exempt breaches under Regulation 9 (number)',
      'Payments due to customers',
      'Breaches as % of cases',
      'Exempt breaches as % of breaches',
      'Explanatory notes','Source','Qtr','End_Date']
master=master[cols]
master.to_csv(root + 'master'+target+'.csv', index=False)

q1=pd.read_csv(root+'master2021_Q1.csv')
q2=pd.read_csv(root+'master2021_Q2.csv')
q3=pd.read_csv(root+'master2020_Q3.csv')
q4=pd.read_csv(root+'master2020_Q4.csv')

master_yr=pd.concat([q1,q2,q3,q4], ignore_index=True)
bgx=master_yr[master_yr.Source=='british gas x'] # 12 from q3
print(bgx.min())
print(master_yr.min())
print(bgx.max())
print(master_yr.max())

print([sum(master_yr.iloc[:,i] < 0) for i in [3,4,5,6,7,8]]) # 0 0 0 10 0 0
print(master_yr.iloc[:,[6,10,11]][master_yr.iloc[:,6] < 0]) # 7 RH Q2, 1 RH Q3, 2 UWH Q2
master_yr.iloc[:,6] = np.where(master_yr.iloc[:,6] < 0, abs(master_yr.iloc[:,6]), master_yr.iloc[:,6])

print(master_yr[master_yr.iloc[:,7]==max(master_yr.iloc[:,7])].iloc[:,10:12]) # Shell 2 only br%case > 1 @ 3
print(master_yr[master_yr.iloc[:,8]==max(master_yr.iloc[:,8])].iloc[:,10:12]) # RH 2 ex%br > 1 @ 24
print(master_yr[master_yr.iloc[:,8]==sorted(master_yr.iloc[:,8].unique())[-2]].iloc[:,10:12]) # UWH 2 ex%br > 1 @ 5.4

print(sorted(master_yr.iloc[:,9].unique().astype(str))[:10]) # notes include 0 and 0.0
print(len(master_yr.iloc[:,10].unique())) # 70 Source -> 50 -> 54
print(sorted(master_yr.iloc[:,10].unique()))
print(sorted(master_yr[master_yr.iloc[:,11].isnull()].Source.unique())) # verastar x 3 to []
print(master_yr[master_yr.iloc[:,12].isnull()].iloc[:,10:12].nunique()) # 48 blank end_date for Verastar x 4q to []
print(master_yr[master_yr.iloc[:,12].isnull()].Source.unique()) # 48 blank end_date for Verastar to []

plt.figure(figsize=(10,18))
master_yr.iloc[:,[3]].boxplot() # 1, 4, 12 top groups to 1,3,2,6

plt.figure(figsize=(10,18))
master_yr.iloc[:,[4]].boxplot() # 1, 4, 7 top groups to 1,3,3,3

plt.figure(figsize=(10,18))
master_yr.iloc[:,[5]].boxplot() # 1, 4 top groups, clear break to 1,3

plt.figure(figsize=(10,18))
master_yr.iloc[:,[6]].boxplot() # 1, 4 top groups to 1,3

master_yr.iloc[:,7].value_counts(dropna=False).head().plot.bar()
master_yr.iloc[:,8].value_counts(dropna=False).head().plot.bar()

print(master_yr[(master_yr.iloc[:,12] > '2019-12-31') & (master_yr.iloc[:,12] <= '2021-12-31')]) # 36 < 2004 / 2088 2196

# Set LMS size on today's split, i.e. 9/4/rest
master_yr['Size']='na'
for s in master_yr.Source:
    if s in ['british gas','edf energy plc','e.on','npower','scottishpower retail','sse bus energy','ovo','bulb','octopus energy']: master_yr.Size[master_yr.Source==s]='L'
    elif s in ['avro energy','shell energy retail','utilita energy','utility warehouse']: master_yr.Size[master_yr.Source==s]='M'
    else: master_yr.Size[master_yr.Source==s]='S'
print(master_yr[master_yr.Size=='L'].Source.nunique()) # 9
print(master_yr[master_yr.Size=='M'].Source.nunique()) # 4
print(master_yr[master_yr.Size=='S'].Source.nunique()) # 41
print(master_yr[master_yr.Size=='na'].Source.nunique()) # 0 chk
print('Large:',master_yr[master_yr.Size=='L'].Source.unique())
# OVO L           > Q4 '19
# Octopus L       > Q2 '20
# Bulb L          > Q2 ' 20
print('Medium:',master_yr[master_yr.Size=='M'].Source.unique())
# Avro M          > Q3 '19, x anything <
print('Small:',master_yr[master_yr.Size=='S'].Source.unique())
# co-op x         > Q1 '19
# green nw        x > Q3 '20
# british gas 'x' only for Q3 '20

master_yr.to_csv(root + 'master_yr.csv', index=False)

# Heatmap

print(12*50,12*45,12*43,12*36)
print(master_yr.End_Date.value_counts()) # Q3,4,1,2
# Below fixed
q1.Qtr.unique() # 3 and 4 -> only 1
q1.Source[q1.Qtr==3].unique() # Nabuh x
q1.Source[q1.Qtr==4].unique() # BG, Orsted x
q2.Qtr.unique() # 1 -> only 2
q2.Source[q2.Qtr==1].unique() # CNG, Good, Igloo, UGP x
q3.Qtr.unique() # 1 and 2 -> only 3
q3.Source[q3.Qtr==1].unique() # BG x
q3.Source[q3.Qtr==2].unique() # CNG, OVO x
q4.Qtr.unique() # 3 -> only 4
q4.Source[q4.Qtr==3].unique() # Nabuh, Utilita x

import seaborn as sns
sns.set()

resp = pd.DataFrame()
for s in master_yr.Source.unique():
    for q in master_yr.Qtr.unique():
        if any(master_yr.End_Date[(master_yr.Source==s) & (master_yr.Qtr==q)].notnull()): resp.loc[s,q]=sum(master_yr.End_Date[(master_yr.Source==s) & (master_yr.Qtr==q)].notnull())
col=[3,4,1,2]
resp=resp[col].sort_index()
print(resp.min().min(), resp.max().max())
resp[resp.max(axis=1)==resp.max().max()], resp.columns[resp.max()==resp.max().max()]

fig, ax = plt.subplots(figsize=(20,40))
ax.tick_params(right=True, top=True, labelright=True, labeltop=True)
sns.heatmap(resp/12, annot=True, vmin=0, center=resp.max().max()/2, linewidths=.5, cbar_kws = dict(use_gridspec=False,location="top"))
plt.text(0,-5,'Number of non-null End_Date values per supplier per qtr', fontsize=30)
fig.savefig(root+'heatmap.png')

resp.count() # 47,49,45,42+1
GSoPfreq = [resp.iloc[i].count() for i in range(len(resp))]
pd.Series(GSoPfreq).value_counts(sort=False) # 5x1qtr resp, 4x2, 10-1x3, 35+1 x all

# Q1 totals
c1=sum(q1[q1.Subcat=='gas appointments'].iloc[:,3].dropna())
b1=sum(q1[q1.Subcat=='gas appointments'].iloc[:,4].dropna())
x1=sum(q1[q1.Subcat=='gas appointments'].iloc[:,5].dropna())
c2=sum(q1[q1.Subcat=='faulty gas meters'].iloc[:,3].dropna())
b2=sum(q1[q1.Subcat=='faulty gas meters'].iloc[:,4].dropna())
x2=sum(q1[q1.Subcat=='faulty gas meters'].iloc[:,5].dropna())
c3=sum(q1[q1.Subcat=='faulty gas prepayment meters'].iloc[:,3].dropna())
b3=sum(q1[q1.Subcat=='faulty gas prepayment meters'].iloc[:,4].dropna())
x3=sum(q1[q1.Subcat=='faulty gas prepayment meters'].iloc[:,5].dropna())
c4=sum(q1[q1.Subcat=='gas reconnections'].iloc[:,3].dropna())
b4=sum(q1[q1.Subcat=='gas reconnections'].iloc[:,4].dropna())
x4=sum(q1[q1.Subcat=='gas reconnections'].iloc[:,5].dropna())

c5=sum(q1[q1.Subcat=='electricity appointments'].iloc[:,3].dropna())
b5=sum(q1[q1.Subcat=='electricity appointments'].iloc[:,4].dropna())
x5=sum(q1[q1.Subcat=='electricity appointments'].iloc[:,5].dropna())
c6=sum(q1[q1.Subcat=='faulty electricity meters'].iloc[:,3].dropna())
b6=sum(q1[q1.Subcat=='faulty electricity meters'].iloc[:,4].dropna())
x6=sum(q1[q1.Subcat=='faulty electricity meters'].iloc[:,5].dropna())
c7=sum(q1[q1.Subcat=='faulty electricity prepayment meters'].iloc[:,3].dropna())
b7=sum(q1[q1.Subcat=='faulty electricity prepayment meters'].iloc[:,4].dropna())
x7=sum(q1[q1.Subcat=='faulty electricity prepayment meters'].iloc[:,5].dropna())
c8=sum(q1[q1.Subcat=='electricity reconnections'].iloc[:,3].dropna())
b8=sum(q1[q1.Subcat=='electricity reconnections'].iloc[:,4].dropna())
x8=sum(q1[q1.Subcat=='electricity reconnections'].iloc[:,5].dropna())

c9=sum(q1[q1.Subcat=='microbusiness gas appointments'].iloc[:,3].dropna())
b9=sum(q1[q1.Subcat=='microbusiness gas appointments'].iloc[:,4].dropna())
x9=sum(q1[q1.Subcat=='microbusiness gas appointments'].iloc[:,5].dropna())
c10=sum(q1[q1.Subcat=='microbusiness electricity appointments'].iloc[:,3].dropna())
b10=sum(q1[q1.Subcat=='microbusiness electricity appointments'].iloc[:,4].dropna())
x10=sum(q1[q1.Subcat=='microbusiness electricity appointments'].iloc[:,5].dropna())

# Can split by size
'{:,}'.format(int(sum(master_yr[(master_yr.Subcat=='gas appointments')&(master_yr.Qtr==1)&(master_yr.Size=='L')].iloc[:,3].dropna())))
'{:,}'.format(int(sum(master_yr[(master_yr.Subcat=='gas appointments')&(master_yr.Qtr==1)&(master_yr.Size=='M')].iloc[:,3].dropna())))
'{:,}'.format(int(sum(master_yr[(master_yr.Subcat=='gas appointments')&(master_yr.Qtr==1)&(master_yr.Size=='S')].iloc[:,3].dropna())))

# Can split case/br/ex by market and type
dg_cases=c1+c2+c3+c4
de_cases=c5+c6+c7+c8
dom_cases=dg_cases+de_cases
mg_cases=c9
me_cases=c10
mic_cases=mg_cases+me_cases
all_cases=dom_cases+mic_cases

dg_br=b1+b2+b3+b4
de_br=b5+b6+b7+b8
dom_br=dg_br+de_br
mg_br=b9
me_br=b10
mic_br=mg_br+me_br
all_br=dom_br+mic_br

dg_x=x1+x2+x3+x4
de_x=x5+x6+x7+x8
dom_x=dg_x+de_x
mg_x=x9
me_x=x10
mic_x=mg_x+me_x
all_x=dom_x+mic_x

dom_diff=dom_br-dom_x
mic_diff=mic_br-mic_x
all_diff=all_br-all_x

# ASP chk
all_diff
asp=sum(q1[q1.Subcat=='number of additional standard payments'].iloc[:,4].dropna())
asp

# Total non-x br
nxb1=sum(q1.iloc[:,4].dropna()) - sum(q1.iloc[:,5].dropna())
nxb4=sum(q4.iloc[:,4].dropna()) - sum(q4.iloc[:,5].dropna())
nxb3=sum(q3.iloc[:,4].dropna()) - sum(q3.iloc[:,5].dropna())
nxb2=sum(q2.iloc[:,4].dropna()) - sum(q2.iloc[:,5].dropna())
plt.plot(pd.Series([nxb2,nxb3,nxb4,nxb1]))

for i in master_yr.iloc[:,4].dropna().unique():
    if int(i) != i: print(i) # 75.5

q4.Source[q4.iloc[:,4]==75.5] # PP Q4 Elec Dom Apt. Br. ?? shows as 76

for i in master_yr.iloc[:,7].dropna().unique():
    if (i<0) | (i>100): print(i) #

#Test

sum(master_yr.iloc[:,3]>master_yr.iloc[:,4]) # 730
sum(master_yr.iloc[:,3]==master_yr.iloc[:,4]) # 652
testpos=master_yr.iloc[:,3]>=master_yr.iloc[:,4]
sum(testpos) # 1382
testfail=master_yr.iloc[:,3]<master_yr.iloc[:,4]
sum(testfail) # 7 CANNOT be less
master_yr[testfail].iloc[:,[10,11]] # ESB Q1, Bulb Q2, E Q2,3,4, Shell Q2, OVO Q3 <CHECK>
rest=~(testfail | testpos)
sum(rest) # 807
len(master_yr[rest][master_yr[rest].iloc[:,3].isnull() & master_yr[rest].iloc[:,4].isnull()]) # 659
len(master_yr[rest][master_yr[rest].iloc[:,3].notnull()].iloc[:,4])#.unique() # 24 NaN
len(master_yr[rest][master_yr[rest].iloc[:,4].notnull()].iloc[:,3])#.unique() # 124 NaN <CHECK>

master_yr[rest][master_yr[rest].iloc[:,4].notnull()].iloc[:,10].nunique() # 38 suppliers

sum(master_yr.iloc[:,4]>master_yr.iloc[:,5]) # 412
sum(master_yr.iloc[:,4]==master_yr.iloc[:,5]) # 750
testpos=master_yr.iloc[:,4]>=master_yr.iloc[:,5]
sum(testpos) # 1162
testfail=master_yr.iloc[:,4]<master_yr.iloc[:,5]
sum(testfail) # 9 CANNOT be less
master_yr[testfail].iloc[:,[10,11]] # 7RH, 2UWH <CHECK>
rest=~(testfail | testpos)
sum(rest) # 1037
len(master_yr[rest][master_yr[rest].iloc[:,4].isnull() & master_yr[rest].iloc[:,5].isnull()]) # 671
len(master_yr[rest][master_yr[rest].iloc[:,4].notnull()].iloc[:,5])#.unique() # 353
len(master_yr[rest][master_yr[rest].iloc[:,5].notnull()].iloc[:,4])#.unique() # 13 <CHECK>

master_yr[rest][master_yr[rest].iloc[:,5].notnull()].iloc[:,10].unique() # 4 suppliers: E, Nabuh, UP, BGX

## Report

# Overall breach rate x Dom, Micro, ASP, All
focus = q1 #master_yr

qdom = focus[(focus.Category=='gas domestic') | (focus.Category=='electricity domestic')] # 8 cats
qdiff1 = (qdom.iloc[:,4] - qdom.iloc[:,5]) / qdom.iloc[:,3]
qdiff1.replace(np.inf,np.nan,inplace=True)
print(round(100*(sum(qdiff1.dropna()))/len(qdiff1.dropna()),1))

qmicro = focus[(focus.Category=='gas micro-business') | (focus.Category=='electricity micro-business')] # 2 cats
qdiff2 = (qmicro.iloc[:,4] - qmicro.iloc[:,5]) / qmicro.iloc[:,3]
qdiff2.replace(np.inf,np.nan,inplace=True)
#print(round(100*sum(qmicro.iloc[:,7].dropna())/len(qmicro),1))
print(round(100*(sum(qdiff2.dropna()))/len(qdiff2.dropna()),1))

qasp = focus[focus.Category=='all gas and electricity domestics and micro-businesses'] # 1 cat
qdiff3 = (qasp.iloc[:,4] - qasp.iloc[:,5]) / qasp.iloc[:,3]
qdiff3.replace(np.inf,np.nan,inplace=True)
#if len(qasp) !=0: print(round(100*sum(qasp.iloc[:,7].dropna())/len(qasp),1))
if len(qdiff3.dropna()) !=0: print(round(100*(sum(qdiff3.dropna()))/len(qdiff3.dropna()),1))
else: print('No ASPs')

qall=pd.concat([qdiff1,qdiff2,qdiff3])
#print(round(100*sum(qall.iloc[:,7].dropna())/len(qall),1))
qall.replace(np.inf,np.nan,inplace=True)
print(round(100*(sum(qall.dropna()))/len(qall.dropna()),1))

# Breach # x Dom, ND
sum(qdom.dropna().iloc[:,4]) # 72,337
sum(qmicro.dropna().iloc[:,4]) # 345

# % Missed apt x Dom
round(100*sum(qdom.iloc[:,4].dropna()[(qdom.Subcat=='gas appointments') | (qdom.Subcat=='electricity appointments')]) / sum(qdom.iloc[:,3].dropna()[(qdom.Subcat=='gas appointments') | (qdom.Subcat=='electricity appointments')]),2) # 7.09%

# Worst five x Dom, ND, ASP
qdom.sort_values('Breaches as % of cases', ascending=False).iloc[:,[7,10]].head()
qmicro.sort_values('Breaches as % of cases', ascending=False).iloc[:,[7,10]].head()
qasp=q4[q4.Subcat=='number of additional standard payments']
qasp.sort_values('Breaches as % of cases', ascending=False).iloc[:,[7,10]].head()

# Set columns for dashboard
master_yr['Market']='na'
master_yr.Market[(master_yr.Category=='gas domestic') | (master_yr.Category=='electricity domestic')]='Dom'
master_yr.Market[(master_yr.Category=='gas micro-business') | (master_yr.Category=='electricity micro-business')]='Micro'
master_yr.Market[master_yr.Category=='all gas and electricity domestics and micro-businesses']='ASP'
master_yr.Market[master_yr.Category.isnull()]='Null'
master_yr.Market.value_counts()

master_yr['Type']='na'
master_yr.Type[(master_yr.Category=='gas domestic') | (master_yr.Category=='gas micro-business')]='Gas'
master_yr.Type[(master_yr.Category=='electricity domestic') | (master_yr.Category=='electricity micro-business')]='Elec'
master_yr.Type[master_yr.Category=='all gas and electricity domestics and micro-businesses']='ASP'
master_yr.Type[master_yr.Category.isnull()]='Null'
master_yr.Type.value_counts()

master_yr.to_csv(root + 'master_yr.csv', index=False)
