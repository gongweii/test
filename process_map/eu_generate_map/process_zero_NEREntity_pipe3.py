#!/user/bin/env python                                                                                                                                       
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------
# File       : process_zero_NEREntity_pipe3.py
# Author     : 
# Copyright  : Dynamic Technology Lab Pte Ltd
# Description: TODO
# Created    : 
# Revision   : none
#----------------------------------------------------------------------

#### write file
miss_file = "res/pipe3/miss"
def write_miss(line):
  with open(miss_file,"a",encoding="utf-8") as outf:
    print(line.strip('\n'),file=outf)

error_file = "res/pipe3/error"
def write_error(line,org_set,ticker_set):
  with open(error_file,"a",encoding="utf-8") as outf:
    output_line = line.strip('\n') + "|" + ",".join(org_set) + "|" + ",".join(ticker_set)
    print(output_line.strip('\n'),file = outf)

right_file = "res/pipe3/right"
def write_right(line,org_set,ticker_set):
  with open(right_file,"a",encoding="utf-8") as outf:
    output_line = line.strip('\n') + "|" + ",".join(org_set) + "|" + ",".join(ticker_set)
    print(output_line.strip('\n'),file = outf)

perfect_file = "res/pipe3/perfect"
def write_perfect(line,org_set,ticker_set):
  with open(perfect_file,"a",encoding="utf-8") as outf:
    output_line = line.strip('\n') + "|" + ",".join(org_set) + "|" + ",".join(ticker_set)
    print(output_line.strip('\n'),file = outf)

#### read ticker_core_eu_tmp
auto_dict = {}
eusa_file = "../../map/eusa_auto"
with open(eusa_file,"r",encoding="utf-8") as inf:
  for line in inf:
    print(line)
    auto_dict[line.split("|")[1].strip()] = line.split("|")[2].strip()

#### Search company name in map directly and records result
miss_num = 0
right_num = 0
perfect_num = 0
error_num = 0
ticker_zero_NEREntity_file = "res/pipe1/eusa_zero_NEREntity"
with open(ticker_zero_NEREntity_file,"r",encoding="utf-8") as inf:
  for i,line in enumerate(inf):
    if i%100 == 0:
      print("error: ",error_num)
      print("miss: ",miss_num)
      print("right: ",right_num)
      print("perfect: ",perfect_num)
    org_set = set()
    ticker_set = set()
    headline = line.split("|")[1].lower().strip()
    ticker = line.split("|")[2].strip()
    for key,value in auto_dict.items():
      location = headline.find(key)
      if(location!=-1 and (location == 0 or not headline[location-1].isalpha()) and (location+len(key) == len(headline) or not headline[location+len(key)].isalpha())):   
        org_set.add(key)
        ticker_set.add(value)
    ## If just one company can be found in map len(ticker) = 1, records as perfect
    if len(ticker_set) == 1 and ''.join(ticker_set) == ticker:
      write_perfect(line,org_set,ticker_set)
      perfect_num += 1
    ## If one or more companies can be found in map,but related ticker is not wanted, records as error
    if len(ticker_set) == 1 and ''.join(ticker_set) != ticker:
      write_error(line,org_set,ticker_set)
      error_num += 1
    ## If can't find any ticker in map, records as missing
    if len(ticker_set) == 0:
      write_miss(line)
      miss_num += 1
    ## If more than one companies can be found in map and only one is wanted, records as right
    if len(ticker_set) > 1:
      for i in range(len(list(ticker_set))):
        if list(ticker_set)[i] == ticker:
          write_right(line,org_set,ticker_set)
          right_num += 1
          break
        if list(ticker_set)[i] != ticker and i == len(list(ticker_set)) - 1:
          write_error(line,org_set,ticker_set)
          error_num += 1


















