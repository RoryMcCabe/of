# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 15:34:31 2021

@author: McCabeR
"""

import glob, time, pandas as pd, config, os, time
#from datetime import datetime, date
#today = date.today().strftime("%d_%m_%Y")
#print(datetime.date(datetime.now()))
#print(datetime.time(datetime.now()))
ver = str(int(time.time()))
ver
base_path = r"C:\network_price_controls"
date_str = config.date_str
#company_list = ["dummy_test"]#,"test2"]
company_list = config.company_list
#company_path_dict = config.company_path_dict
files=[]
for com in company_list:
    source = os.path.join(base_path, "gather", com, date_str)
    files = files + glob.glob(source + 'npc_*.csv')
dest='N:/NPC-DS Project/ED/data/gather/Grouped/'

cfiles, mfiles, ofiles=[],[],[]
for file in files:
    if 'npc_c' in file: cfiles += [file]
    elif 'npc_m' in file: mfiles += [file]
    else: ofiles += [file]

master,memos,misc = pd.DataFrame(),pd.DataFrame(),pd.DataFrame()
percent=[]
def gengroup(files,ftype,dftype,tablist):
    for n,file in enumerate(files):
        pc = 100*(n+1)/len(files)
        if pc%1==0: percent.append(time.time())
        print(round(pc,2), '% ',ftype, 'in DNO', company_list.index(file.split('\\')[3])+1, file.split('\\')[3], file.split('\\')[6], '...')
        df = pd.read_csv(file,encoding='utf-8')
        dftype = pd.concat([dftype,df], ignore_index=True, sort=True)
    print('Saving ', ftype, tablist, ' file...')
    return(dftype)

start =time.time()
master =gengroup(cfiles,'master',master,'C/CV')
end = time.time()
time_seconds = end - start
print("This run took: " + str(time_seconds/60) + " minutes")
import matplotlib.pyplot as plt
plt.plot(percent)
plt.savefig(dest+'master.png')

memos=gengroup(mfiles,'memo',memos,'M')
plt.plot(percent)
misc=gengroup(ofiles,'misc',misc,'Ap,I,Li,Narm,OErpe,V')
plt.plot(percent)
#print(sorted(master.columns))
#for col in master.columns: print(col,master[col].nunique()) # 41

# master ~ 470Mb
master.to_csv(dest + 'all_c_and_cv_' + ver + '.csv', index=False, encoding='utf-8-sig')
memos.to_csv(dest + 'all_memo_' + ver + '.csv', index=False, encoding='utf-8-sig')
misc.to_csv(dest + 'all_misc_' + ver + '.csv', index=False, encoding='utf-8-sig')

def edgroup(xlist):
    res = pd.DataFrame()
    for file in files:
        if file.split('\\')[6].split('_')[1] in xlist:
            df = pd.read_csv(file,encoding='utf-8')
            res = pd.concat([res,df], ignore_index=True, sort=True)
    return(res)

# Note: C2 is in both lr and copc
lrlist = ['cv1','cv2','cv3','cv4','c2']
lrgroup = edgroup(lrlist)
lrgroup.to_csv(dest + 'load_related_capex_' + ver + '.csv', index = False, encoding='utf-8-sig')

xllist = ['cv5','cv6','cv7','cv8','cv9','cv10','cv11','cv12','cv13','cv14','cv15','cv16','cv17','cv18','cv19','cv20','cv21','cv22','c3']
xlgroup = edgroup(xllist)
xlgroup.to_csv(dest + 'non_load_capex_' + ver + '.csv', index = False, encoding='utf-8-sig')

xcplist = ['c4','c5','c6','c7']
xcpgroup = edgroup(xcplist)
xcpgroup.to_csv(dest + 'non_op_capex_' + ver + '.csv', index = False, encoding='utf-8-sig')

hvplist = ['cv23','cv24','cv25']
hvpgroup = edgroup(hvplist)
hvpgroup.to_csv(dest + 'high_value_projects_' + ver + '.csv', index = False, encoding='utf-8-sig')

shetlist = ['c25']
shetgroup = edgroup(shetlist)
shetgroup.to_csv(dest + 'shetland_' + ver + '.csv', index = False, encoding='utf-8-sig')

rpmlist = ['c24']
rpmgroup = edgroup(rpmlist)
rpmgroup.to_csv(dest + 'related_party_margin_' + ver + '.csv', index = False, encoding='utf-8-sig')

noslist = ['cv26','cv27','cv28','cv29','cv30','cv31','cv32','cv33','cv34','c8']
nosgroup = edgroup(noslist)
nosgroup.to_csv(dest + 'network_operating_costs_' + ver + '.csv', index = False, encoding='utf-8-sig')

cailist = ['cv35','c9','c10','c11']
caigroup = edgroup(cailist)
caigroup.to_csv(dest + 'closely_associated_indirects_' + ver + '.csv', index = False, encoding='utf-8-sig')

bsclist = ['c12','c13','c14']
bscgroup = edgroup(bsclist)
bscgroup.to_csv(dest + 'business_support_costs_' + ver + '.csv', index = False, encoding='utf-8-sig')

otherlist = ['cv36','cv36a','cv37','cv38']
othergroup = edgroup(otherlist)
othergroup.to_csv(dest + 'other_costs_within_price_control_' + ver + '.csv', index = False, encoding='utf-8-sig')

copclist = ['cv39','c2','c16','c17','c18','c19','c21']
copcgroup = edgroup(copclist)
copcgroup.to_csv(dest + 'costs_outside_price_control_' + ver + '.csv', index = False, encoding='utf-8-sig')

nabclist = ['c22','c23']
nabcgroup = edgroup(nabclist)
nabcgroup.to_csv(dest + 'non_activity_based_costs_' + ver + '.csv', index = False, encoding='utf-8-sig')

lrgroup['group']='load_related_capex'
xlgroup['group']='non_load_capex'
xcpgroup['group']='non_op_capex'
hvpgroup['group']='high_value_projects'
shetgroup['group']='shetland'
rpmgroup['group']='related_party_margin'
nosgroup['group']='network_operating_costs'
caigroup['group']='closely_associated_indirects'
bscgroup['group']='business_support_costs'
othergroup['group']='other_costs_within_price_control'
copcgroup['group']='costs_outside_price_control'
nabcgroup['group']='non_activity_based_costs'
master_grouped = pd.concat([lrgroup, xlgroup, xcpgroup, hvpgroup, shetgroup, rpmgroup, nosgroup, caigroup, bscgroup, othergroup, copcgroup, nabcgroup], ignore_index=True, sort=True)
master_grouped.to_csv(dest + 'master_grouped' + ver + '.csv', index = False, encoding='utf-8-sig')
