#!/user/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------
# File       : gen_ticker_auto_from_mtd.py
# Author     : 
# Copyright  : Dynamic Technology Lab Pte Ltd                                                                                                                                                         
# Description: TODO
# Created    : 
# Revision   : none
#----------------------------------------------------------------------

import pdb
import os
import json
import bing as bi
import ticker_extract as te 

### find ticker from ref clean_company_name
def find_ticker_from_ref(org_name_set,ref_ticker_dict):
  for org_mtd in org_name_set:
    if org_mtd.lower() in ref_ticker_dict:
      return ref_ticker_dict.get(org_mtd.lower())
    if te.clean_company_name(org_mtd) in ref_ticker_dict:
      return ref_ticker_dict.get(te.clean_company_name(org_mtd))
  return None

### find ticker from ticker_core
def find_ticker_from_core(org_name_set,ticker_core_dict):
  for org_mtd in org_name_set:
    if org_mtd.lower() in ticker_core_dict:
      return ticker_core_dict.get(org_mtd.lower())
    if te.clean_company_name(org_mtd) in ticker_core_dict:
      return ticker_core_dict.get(te.clean_company_name(org_mtd))
  return None

### find ticker from ticker_auto
def find_ticker_from_auto(org_name_set,ticker_auto_dict):
  for org_mtd in org_name_set: 
    if org_mtd.lower() in ticker_auto_dict:
      return ticker_auto_dict.get(org_mtd.lower())
    if te.clean_company_name(org_mtd) in ticker_auto_dict:
      return ticker_auto_dict.get(te.clean_company_name(org_mtd))
  return None

	
### read ref_ticker csv files
ref_ticker_dir = 'mtd/ref_ticker_name'
ref_ticker_dict = {}

for file_name in os.listdir(ref_ticker_dir):
  path = os.path.join(ref_ticker_dir,file_name)
  with open(path,'r',encoding='utf-8') as inf:
    for line in inf:
      ticker = line.split('"')[1].strip()
      org_name = line.split('"')[3].strip()
      if ticker == 'Symbol':
        continue
      if ticker.find('^') != -1: 
        continue
      if org_name not in ref_ticker_dict:
        ref_ticker_dict[org_name.lower()] = ticker

### read ticker_core file
ticker_core_file = '../../map/us_core'
ticker_core_dict = {}
with open(ticker_core_file,'r',encoding='utf-8') as inf:
  for line in inf:
    org_name = line.split('|')[1].strip()
    ticker = line.split('|')[2].strip()
    if org_name not in ticker_core_dict:
      ticker_core_dict[org_name] = ticker

### read ticker_auto file
ticker_auto_file = '../../map/us_auto'
ticker_by_mtd_file = 'ticker_by_mtd'
ticker_auto_dict = {}
with open(ticker_auto_file,'r',encoding='utf-8') as inf:
  for line in inf:
    org_name = line.split('|')[1].strip()
    ticker = line.split('|')[2].strip()
    if org_name not in ticker_auto_dict:
      ticker_auto_dict[org_name] = ticker

### paste result , record as ticker_auto
def write_ticker_auto_file(ticker_symbols,org_all_set,bbid,ticker_by_mtd_file,ticker_all_dict,flag):				
  for org_mtd in org_all_set:
    with open(ticker_by_mtd_file, 'a') as outfile:
      if (org_mtd not in ticker_all_dict) and (org_mtd != "") and (bbid != -1):
        output_lines = str(flag) + '|' + org_mtd.lower().strip() + '|' + ticker_symbols.strip() + '|' + bbid.strip()
        print(output_lines.strip(),file=outfile)

### traverse mtd_sample dir and read json file
mtd_sample_dir = 'mtd/dump_info'
ticker_all_dict = dict(ticker_core_dict, **ticker_auto_dict)
mtd_sample_dict = {}
num = 1
for file_name in os.listdir(mtd_sample_dir):
  print("The mtd_sample: "+str(num))
  path = os.path.join(mtd_sample_dir,file_name)

  try:
    with open(path, 'r', encoding='utf-8') as inf:
      temp = json.load(inf)
      ticker_symbols = temp['ticker_symbols']
      aliases = temp['aliases']
      associated_domains = temp['associated_domains']
      previous_names = temp['previous_names']
      org_all_set = set(aliases + previous_names + associated_domains)
      org_name_set = set(aliases + previous_names)
      if ticker_symbols == []:
        # step 1 search in ref_ticker_name
        ticker_symbols = find_ticker_from_ref(org_name_set,ref_ticker_dict)
        if type(ticker_symbols) == type(None):
          # step 2 search in ticker core
          ticker_symbols = find_ticker_from_core(org_name_set,ticker_core_dict)
          if type(ticker_symbols) == type(None):
            # step 3 call bing search API to search
            ticker_symbols = bi.crawler(org_name_set)
            if type(ticker_symbols) == type(None):
              # step 4 search in ticker_auto
              ticker_symbols = find_ticker_from_auto(org_name_set,ticker_auto_dict)
              if type(ticker_symbols) == type(None):
                with open('miss_symbol','a') as outf:
                  print(file_name,file = outf)
                  print("The mtd_sample: "+str(num)+" ticker_symbols search failure") 
                continue
  except:
    print("file"+str(file_name)+"not exsists")
    continue

  num = num + 1      
  bbid = te.find_bbid_by_ticker_and_date(ticker_symbols)
  # 3|org|ticker
  write_ticker_auto_file(ticker_symbols,org_all_set,bbid,ticker_by_mtd_file,ticker_all_dict,3)  
