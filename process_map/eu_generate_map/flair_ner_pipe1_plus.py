#!/user/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------
# File       : flair_ner_pipe1_plus.py
# Author     : 
# Copyright  : Dynamic Technology Lab Pte Ltd
# Description: TODO
# Created    : 
# Revision   : none
#----------------------------------------------------------------------

import ticker_extract as te

#### sort ticker_one_NEREntity and clean company name
### clean company name
ticker_one_NEREntity_temp_file = "res/pipe1/eusa_one_NEREntity_temp"
ticker_one_NEREntity = list()
with open(ticker_one_NEREntity_temp_file,'r',encoding="utf-8") as inf:
  for line in inf:
    org = line.split("|")[1].strip()
    org = te.clean_company_name(org)
    clean_line = line.split("|")[0].strip() + "|" + org.strip() + "|" + line.split("|")[2].strip()
    ticker_one_NEREntity.append(clean_line.strip("\n"))

### sort by ticker
ticker_one_NEREntity = sorted(ticker_one_NEREntity,key = lambda line:line.split("|")[2].strip(),reverse=False)

### write file
ticker_one_NEREntity_file = "res/pipe1/eusa_one_NEREntity"
with open(ticker_one_NEREntity_file,"a",encoding="utf-8") as outf:
  for line in ticker_one_NEREntity:
    print(line.strip("\n"),file=outf)
