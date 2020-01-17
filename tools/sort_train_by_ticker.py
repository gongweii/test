#!/usr/bin/env python                                                                                                                                                                                       
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------
# File       : sort_by_ticker.py
# Author     : 
# Copyright  : Dynamic Technology Lab Pte Ltd
# Description: sort headline by ticker
# Created    : Thur 26 Nov 2019 10:37:15 PM +08
# Revision   : none
#----------------------------------------------------------------------
import pdb

#train_file = "/home/wgong/tt/earlier_res/cn_result/missing_format"
#train_file = "/home/wgong/tt/result/jp/error_nq"
#train_file = "../result/eu/missing_ns_noformat"
#train_file = "/export/scratch/for_wgong/eu_data/ns_eu_till_2015"
train_file = "../result/eu/error_euis_all"
train_list = []
with open(train_file,"r",encoding="utf-8") as inf:
  for line in inf:
    train_list.append(line.strip())

train_list.sort(key = lambda x:x.split("|")[6].strip())
train_sort_file = "../result/eu/error_euis_all_sort"
with open(train_sort_file,"a",encoding="utf-8") as outf:
  for line in train_list:
    print(line.strip(),file=outf)

