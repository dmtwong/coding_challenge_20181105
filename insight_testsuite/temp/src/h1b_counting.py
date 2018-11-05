# -*- coding: utf-8 -*-
"""
Created on Sun Nov 04 18:43:39 2018

@author: David Wong
"""

import os
import pip

os.getcwd()
#os.listdir(os.getcwd())

#dir()

occup_dict = dict() # Key: JOB_TITLE, Value: certified Count 
state_dict = dict() # Key: WORKSITE_STATE, Value: Certified Count 
sorted_occup = sorted(occup_dict.keys())
sorted_state = sorted(state_dict.keys())

#input_hand = open(os.getcwd() + '/h1b_statistics-master/insight_testsuite/temp/input/h1b_input.csv', 'r')
#input_hand = open('.\\insight_testsuite\\h1b_input.csv', 'r')
#input_hand = open('/h1b_statistics-master/insight_testsuite/temp/input/h1b_input.csv', 'r')
os.chdir('src')
#os.chdir('..//input')
input_hand = open('..//input//h1b_input.csv', 'r')
#input_hand = open('h1b_input.csv', 'r')

col_name = input_hand.readline()
col_name = col_name.split(';')
#col_name
#len(col_name)

col_sele_name = [name in ['CASE_NUMBER', 'CASE_STATUS', 'SOC_NAME', 
                          'WORKSITE_STATE'] for name in col_name]
col_sele_ix = filter(lambda x: col_sele_name[x], range(len(col_sele_name)))
#col_sele_ix

def extract_ele(entry, ix):
    return entry[ix]
#line_list = []
   
def add_occup(new_occup):
    """ Assumes: new_occup is not in key of occup_dict
    new_occup is added as a new key with first count in value """
    occup_dict[new_occup] = 1
    sorted_occup.append(new_occup)
    sorted_occup.sort()

def add_state(new_state):
    """ Assumes: new_state is not in key of state_dict
    new_state is added as a new key with first count in value """
    state_dict[new_state] = 1
    sorted_state.append(new_state)
    sorted_state.sort()

class countDict(object):
    """ A Dictionary with integer keys (Count) 
    and string value (Occupation or States)
    for hash """
    def __init__(self, unique_Counts):
        """Create an empty dictionary"""
        self.count_lst = []        
        #unique = len(unique_Counts)
        for i in unique_Counts: 
            self.count_lst.append([i])         

    def add_ele(self, dict_key, dict_val):
        """ Assume dict_key is integer of frequency for specific occup/state_dict
        append specific occup/state_dict according to the correspondind counting bucket"""    
        list_freq = [item[0] for item in self.count_lst]
        this_hash_buck = self.count_lst[list_freq.index(dict_key)]        
        this_hash_buck.append((dict_val.replace('"',''),))
    
    def get_ele(self, dict_key):
        """ Assume the counting frequency is provided as key
        will return a sorted list of occup/state_dict that has the same count"""
        list_freq = [item[0] for item in self.count_lst]
        this_hash_buck = self.count_lst[list_freq.index(dict_key)]
        tmp = [item[0] for item in this_hash_buck[1:]]
        #tmp = tmp.replace('"','')
        return sorted(tmp)
    
    def get_length(self, dict_key):
        """ Count how many has same fre"""
        return len(self.get_ele(dict_key))
          
    def __str__(self):
        result = '{'
        for each_count in self.count_lst:
            for each_item in each_count:
                result = result + str(each_item) + ','
        return result[:-1] + '}' 

count_Cert = 0

for line in input_hand:
    line = line.split(';')
    this_record = [ line[i] for i in col_sele_ix ]
    # print(this_record)
    
    if extract_ele(this_record, 1) != 'CERTIFIED':
        break
    
    count_Cert += 1
    this_case_JOB   = extract_ele(this_record, 2)
    this_case_STATE = extract_ele(this_record, 3)
    
    if this_case_JOB not in sorted_occup:
        add_occup(this_case_JOB)
    else:
        occup_dict[this_case_JOB] += 1
        
    if this_case_STATE not in sorted_state:
        add_state(this_case_STATE)
    else:
        state_dict[this_case_STATE] += 1  

input_hand.close()

#occup_dict
#sorted_occup

## occupations based
list_occ_tuples = occup_dict.items()
occup_count_list = occup_dict.values()
occup_count_unique = sorted(set(occup_count_list), reverse = True)
list_occ_tuples = [(t[1], t[0]) for t in list_occ_tuples]

## state based
list_state_tuples = state_dict.items()
state_count_list = state_dict.values()
state_count_unique = sorted(set(state_count_list), reverse = True)
list_state_tuples = [(t[1], t[0]) for t in list_state_tuples]
'''
occup_count_unique
occup_count_list 
list_occ_tuples
'''

certfied_Count = sum([item[0] for item in list_occ_tuples])

top_occup_limit = 10
hash_Occup = countDict(occup_count_unique)
top_state_limit = 10
hash_State = countDict(state_count_unique)

for ele in list_occ_tuples:
    #print ele
    if top_occup_limit < 1:
        pass
    else:
        hash_Occup.add_ele(ele[0], ele[1])

for ele in list_state_tuples:
    #print ele
    if top_state_limit < 1:
        pass
    else:
        hash_State.add_ele(ele[0], ele[1])
'''        
print hash_Occup
print hash_State

hash_Occup.get_ele(1)
hash_State.get_ele(2)
'''
os.getcwd()

#os.chdir('output')
#output_file = open(os.getcwd() +'/Desktop/repeat_donors_99th.txt', 'w+')  
output_file = open('..//output//top_10_occupations.txt', 'w+')
#output_file = open('./output/top_10_occupations.txt', 'w+')
#output_file = open('top_10_occupations.txt', 'w+')
#output_file = open('//output//top_10_occupations.txt', 'w+')
output_file.write('TOP_OCCUPATIONS;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE\n')
for count in occup_count_unique:
    if top_occup_limit < 1:
        continue
    len_ele = hash_Occup.get_length(count)
    #print len_ele
    if len_ele == 1:
        top_occup_limit -= 1
        tmp = hash_Occup.get_ele(count)
        output_file.write(tmp[0] + ';' + str(count) + ';' + 
                          str(round(float(count) / certfied_Count * 100, 1)) + 
                          '%' + '\n')
    else:
        range_tmp = min(len_ele, top_occup_limit)
        tmp = hash_Occup.get_ele(count)
        for i in range(range_tmp):
            top_occup_limit -= 1
            perc_tmp = round(float(count) / certfied_Count * 100, 1)
            output_file.write(tmp[i] + ';' + str(count) + ';' + 
                          str(perc_tmp) + '%' + '\n')
output_file.close()

#output_file2 = open('top_10_states.txt', 'w+')
output_file2 = open('..//output//top_10_states.txt', 'w+')
#output_file2 = open('./output/top_10_states.txt', 'w+')
output_file2.write('TOP_STATES;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE\n')
for count in state_count_unique:
    if top_state_limit < 1:
        continue
    len_ele = hash_State.get_length(count)
    #print len_ele
    if len_ele == 1:
        top_state_limit -= 1
        tmp = hash_State.get_ele(count)
        output_file2.write(tmp[0] + ';' + str(count) + ';' + 
                          str(round(float(count) / certfied_Count * 100, 1)) + 
                          '%' + '\n')
    else:
        range_tmp = min(len_ele, top_state_limit)
        tmp = hash_State.get_ele(count)
        for i in range(range_tmp):
            top_state_limit -= 1
            perc_tmp = round(float(count) / certfied_Count * 100, 1)
            output_file2.write(tmp[i] + ';' + str(count) + ';' + 
                          str(perc_tmp) + '%' + '\n')
output_file2.close()
#os.chdir('..//')