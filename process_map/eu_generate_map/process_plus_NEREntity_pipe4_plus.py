#!/user/bin/env python                                                                                                                                             
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------
# File       : process_plus_NEREntity_pipe4_plus.py
# Author     : 
# Copyright  : Dynamic Technology Lab Pte Ltd
# Description: TODO
# Created    : 
# Revision   : none
#----------------------------------------------------------------------

import ticker_extract as te

#### write file
miss_file = "res/pipe4/miss1"
def write_miss(line):
  with open(miss_file,"a",encoding="utf-8") as outf:
    print(line.strip("\n"),file=outf)

right_file = "res/pipe4/right1"
def write_right(line,ticker_set):
  with open(right_file,"a",encoding="utf-8") as outf:
    output_line = line.strip("\n") + "|" + ','.join(ticker_set)
    print(output_line,file=outf)

error_file = "res/pipe4/error1"
def write_error(line,ticker_set):
  with open(error_file,"a",encoding="utf-8") as outf:
    output_line = line.strip("\n") + "|" + ','.join(ticker_set)
    print(output_line,file=outf)

perfect_file = "res/pipe4/perfect1"
def write_perfect(line,ticker_set):
  with open(perfect_file,"a",encoding="utf-8") as outf:
    output_line = line.strip("\n") + "|" + ','.join(ticker_set)
    print(output_line,file=outf)

#### read map
eusa_auto_file = "../../map/eusa_auto"
eusa_dict = {}
with open(eusa_auto_file,"r",encoding="utf-8") as inf:
  for line in inf:
    eusa_dict[line.split("|")[1].strip()] = line.split("|")[2].strip()

#### Search company name in map directly and records results
eusa_plus_NEREntity_file = "res/pipe1/eusa_plus_NEREntity"
with open(eusa_plus_NEREntity_file,"r",encoding="utf-8") as inf:
  for i,line in enumerate(inf):
    org_str = line.split("|")[1].strip()
    ticker = line.split("|")[2].strip()
    org_list = org_str.split(",")
    org_list = [te.clean_company_name(org) for org in org_list]
    ticker_set = set()
    for org in org_list:
      for key,value in eusa_dict.items():
        location = org.find(key)
        if(location!=-1 and (location == 0 or not org[location-1].isalpha()) and (location+len(key) == len(org) or not org[location+len(key)].isalpha())):
          ticker_set.add(value)
    ## write matching results which include error, missing, right and perfect
    if len(ticker_set) == 0:
      write_miss(line)
    if len(ticker_set) == 1 and ''.join(ticker_set) == ticker:
      write_perfect(line,ticker_set)
    if len(ticker_set) == 1 and ''.join(ticker_set) != ticker:
      write_error(line,ticker_set)
    if len(ticker_set) > 1 and ticker in ticker_set:
      write_right(line,ticker_set)
    if len(ticker_set) > 1 and ticker not in ticker_set:  
      write_error(line,ticker_set)
