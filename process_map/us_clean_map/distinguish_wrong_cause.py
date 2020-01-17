#!/user/bin/env python
# -*- coding:utf-8 -*-
#----------------------------------------------------------------------
# File       : distinguish_wrong_cause.py
# Author     : 
# Copyright  : Dynamic Technology Lab Pte Ltd
# Description: TODO
# Created    : 
# Revision   : none
#----------------------------------------------------------------------
import pdb

### write wrong data(classified as error and miss) caused by NER into file
### parameter flag 1: Generated from bf_error, flag 2: Generated from bf_miss,flag 3: Generated from rp_error,flag 4: Generated from rp_miss
error_data_by_ner_file = "wrong_by_ner"
def write_wrong_data_by_ner(headline,org_name,ticker, flag):
  with open(error_data_by_ner_file, "a", encoding="utf-8") as outf:
    output_line = str(flag) + "|" + headline + "|" + org_name.lower() + "|" + ticker
    print(output_line, file=outf)

### write wrong data caused by map into file
error_data_by_map_file = "wrong_by_map"
def write_wrong_data_by_map(headline,ticker,flag,wrong_org="", wrong_ticker=""):
  with open(error_data_by_map_file, "a", encoding="utf-8") as outf:
    if wrong_org == "" and wrong_ticker == "":
      output_line = str(flag) + "|" + headline + "|" + ticker
      print(output_line, file=outf)
    else:
      output_line = str(flag) + "|" + headline + "|" + ticker + "|" + wrong_org.lower() + "|" + wrong_ticker
      print(output_line, file=outf)

### write not exists ticker into file
not_exists_ticker_file = "not_exists_ticker"
def write_not_exists_ticker(headline,ticker,flag):
  with open(not_exists_ticker_file, "a", encoding="utf-8") as outf:
    output_line = str(flag) + "|" + headline + "|" + ticker
    print(output_line, file=outf)

### generate a dictionary. format: {ticker_i:[org_name_i1,org_name_i2,...,org_name_ij,...]}
ticker_core_file = "ticker_core_1.1"
ticker_auto_by_shape_file = "ticker_auto_by_shape"
ticker_auto_by_mtd_file = "ticker_by_mtd"

all_dict = {}
with open(ticker_core_file, "r", encoding="utf-8") as inf:
  for line in inf:
    org_name = line.split("|")[1].strip()
    ticker = line.split("|")[2].strip()
    if ticker not in all_dict:
      all_dict[ticker] = [org_name]
    if ticker in all_dict and org_name not in all_dict[ticker]:
      all_dict[ticker].append(org_name)
with open(ticker_auto_by_shape_file, "r", encoding="utf-8") as inf:
  for line in inf:
    org_name = line.split("|")[1].strip()
    ticker = line.split("|")[2].strip()
    if ticker not in all_dict:
      all_dict[ticker] = [org_name]
    if ticker in all_dict and org_name not in all_dict[ticker]:
      all_dict[ticker].append(org_name)
with open(ticker_auto_by_mtd_file, "r", encoding="utf-8") as inf:
  for line in inf:
    org_name = line.split("|")[1].strip()
    ticker = line.split("|")[2].strip()
    if ticker not in all_dict:
      all_dict[ticker] = [org_name]
    if ticker in all_dict and org_name not in all_dict[ticker]:
      all_dict[ticker].append(org_name)

### Distinguish wrong data from bf_data_error caused by NER or map
bf_error_file = "bf_train_data_result_all_error"
with open(bf_error_file, "r", encoding="utf-8") as inf:
  for line in inf:
    headline = line.split("|")[1].strip().lower()
    ticker = line.split("|")[2]
    wrong_org = line.split("|")[5].strip()
    wrong_ticker = line.split("|")[6].strip()
    org_set = all_dict.get(ticker,-1)
    if org_set == -1:
      print("Do not contain ticker: " + ticker + " in all map")
      write_not_exists_ticker(line.split("|")[1].strip(),ticker,1)
      continue
    by_ner = False
    for org in org_set:
      location = headline.find(org)
      if(location!=-1 and (location == 0 or not headline[location-1].isalpha()) and (location+len(org) == len(headline) or not headline[location+len(org)].isalpha())):
        write_wrong_data_by_ner(line.split("|")[1].strip(),org,ticker, 1)
        by_ner = True
        break
    if by_ner == False:
      write_wrong_data_by_map(line.split("|")[1].strip(),ticker,1,wrong_org,wrong_ticker) 

### Distinguish wrong data from rp_data_error caused by NER or map
rp_error_file = "rp_train_data_result_all_error"
with open(rp_error_file, "r", encoding="utf-8") as inf:
  for line in inf:
    headline = line.split("|")[1].strip().lower()
    ticker = line.split("|")[2]
    wrong_org = line.split("|")[5].strip()
    wrong_ticker = line.split("|")[6].strip()
    org_set = all_dict.get(ticker,-1)
    if org_set == -1: 
      print("Do not contain ticker: " + ticker + " in all map")
      write_not_exists_ticker(line.split("|")[1].strip(),ticker,3)
      continue
    by_ner = False
    for org in org_set:
      location = headline.find(org)
      if(location!=-1 and (location == 0 or not headline[location-1].isalpha()) and (location+len(org) == len(headline) or not headline[location+len(org)].isalpha())):
        write_wrong_data_by_ner(line.split("|")[1].strip(),org,ticker, 3)
        by_ner = True
        break
    if by_ner == False:
      write_wrong_data_by_map(line.split("|")[1].strip(),ticker,3,wrong_org,wrong_ticker) 

### Distinguish wrong data from bf_data_missing caused by NER or map
bf_missing_file = "bf_train_data_result_all_missing" 
with open(bf_missing_file, "r", encoding="utf-8") as inf:
  for line in inf:
    headline = line.split("|")[1].strip().lower()
    ticker = line.split("|")[2]
    org_set = all_dict.get(ticker,-1)
    if org_set == -1:
      print("Do not contain ticker: " + ticker + " in all map")
      write_not_exists_ticker(line.split("|")[1].strip(),ticker,2)
      continue
    by_ner = False
    for org in org_set:
      location = headline.find(org)
      if(location!=-1 and (location == 0 or not headline[location-1].isalpha()) and (location+len(org) == len(headline) or not headline[location+len(org)].isalpha())):
        write_wrong_data_by_ner(line.split("|")[1].strip(),org,ticker,2)
        by_ner = True
        break
    if by_ner == False:
      write_wrong_data_by_map(line.split("|")[1].strip(),ticker,2) 

### Distinguish wrong data from rp_data_missing caused by NER or map
rp_missing_file = "rp_train_data_result_all_missing"
with open(bf_missing_file, "r", encoding="utf-8") as inf:
  for line in inf:
    headline = line.split("|")[1].strip().lower()
    ticker = line.split("|")[2]
    org_set = all_dict.get(ticker,-1)
    if org_set == -1:
      print("Do not contain ticker: " + ticker + " in all map")
      write_not_exists_ticker(line.split("|")[1].strip(),ticker,4)
      continue
    by_ner = False
    for org in org_set:
      location = headline.find(org)
      if(location!=-1 and (location == 0 or not headline[location-1].isalpha()) and (location+len(org) == len(headline) or not headline[location+len(org)].isalpha())):
        write_wrong_data_by_ner(line.split("|")[1].strip(),org,ticker,4)
        by_ner = True
        break
    if by_ner == False:
      write_wrong_data_by_map(line.split("|")[1].strip(),ticker,4) 
