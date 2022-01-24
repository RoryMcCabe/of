# -*- coding: utf-8 -*-
"""
Created on Mon Apr 1 2019
@author: McCabeR
"""

import csv, time, win32com.client as wc

input_outlook_folder = 'Enforcement'
output_csv_folder = 'H:/Enforcement/'
keywords = ['legal', 'risk', 'consumer benefit'] # can be partial but keep lowercase to match all cases
filtered = {}
start_time = time.time()

def ftest():
    outlook = wc.Dispatch("Outlook.Application").GetNamespace("MAPI")
    inbox = outlook.GetDefaultFolder(6) # 6 is the Inbox default folder index 
    searchdir = inbox.Folders[input_outlook_folder]
    messages=searchdir.Items
    for msg in messages:
        for keyword in keywords:
            if keyword in msg.Body.lower():
                if keyword in filtered.keys():
                    filtered[keyword].append(msg.Subject)
                else:
                    filtered[keyword] = [msg.Subject]

ftest()
print("==== %s seconds ====" % round(time.time() - start_time))

with open(output_csv_folder + 'filtered.csv', mode = 'w', newline = '') as out:
    cw = csv.writer(out, delimiter=',')
    for k,v in filtered.items():
        cw.writerow([k] + [len(v)] + v)