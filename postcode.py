# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 10:34:32 2019

@author: McCabeR
"""

import re

s="123 Some Road Name\nTown, City\nCounty\nPA23 6NH\n123 Some Road Name\nTown, City County\nPA2 6NH\n123 Some Road Name\nTown, City\nCounty\nPA2Q 6NH"
re.findall(r'\b[A-Z]{1,2}[0-9][A-Z0-9]? [0-9][ABD-HJLNP-UW-Z]{2}\b', s) 
re.findall(r'[A-Z]{1,2}[0-9R][0-9A-Z]? [0-9][A-Z]{2}', s)

ADDRESS="""123 Some Road Name
Town, City
County
PA23 6NH"""

# or

reobj = re.compile(r'(\b[A-Z]{1,2}[0-9][A-Z0-9]? [0-9][ABD-HJLNP-UW-Z]{2}\b)')
matchobj = reobj.search(ADDRESS)
if matchobj:
    print(matchobj.group(1))

# O'Reilly - see BS7666
# ^[A-Z]{1,2}[0-9R][0-9A-Z]?●[0-9][ABD-HJLNP-UW-Z]{2}$
# or to catch all exceptions using classes, anchors, alternation, grouping and repetition
# ^(?:(?:[A-PR-UWYZ][0-9]{1,2}|[A-PR-UWYZ][A-HK-Y][0-9]{1,2} |[A-PR-UWYZ][0-9][A-HJKSTUW]|[A-PR-UWYZ][A-HK-Y][0-9] [ABEHMNPRV-Y])●[0-9][ABD-HJLNP-UW-Z]{2}|GIR 0AA)$

# or [A-Z]([A-Z](d{1,2}|d[A-Z])|d{1,2})sd[A-Z]{2}
