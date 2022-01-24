# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 16:50:56 2019

@author: McCabeR
"""

import glob
import collections as col
import win32com.client as wc

input_dir = 'H:/Enforcement'
emails = glob.glob(input_dir + '**/*.msg', recursive=True)

def diction(input_dir, emails):
    # emails = [os.path.join(input_dir,f) for f in os.listdir(input_dir)]    
    all_words = []       
    for mail in emails:    
        #with open(mail, encoding='ISO-8859-1') as m:
        outlook = wc.Dispatch("Outlook.Application").GetNamespace("MAPI")
        msg = outlook.OpenSharedItem(mail)
        for i,line in enumerate(msg.Body):
            if i == 2:  # if start at third line
                words = line.split()
                all_words += words
        del outlook, msg
    dictionary = col.Counter(all_words)
    #list_to_remove = dictionary.keys()
    #for item in list_to_remove:
    #    if item.isalpha() == False: 
    #        del dictionary[item]
    #    elif len(item) == 1:
    #        del dictionary[item]
    #dictionary = dictionary.most_common(3000) 
    return dictionary

emaildict = diction(input_dir, emails)

keyword = 'Wednesday'

outlook = wc.Dispatch("Outlook.Application").GetNamespace("MAPI")
msg1 = outlook.OpenSharedItem(r"H:\Enforcement\1 Current Contacts for CRM list.msg")
if keyword in msg1.Body: print('yes')
else: print('no')
del outlook, msg1

outlook = wc.Dispatch("Outlook.Application").GetNamespace("MAPI")
msg2 = outlook.OpenSharedItem(r"H:\Enforcement\2 FW Last chance to book.msg")
if keyword in msg2.Body: print('yes')
else: print('no')
del outlook, msg2

outlook = wc.Dispatch("Outlook.Application").GetNamespace("MAPI")
msg3 = outlook.OpenSharedItem(r"H:\Enforcement\3 Easter Party.msg")
if keyword in msg3.Body: print('yes')
else: print('no')
del outlook, msg3

file = 'H:\Enforcement\1 Current Contacts for CRM list.msg'

def testmsg(msg, file):
    if keyword in msg.Body: print('yes')
    else: print('no')

###############################################################################

import csv, time, win32com.client as wc

filtered = {}
start_time = time.time()
#keywords = ['chlo', 'risk', 'consumer benefit'] # can be partial but keep lowercase to match all cases
keywords = ['legal', 'risk', 'consumer benefit']

def ftest(keyword):
    outlook = wc.Dispatch("Outlook.Application").GetNamespace("MAPI")
    inbox = outlook.GetDefaultFolder(6) # 6 is the Inbox default folder index 
    searchdir = inbox.Folders['Enforcement']
    messages=searchdir.Items
    for msg in messages:
        for keyword in keywords:
            if keyword in msg.Body.lower():
                if keyword in filtered.keys():
                    filtered[keyword].append(msg.Subject)
                else:
                    filtered[keyword] = [msg.Subject]

ftest(keywords)
print("==== %s seconds ====" % round(time.time() - start_time))
# 6,170 files x 2 keywords in 64 seconds, 3 more in 80 seconds

with open('H:/Enforcement/filtered.csv', mode = 'w', newline = '') as out:
    cw = csv.writer(out, delimiter=',')
    for k,v in filtered.items():
        cw.writerow([k] + [len(v)] + v)

###############################################################################

filtered2 = {}
keywords = ['jeremy', 'nicky', 'chlo']
outlook = wc.Dispatch("Outlook.Application").GetNamespace("MAPI")
msg1 = list(outlook.OpenSharedItem(r"H:\Enforcement\c1.msg")) # this object does not support enumeration
msg2 = outlook.OpenSharedItem(r"H:\Enforcement\c2.msg")
msg3 = outlook.OpenSharedItem(r"H:\Enforcement\c3.msg")
msg4 = outlook.OpenSharedItem(r"H:\Enforcement\c4.msg")
msg5 = outlook.OpenSharedItem(r"H:\Enforcement\c5.msg")
for msg in [msg1, msg2, msg3, msg4, msg5]:
    for keyword in keywords:
        if keyword in msg.Body.lower():
            if keyword in filtered2.keys():
                filtered2[keyword].append(msg.Subject)
            else:
                filtered2[keyword] = [msg.Subject]
    
#from email.message import EmailMessage
file_path= 'H:\\Enforcement\\c1.msg'
mail = open(file_path, encoding='Latin-1')
mail_contents = mail.read()
print(mail_contents)

import csv, time, win32com.client as wc
outlook = wc.Dispatch("Outlook.Application").GetNamespace("MAPI")
for i in range(100):
    try:
        box = outlook.GetDefaultFolder(i)
        name = box.Name
        print(i, name) # 3-6, 9-17, 19-23, 25-26, 28, 31, 33, 35-36, 38
    except:
        pass
del outlook, box, name, i


#for folder in inbox.Folders:
#    print(folder.Name)

#print (msg.SenderName)
#print (msg.SenderEmailAddress)
#print (msg.SentOn)
#print (msg.To)
#print (msg.CC)
#print (msg.BCC)
#print (msg.Subject)
#print (msg.Body)
#count_attachments = msg.Attachments.Count
#if count_attachments > 0:
#    for item in range(count_attachments):
#        print (msg.Attachments.Item(item + 1).Filename)
