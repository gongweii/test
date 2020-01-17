#!/user/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------
# File       : gen_ticker_auto_by_shape.py
# Author     : 
# Copyright  : Dynamic Technology Lab Pte Ltd
# Description: TODO
# Created    : 
# Revision   : none
#----------------------------------------------------------------------
import spacy
import pdb
import ticker_extract as te
import time
from collections import Counter

nlp = spacy.load("../../ner_model_version_1.0")
time0 = time.time()

country_list = list()
country_file = "country"
with open(country_file, "r", encoding="utf-8") as inf:
  for line in inf:
    country_list.append(line[:line.find("(")].lower().strip())

### find alone or continuous word which pos is PROPN
def find_continuous_token_pos(token_pos,pos_):
  temp = ""
  org_set = list()
  for i in range(len(token_pos)):
    if token_pos[i][1] == pos_:
      temp += " " + token_pos[i][0]
    else:
      # the first elem should be upper alpha
      if temp.strip() != "" and temp.strip()[0].isalpha() and temp.strip()[0] == temp.strip()[0].upper():
        org_set.append(temp.strip())
        temp = ""
  if temp.strip() != "" and temp.strip()[0].isalpha() and temp.strip()[0] == temp.strip()[0].upper():
    org_set.append(temp)
  return org_set

### Get shape of company name
def get_shape_of_org(org):
  # 1 Xxx
  # 2 XxXx
  # 3 XYZ
  # 4 Xx Xx
  # 0 other
  org = org.strip()
  if len(org) == 1 and org.isupper():
    no_of_shape = 1
  elif len(org.split(" ")) == 1 and org[0].isupper() and org[1:].islower():
    no_of_shape = 1
  elif len(org.split(" ")) == 1 and org[0].isupper() and (not org[1:].islower()) and (not org[1:].isupper()):
    no_of_shape = 2
  elif len(org.split(" ")) == 1 and len(org)>1 and org.isupper():
    no_of_shape = 3
  elif len(org.split(" ")) > 1 and sum([get_shape_of_org(ele) for ele in org.split(" ")]) == len(org.split(" ")):
    no_of_shape = 4
  else:
    no_of_shape = 0
  return no_of_shape

### shape is Xxx , no_of_shape is 1
def match_Xxx_shape_with_ticker(org,ticker):
  first_alpha = ticker[0]
  if org.find(first_alpha) != -1:
    pre_index = org.find(first_alpha) + 1
    ticker_index = [0]
    for c in ticker[1:].lower():
      ticker_index.append(org.lower().find(c,pre_index))
      pre_index = max(pre_index, org.lower().find(c,pre_index)) + 1
    if len([x for x in ticker_index if x != -1]) == len(ticker):
      return org.strip().lower()
  return None

### shape is XxXx ,no_of_shape is 2 
def match_XxXx_shape_with_ticker(org,ticker):
  res = None
  #compare only upper char
  upper = [c for c in org if c.isalpha() and c == c.upper()]
  ticker_index = []
  pre_index = 0
  for c in ticker:
    ticker_index.append(org.find(c,pre_index))
    pre_index = max(pre_index,org.find(c,pre_index))+1
  match_length = len([x for x in ticker_index if x != -1])
  if abs(len(ticker)-match_length) <= len(ticker)//2 and abs(len(upper)-match_length) <= len(ticker)//2 and \
    upper[:match_length] == ticker[:match_length]:
    res = org.strip().lower()
    return res
  #compare lower char also
  if res == None and org.find(ticker[0]) != -1 and \
    match_Xxx_shape_with_ticker(org[org.find(ticker[0]):],ticker) is not None:
    res = org.strip().lower()
    return res
  if res == None and org.find(ticker[0]) == -1 and \
    match_Xxx_shape_with_ticker(org[org.find(ticker[0]):],ticker) is not None and \
    len(ticker) == len(org[org.find(ticker[0]):]): 
    return org.strip().lower()
  return None

### shape is XYZ, no_of_shape is 3    
def match_XYZ_shape_with_ticker(org,ticker):
  if org == ticker:
    return org.strip().lower()
  else:
    return None

### shape is Xx Xx, no_of_shape is 4
def match_Xx_Xx_shape_with_ticker(org,ticker):
  res = None
  #compare only upper char
  upper = [c for c in org if c.isalpha() and c == c.upper()]
  ticker_index = []
  pre_index = 0
  for c in ticker:
    ticker_index.append(org.find(c,pre_index))
    pre_index = max(pre_index,org.find(c,pre_index))+1
  match_length = len([x for x in ticker_index if x != -1])
  if abs(len(ticker)-match_length) <= len(ticker)//2 and abs(len(upper)-match_length) <= len(ticker)//2 and \
    upper[:match_length] == ticker[:match_length]:
    res = org.strip().lower()
    return res
  #compare lower char also
  if res is None and org.find(ticker[0]) != -1 and \
    match_Xxx_shape_with_ticker(org[org.find(ticker[0]):],ticker) is not None:
    return org.strip().lower()
  return None

### shape is others, no_of_shape is 0
def match_other_shape_with_ticker(org,ticker):
  if len(org) <= 2*len(ticker) and len(ticker) > 2:
    return match_Xxx_shape_with_ticker(org,ticker)

### filter some org_name
def filter_org_name(org,headline):
  result = nlp(headline)
  for ent in result.ents:
    if ent.label_ in ('GPE','NORP'):
      country_list.append(str(ent).lower())
  # only a word belong to GPE(country,city,and so on),like "American" is country
  if org.lower() in country_list:
    return True
  return False

### find org_name corresponding ticker
def get_org_name_of_ticker(org_set,ticker,headline):
  #ticker's length equals 1, do not find org name
  if len(ticker) == 1:
    return None

  res = []
  for org in org_set:
    if filter_org_name(org,headline):
      break
    no_of_shape = get_shape_of_org(org)
    if no_of_shape == 1 and match_Xxx_shape_with_ticker(org,ticker) is not None:
      res.append(match_Xxx_shape_with_ticker(org,ticker))
    elif no_of_shape == 2 and match_XxXx_shape_with_ticker(org,ticker) is not None:
      res.append(match_XxXx_shape_with_ticker(org,ticker))
    elif no_of_shape == 3 and match_XYZ_shape_with_ticker(org,ticker) is not None:
      res.append(match_XYZ_shape_with_ticker(org,ticker))
    elif no_of_shape == 4 and match_Xx_Xx_shape_with_ticker(org,ticker) is not None:
      res.append(match_Xx_Xx_shape_with_ticker(org,ticker))
  res = [elem for elem in res if elem is not None]
  return list(set(res))

### part-of-speech tagging
def get_doc_pos(headline):
  token_pos = []
  result = nlp(headline)
  for token in result:
    token_pos.append([str(token).strip(),token.pos_])
  # the first token exclude The an a ,should be PROPN
  if token_pos[0][0].lower().strip() not in ('the','a','an'):
    token_pos[0][1] = 'PROPN'
  return token_pos

def get_org_set_by_pos(headline_org,ticker_core_org_set,ticker):
  if len(ticker) == 1:
    return []

  headline_list = headline_org[::2]
  exclude_org_list = headline_org[1::2]
  org_all_set = list()  
  org_set = list()
  tokens = list()
  for headline in headline_list:
    org_set = []
    token_pos = get_doc_pos(headline)
    org_set = find_continuous_token_pos(token_pos,'PROPN')
    org_set = get_org_name_of_ticker(org_set,ticker,headline)
    exclude_org = exclude_org_list[headline_list.index(headline)]

    org_set_clean = list()
    for org in org_set:
      org_set_clean.append(te.clean_company_name(org.strip()))
    org_all_set += org_set_clean
  return list(set(org_all_set))

### write ticker_by_shape map 
def write_ticker_shape_file(ticker,org_set,bbid,flag):
  for org in org_set:
    output_line = str(flag) + '|'+ org + '|' + ticker + '|'+ bbid
    with open(ticker_shape_file, 'a', encoding='utf-8') as outf:
      print(output_line,file = outf)

### read map
ticker_shape_file = "ticker_by_shape"
ticker_core_file = "../../us_clean_map/ticker_core_1.1"
bbid_map_file = "../../map/us_bbid_ticker_with_date_range"
three_party_file = "../../map/us_three_party"
core_set = {}
with open(ticker_core_file,'r',encoding='utf-8') as inf:
  for line in inf:
    if line.split('|')[2] not in core_set:
      core_set[line.split('|')[2]] = [line.split('|')[1]]
    else:
      core_set[line.split('|')[2]].append(line.split('|')[1])   
three_party_set = []
with open(three_party_file,'r',encoding='utf-8') as inf:
  for line in inf:
    three_party_set.append(line.split('|')[1].strip())
bbid_mapset = []
with open(bbid_map_file,'r',encoding='utf-8') as inf:
  for line in inf:
    bbid_mapset.append(line)

### start to generate ticker_by_shape
outputfile_error = "bf_train_data_result_all_error"
outputfile_error_dict = {}
exclude_org_dict = {}
with open(outputfile_error_file,'r',encoding='utf-8') as inf:
  for line in inf:    
    headline = line.split("|")[1].strip()
    ticker = line.split("|")[2].strip()
    exclude_org = line.split("|")[5].strip()
    if ticker not in outputfile_error_dict:
      outputfile_error_dict[ticker] = [headline]   
    else:
      outputfile_error_dict[ticker].append(headline)
    outputfile_error_dict[ticker].append(exclude_org)

i = 0
for ticker,headline_org in outputfile_error_dict.items():
  if i%100 == 0:
    print("the ticker ", i, " of ticker_by_shape done. take time",time.time()-time0)
  i += 1
  if te.is_valid_ticker(ticker):
    ticker_core_org_set = core_set.get(ticker,"")
    org_set = get_org_set_by_pos(headline_org,ticker_core_org_set,ticker)
    bbid = te.find_bbid_by_ticker_and_date(ticker)
    write_ticker_shape_file(ticker,org_set,bbid,3)


