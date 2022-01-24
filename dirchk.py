# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 14:42:59 2019

@author: McCabeR
"""

# test to interrogate the EHL folders on K: for a given month and return the gaps, i.e. missing days not gathered

def gather_test(month='08'):
    import glob
    chk_folder = 'K:/User Centred Data Services/Beta/All Data/Data Import Staging/gather/energy_helpline/domestic_tariffs/2019/' + month
    reports_list = glob.glob(chk_folder + '**/*', recursive=False)
    lst=[int(i[-2:]) for i in reports_list]
    return([x for x in range(lst[0], lst[-1]+1) if x not in lst])

gather_test() # [] blank uses default => no missing dates so far in August
gather_test('06') # [20, 21, 22, 23] => four dates in June
