#!/user/bin/env python                                                                                                                                   
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------
# File       : frequent_itemset_mining_pipe2.py
# Author     : 
# Copyright  : Dynamic Technology Lab Pte Ltd
# Description: TODO
# Created    : 
# Revision   : none
#----------------------------------------------------------------------

import ticker_extract as te
from collections import Counter

# Make sure Confidence > 0.2
FREQ_NUM = 0.2

eusa_one_NEREntity_file = "res/pipe1/eusa_one_NEREntity"
ticker_set = set()                
eusa_one_NEREntity_list = list()  
with open(eusa_one_NEREntity_file,'r',encoding='utf-8') as inf:
  for line in inf:
    ticker = line.split("|")[2].strip()
    ticker_set.add(ticker)
    eusa_one_NEREntity_list.append(line.strip())

#### frequent items mining
def frequent_items(ticker):
  line_of_ticker = list()
  flag = False
  for line in eusa_one_NEREntity_list:
    if line.split("|")[2].strip() == ticker:
      clean_line = line.split("|")[0].strip() + "|" + te.clean_company_name(line.split("|")[1]) + "|" + ticker
      line_of_ticker.append(clean_line.strip())
      flag = True
    if flag and line.split("|")[2].strip() != ticker:
      break
  ### caculate Confidence: support(org U ticker)/support(ticker)
  total_num = len(line_of_ticker)
  line_of_ticker_dict = Counter(line_of_ticker)
  line_of_ticker_dict = {key:value/float(total_num) for key,value in line_of_ticker_dict.items()}
  freq_items = [key for key,value in line_of_ticker_dict.items() if value > FREQ_NUM]  
  
  return freq_items

#### write result 
eusa_auto_file = "res/pipe2/eusa_auto"
def write_map(flag,freq_items):
  with open(eusa_auto_file,"a",encoding="utf-8") as outf:
    if len(all_freq_items) > 0:
      for output_line in all_freq_items:
        print(output_line.strip('\n'),file=outf)

all_freq_items = list()
miss_ticker_set = set()
repeat_org_set = set()
org_set = set()
miss_num = 0
repeat_num = 0
for ticker in ticker_set:
  freq_items = frequent_items(ticker)
  ## If some ticker can't fulfil Confidence > FREQ_NUM, record it
  if len(freq_items) == 0:
    miss_ticker_set.add(ticker)
    miss_num += 1
    print("miss_num: ",miss_num)
  else:
    for item in freq_items:
      org_name = item.split("|")[1].strip()
      if org_name not in org_set:
        org_set.add(org_name)
        all_freq_items.append(str(1)+"|"+org_name+"|"+ticker)
      ## If exists same company name -> multiple tickers conflicts,record it
      else:  
        repeat_org_set.add(org_name)
        repeat_num += 1
        print("repeat_num: ",repeat_num)

write_map(1,all_freq_items)

print("There is some ticker does not have freq items,total ",len(miss_ticker_set))
print(miss_ticker_set)
print("there is some org has different ticker,total ",len(repeat_org_set))
print(repeat_org_set)
