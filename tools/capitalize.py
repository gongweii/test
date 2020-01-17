#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------
# File       : Capitilize.py
# Author     : 
# Copyright  : Dynamic Technology Lab Pte Ltd
# Description: regular map
# Created    : Thur 26 Nov 2019 10:37:15 PM +08
# Revision   : none
#----------------------------------------------------------------------

map_file = "../map/eu_core"
map_list = []
with open(map_file,"r",encoding="utf-8") as inf:
  for i,line in enumerate(inf):
    if len(line.split("|")) == 3:
      org_name = line.split("|")[1].strip().lower()
      flag = line.split("|")[0].strip()
      ticker = line.split("|")[2].strip().upper()
      output_line = flag + "|" + org_name + "|" + ticker
#      if output_line not in map_list:
      map_list.append(output_line.strip())
    else:
      print(i)
      print(line)

map_pro_file = "../map/eu_core1"
with open(map_pro_file,"a",encoding="utf-8") as outf:
  for line in map_list:
    print(line.strip(),file=outf)
