#!/user/bin/env python
# -*- coding:utf-8 -*-

#----------------------------------------------------------------------
# File       : statistic_frequency_of_wrong_by_map.py
# Author     : 
# Copyright  : Dynamic Technology Lab Pte Ltd
# Description: wrong_by_map_file: statistic frequency of org name and ticker
# Created    : 
# Revision   : none
#----------------------------------------------------------------------
import pdb

wrong_by_map_file = "wrong_by_map"
bf_org_freq_file = "bf_org_frequence"
bf_ticker_freq_file = "bf_ticker_frequence"
rp_org_freq_file = "rp_org_frequence"
rp_ticker_freq_file = "rp_ticker_frequence"

### statistic frequence of org and ticker by wrong_by_map file
### parameter flag 1: wrong data generated bf_data_error, flag 3: wrong data generated from rp_data_error
def statistic_freq(flag):
  org_freq_dict = {}                                         # org freqence, like {org_name: 5}
  ticker_freq_dict = {}                                      # ticker frequence, like {tiker: 12}

  with open(wrong_by_map_file, "r", encoding="utf-8") as inf:
    for line in inf:
      # only statistic error, not miss & data source is bf or rp
      if len(line.split("|")) > 3 and line.split("|")[0].strip() == str(flag):            
        org_str = line.split("|")[3].strip()                 # comma as seperator
        ticker_str = line.split("|")[4].strip()
        org_list = org_str.split(",")
        ticker_list = ticker_str.split(",")
        for elem in org_list:
          if elem.strip() in org_freq_dict:  
            org_freq_dict[elem.strip()] += 1
          else:  
            org_freq_dict[elem.strip()] = 1
        for elem in ticker_list:
          if elem in ticker_freq_dict:
            ticker_freq_dict[elem.strip()] += 1
          else:
            ticker_freq_dict[elem.strip()] = 1
  return org_freq_dict,ticker_freq_dict

### statistic freqence of wrong data from bf_data_error
(bf_org_freq_dict,bf_ticker_freq_dict) = statistic_freq(1)
#descending sort by frequence
bf_org_freq_desc_dict = sorted(bf_org_freq_dict.items(),key = lambda o:o[1],reverse = True)
bf_ticker_freq_desc_dict = sorted(bf_ticker_freq_dict.items(),key = lambda o:o[1],reverse = True)
with open(bf_org_freq_file, "a", encoding="utf-8") as outf:
  for line in bf_org_freq_desc_dict:
    print(line,file=outf)
with open(bf_ticker_freq_file, "a", encoding="utf-8") as outf:
  for line in bf_ticker_freq_desc_dict:
    print(line,file=outf)

### statistic freqence of wrong data from rp_data_error
(rp_org_freq_dict,rp_ticker_freq_dict) = statistic_freq(3)
rp_org_freq_desc_dict = sorted(rp_org_freq_dict.items(),key = lambda o:o[1],reverse = True)
rp_ticker_freq_desc_dict = sorted(rp_ticker_freq_dict.items(),key = lambda o:o[1],reverse = True)
with open(rp_org_freq_file, "a", encoding="utf-8") as outf:
  for line in rp_org_freq_desc_dict:
    print(line,file=outf)
with open(rp_ticker_freq_file, "a", encoding="utf-8") as outf:
  for line in rp_ticker_freq_desc_dict:
    print(line,file=outf)
