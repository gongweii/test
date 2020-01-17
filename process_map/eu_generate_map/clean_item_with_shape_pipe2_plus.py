#!/user/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------
# File       : clean_item_with_shape_pipe2_plus.py
# Author     : 
# Copyright  : Dynamic Technology Lab Pte Ltd
# Description: TODO
# Created    : 
# Revision   : none
#----------------------------------------------------------------------

SIMILARITY = 0.4

# filter some invalid company by company name's shape
def compare_by_shape(org,ticker):
  first_alpha = ticker[0].lower()
  if org.find(first_alpha) != -1: 
    pre_index = org.find(first_alpha) + 1 
    ticker_index = [0] 
    for c in ticker[1:].lower():
      ticker_index.append(org.lower().find(c,pre_index))
      pre_index = max(pre_index, org.lower().find(c,pre_index)) + 1
    if float(len([x for x in ticker_index if x != -1]))/len(ticker) >= 0.6:
      return True
  return False

eusa_auto_file = "res/pipe2/eusa_auto"
eusa_auto = list()
with open(eusa_auto_file,"r",encoding="utf-8") as inf:
  for line in inf:
    org_name = line.split("|")[1].strip()
    ticker = line.split("|")[2].strip()
    ticker_body = ticker.split(".")[0].strip()
    flag = compare_by_shape(org_name,ticker_body)
    if flag == False:
      print(org_name + "  " + ticker)

