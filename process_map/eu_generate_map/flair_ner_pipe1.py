#!/user/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------
# File       : flair_ner_pipe1.py
# Author     : 
# Copyright  : Dynamic Technology Lab Pte Ltd
# Description: TODO
# Created    : 
# Revision   : none
#----------------------------------------------------------------------

import re
import flair
from flair.data import Sentence
from flair.models import SequenceTagger
tagger = SequenceTagger.load("ner")

def clean_company_name(raw_name):
  result = raw_name.lower()

  result = re.sub("'$", "", result).rstrip()
  result = re.sub(",$", "", result).rstrip()
  result = re.sub("\?$", "", result).rstrip()
  result = re.sub(";$", "", result).rstrip()
  result = re.sub("\.$", "", result).rstrip()
  result = re.sub("\&$", "", result).rstrip()
  result = re.sub("\:$", "", result).rstrip()
  
  result = re.sub("^chart(\:|\-|\s)", "", result).strip()
  result = re.sub("^update(\:|\-|\s)", "", result).strip()
  result = re.sub("^brief(\:|\-|\s)", "", result).strip()
  result = re.sub("^\*", "", result).strip()

  result = re.sub(" reports$", "", result).rstrip() 
  result = re.sub(" raises$", "", result).rstrip()
  result = re.sub(" update$ ", "", result).rstrip()
  result = re.sub(" declares$ ", "", result).rstrip()
  result = re.sub(" confirms$ ", "", result).rstrip()
  result = re.sub(" plans$ ", "", result).rstrip()
  result = re.sub(" buys$ ", "", result).rstrip()

  reult = re.sub(" b\/f$", "", result).rstrip()
  result = re.sub(" p\/f$", "", result).rstrip()
  result = re.sub(" plc$", "", result).rstrip()
  result = re.sub(" st$", "", result).rstrip()
  result = re.sub(" kgaa$", "", result).rstrip()
  result = re.sub(" a\/s$", "", result).rstrip()  
  result = re.sub(" as$", "", result).rstrip()
  result = re.sub(" asa$", "", result).rstrip()
  result = re.sub(" a\.s$", "", result).rstrip()  
  result = re.sub(" inc$", "", result).rstrip()
  result = re.sub(" inc\.$", "", result).rstrip()
  result = re.sub(" corporation$", "", result).rstrip()
  result = re.sub(" company$", "", result).rstrip()
  result = re.sub(" corp$", "", result).rstrip()
  result = re.sub(" corp\.$", "", result).rstrip()
  result = re.sub(" ltd$", "", result).rstrip()
  result = re.sub(" ltd\.$", "", result).rstrip()
  result = re.sub(" co\.$", "", result).rstrip()
  result = re.sub(" co$", "", result).rstrip()  
  result = re.sub(" n\.v$", "", result).rstrip()  
  result = re.sub(" nv$", "", result).rstrip()
  result = re.sub(" sa$", "", result).rstrip()
  result = re.sub(" s\.a$", "", result).rstrip()  
  result = re.sub(" se$", "", result).rstrip()
  result = re.sub(" ab$", "", result).rstrip()  
  result = re.sub(" spa$", "", result).rstrip()
  result = re.sub(" s\.p\.a$", "", result).rstrip() 
  result = re.sub(" ag$", "", result).rstrip()
  result = re.sub(" ag\-pfd$", "", result).rstrip()
  result = re.sub(" group$", "", result).rstrip()  

  result = re.sub("'s$", "", result).rstrip()
  result = re.sub("'$", "", result).rstrip()
  result = re.sub(",$", "", result).rstrip()
  result = re.sub("\?$", "", result).rstrip()
  result = re.sub(";$", "", result).rstrip()
  result = re.sub("\.$", "", result).rstrip()
  result = re.sub("\&$", "", result).rstrip()
  result = re.sub("\:$", "", result).rstrip()
  result = re.sub(" b\/f$", "", result).rstrip()
  result = re.sub(" p\/f$", "", result).rstrip()
  result = re.sub(" plc$", "", result).rstrip()
  result = re.sub(" a\/s$", "", result).rstrip()  
  result = re.sub(" as$", "", result).rstrip()
  result = re.sub(" a\.s$", "", result).rstrip()  
  result = re.sub(" inc$", "", result).rstrip()
  result = re.sub(" corporation$", "", result).rstrip()
  result = re.sub(" corp$", "", result).rstrip()
  result = re.sub(" ltd$", "", result).rstrip()
  result = re.sub(" co$", "", result).rstrip()
  result = re.sub(" n\.v$", "", result).rstrip()  
  result = re.sub(" nv$", "", result).rstrip()
  result = re.sub(" sa$", "", result).rstrip()
  result = re.sub(" s\.a$", "", result).rstrip() 
  result = re.sub(" se$", "", result).rstrip()
  result = re.sub(" ab$", "", result).rstrip()
  result = re.sub(" spa$", "", result).rstrip()
  result = re.sub(" s\.p\.a$", "", result).rstrip()
  result = re.sub(" ag$", "", result).rstrip()

  result = re.sub("'s$", "", result).rstrip()
  result = re.sub("'$", "", result).rstrip()
  result = re.sub(",$", "", result).rstrip()
  result = re.sub("\?$", "", result).rstrip()
  result = re.sub(";$", "", result).rstrip()
  result = re.sub("\.$", "", result).rstrip()
  result = re.sub("\&$", "", result).rstrip()
  result = re.sub("\:$", "", result).rstrip()

  return result

eusa_one_NEREntity_file = "res/pipe1/eusa_one_NEREntity_temp"
eusa_plus_NEREntity_file = "res/pipe1/eusa_plus_NEREntity"
eusa_zero_NEREntity_file = "res/pipe1/eusa_zero_NEREntity"

def write_one_NEREntity(flag,org_name,ticker):
  with open(eusa_one_NEREntity_file,'a',encoding="utf-8") as outf:
    output_line = str(flag) + "|" + org_name.strip() + "|" + ticker.strip()
    print(output_line,file=outf)
def write_plus_NEREntity(flag,org_set,ticker):
  with open(eusa_plus_NEREntity_file,'a',encoding='utf-8') as outf:
    output_line = str(flag) + "|" + ','.join(org_set) + "|" + ticker.strip()
    print(output_line,file=outf)
def write_zero_NEREntity(flag,headline,ticker):
  with open(eusa_zero_NEREntity_file,'a',encoding='utf-8') as outf:
    output_line = str(flag) + "|" + headline.strip() + "|" + ticker.strip()
    print(output_line,file=outf)

### Search org|ticker by ner, return org_set
def recognize_entity(headline):
  org_set = set()
  sentence = Sentence(headline)
  tagger.predict(sentence)
  for ent in sentence.get_spans('ner'):
    if ent.tag == 'ORG':
      target = ent.text
      target = clean_company_name(target)
      org_set.add(target.strip())
  return org_set

### Traverse dataset to generate org|ticker map
train_data_file = "../../eu_data/train_data_sa_eu_till_2015"
more_than_one_num = 0
zero_org_num = 0
norm_org_num = 0
i = 0
with open(train_data_file,"r",encoding="utf-8") as inf:
  for i,line in enumerate(inf):
    if i % 1000 == 0:
      print("Done: ",i)
    
    headline = line.split("|")[1].strip()
    ticker = line.split("|")[2].strip()
    org_set = recognize_entity(headline)
    ## If flair recognize one entity,records that
    if len(org_set) == 1:
      write_one_NEREntity(1,''.join(org_set),ticker)
      norm_org_num += 1
      if norm_org_num%100 == 0:
        print("org_set's length == 1: ",norm_org_num)
    ## If flair recognize more than one entity,records that
    if len(org_set) > 1:
      write_plus_NEREntity(1,org_set,ticker)
      more_than_one_num += 1
      if more_than_one_num%100 == 0:
        print("org_set's length  > 1: ",more_than_one_num)
    ## If flair can't recognize any entity, also records that 
    if len(org_set) == 0:
      write_zero_NEREntity(1,headline,ticker)
      zero_org_num += 1
      if zero_org_num%100 == 0:
        print("org_set's lenght == 0: ",zero_org_num)


