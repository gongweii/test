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

train_file = "../map/us_auto"
train_list = []
with open(train_file,"r",encoding="utf-8") as inf:
  for line in inf:
    train_list.append(line.strip())

train_list.sort(key = lambda x:x.split("|")[2].strip())
train_sort_file = "../map/us_auto_sort"
with open(train_sort_file,"a",encoding="utf-8") as outf:
  for line in train_list:
    print(line.strip(),file=outf)

