#!/user/bin/env python                                                                                                                                             
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------
# File       : gen_bbid_map_pipe5.py
# Author     : 
# Copyright  : Dynamic Technology Lab Pte Ltd
# Description: Generate bloomberg id map 
# Created    : 
# Revision   : none
#----------------------------------------------------------------------

#### read train dataset and records bbid
train_data_file = "../../eu_data/ns_eu_till_2015"
conflict_ticker = set()
bbid_ticker_dict = {}
with open(train_data_file,"r",encoding="utf-8") as inf:
  for line in inf:
    ticker = line.split("|")[2].strip()
    bbid = line.split("|")[3].strip()
    if ticker not in bbid_ticker_dict:
      bbid_ticker_dict[ticker] = bbid
    else:
      if bbid != bbid_ticker_dict.get(ticker):
        conflict_ticker.add(ticker)

#### records that same ticker -> multiple bbid
conflict_date = {}
with open(train_data_file,"r",encoding="utf-8") as inf:
  for line in inf:
    date = line.split("|")[0].strip()
    ticker = line.split("|")[2].strip()
    bbid = line.split("|")[3].strip()
    if ticker in conflict_ticker:
      if bbid not in conflict_date:
        conflict_date[bbid] = [date]
      else:
        if date not in conflict_date[bbid]:
          conflict_date[bbid].append(date)

## some diffrent time & same ticker -> multiple bbid conflict is normal, these conflicts can be solved by modify bbid map
## some same time & same ticker -> multiple bbid conflict is wrong
for key,value in conflict_date.items():
  print("bbid: ",key)
  print("date: ",sorted(value))

#### paste result
eusa_bbid_ticker_with_date_range_file = "res/pipe5/euns_bbid_ticker_with_date_range"
with open(eusa_bbid_ticker_with_date_range_file,"a",encoding="utf-8") as outf:
  for key,value in bbid_ticker_dict.items():
    output_line = value + "|" + key + "|" + "20060101|20151231"
    print(output_line,file = outf)



