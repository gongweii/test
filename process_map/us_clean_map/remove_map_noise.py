#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------
# File       : remove_map_noise_by_bf.py
# Author     : 
# Copyright  : Dynamic Technology Lab Pte Ltd
# Description: TODO
# Created    : Tue 18 Jun 2019 04:27:46 PM SGT
# Revision   : none
#----------------------------------------------------------------------
import pdb

### output dictionary with format: {ticker:[org_name1,org_name2,...]}
def read_map_to_dict(map_file):
  map_dict = {}
  with open(map_file, "r", encoding="utf-8") as inf:
    for line in inf:
      org_name = line.split("|")[1].strip()
      ticker = line.split("|")[2].strip()
      if ticker not in map_dict:
        map_dict[ticker] = [org_name]
      else:
        map_dict[ticker].append(org_name)
  return map_dict

### merge two dictionary
### format of dict one or dict two:{ticker:[org_name1,org_name2,...]}
def merge_dict(one,two):
  # merge one dict and two dict according one dict's keys
  merge_dict = {key: value + two.get(key,[]) for key, value in one.items()}
  # avoid some key in two dict but not in one dict
  merge_dict = dict(merge_dict,**{key: two[key] if key not in merge_dict else merge_dict[key] for key in two.keys()})
  # remove duplicate org name
  merge_dict = {key:list(set(value)) for key,value in merge_dict.items()}
  return merge_dict
  
ticker_core_file = "ticker_core_1.1"
ticker_by_mtd_file = "ticker_by_mtd"
ticker_auto_by_shape_file = "ticker_auto_by_shape_old"                         # cat ticker_auto ticker_by_shape > ticker_auto_by_shape_old
ticker_core_dict = read_map_to_dict(ticker_core_file)
ticker_by_mtd_dict = read_map_to_dict(ticker_by_mtd_file)
ticker_auto_by_shape_dict = read_map_to_dict(ticker_auto_by_shape_file)

tmp_dict = merge_dict(ticker_core_dict,ticker_by_mtd_dict)
all_map_dict = merge_dict(tmp_dict,ticker_auto_by_shape_dict)

### Extract org name which leads to classification as perfect
def get_perfect_org_set(perfect_file,all_map_dict):                            # parameter perfect_file:bf_data_perfect path or rp_data_perfect path
  perfect_set = set()
  with open(perfect_file,'r',encoding="utf-8") as inf:
    for line in inf:
      ticker = line.split("|")[2].strip()
      org_str = line.split("|")[5].lower().strip()
      org_list = org_str.split(",")
      if ticker in all_map_dict:
        for org in org_list:
          if org in all_map_dict[ticker]:
            perfect_set.add(org)
  return perfect_set

bf_perfect_file = "bf_train_data_result_all_perfect"
rp_perfect_file = "rp_train_data_result_all_perfect"
bf_perfect_set = get_perfect_org_set(bf_perfect_file,all_map_dict)
rp_perfect_set = get_perfect_org_set(rp_perfect_file,all_map_dict)
perfect_set = bf_perfect_set|rp_perfect_set                                    # merge bf_perfect_set and rp_perfect_set

### start clean map
# read ticker_auto_by_shape_old
ticker_auto_by_shape = []
ticker_auto_by_shape_file = "ticker_auto_by_shape_old"
with open(ticker_auto_by_shape_file,"r") as inf:
  for line in inf:
    ticker_auto_by_shape.append(line)
  ticker_auto_by_shape = list(set(ticker_auto_by_shape))

# approch of cleaning ticker_auto_by_shape_old map: clean org name which from bf_org_frequence but can't be found in perfect_set
bf_org_dict_file = "bf_org_frequence"
i = 0
with open(bf_org_dict_file,"r") as inf:
  for line in inf:
    try:
      org_first_index = line.index("('")+2
      org_end_index = line.index("',") 
    except ValueError:
      if '("' in line or '",' in line:
        org_first_index = line.index('("')+2
        org_end_index = line.index('",')
      else:
        continue
    org = line[org_first_index:org_end_index].lower().strip()
    for line in ticker_auto_by_shape:
      if line.split("|")[1].strip() == org and line.split("|")[1].strip() != line.split("|")[2].lower().strip() and org not in perfect_set:
        ticker_auto_by_shape.remove(line)
        i += 1
        print("clean map with bf_org_frequence: "+str(i))

# approch of cleaning ticker_auto_by_shape_old map: clean org name which from rp_org_frequence but can't be found in perfect_set
rp_org_dict_file = "rp_org_frequence"
i = 0
with open(rp_org_dict_file,"r") as inf:
  for line in inf:
    try:
      org_first_index = line.index("('")+2
      org_end_index = line.index("',")
    except ValueError:
      if '("' in line or '",' in line:
        org_first_index = line.index('("')+2
        org_end_index = line.index('",')
      else:
        continue
    org = line[org_first_index:org_end_index].lower().strip()
    for line in ticker_auto_by_shape:
      if line.split("|")[1].strip() == org and line.split("|")[1].strip() != line.split("|")[2].lower().strip() and org not in perfect_set:
        ticker_auto_by_shape.remove(line)
        i += 1
        print("clean map with rp_org_frequence: "+str(i))

### wirte cleaned ticker_auto_by_shape into file
cleaned_ticker_auto_by_shape_file = "ticker_auto_by_shape"
with open(cleaned_ticker_auto_by_shape_file,"a") as outf:
  for line in ticker_auto_by_shape:
    print(line.strip(),file = outf)
         
