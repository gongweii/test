#!/usr/bin/env python
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------
# File       : ticker_extract.py
# Author     : htao
# Copyright  : Dynamic Technology Lab Pte Ltd
# Description: Only using core map
# Created    : Fri 23 Nov 2018 04:27:46 PM SGT
# Revision   : none
#----------------------------------------------------------------------
import pdb
import re
import spacy
nlp = spacy.load("../../ner_model_version_1.0")
def optimization_component(doc):
  # NER optimization
  new_ents = list(doc.ents)
  add_ent_set = ("apple",)
  for elem in add_ent_set:
    if doc.text.find(elem) != -1: 
      new_ents.append(spacy.tokens.span.Span(nlp.make_doc(elem),0,1))

  #part-of-sppech tagging and optimization
  token_pos = {}
  for token in doc:
    token_pos[token.text.strip()] = token.pos_
  if token_pos.get(list(token_pos.keys())[0]) != 'PROPN':
    if list(token_pos.keys())[0].lower().strip() not in ('a','an','the'):
      token_pos[list(token_pos.keys())[0]] = 'PROPN'
  return new_ents,token_pos

nlp.add_pipe(optimization_component,name="last_optimization_pipeline", after='ner') 

#### The module of match ticker with bbid by date ####
us_bbid_map_file = "../../map/us_bbid_ticker_with_date_range"
us_bbid_mapset = []
with open(us_bbid_map_file,'r') as inf:
  for line in inf:
    us_bbid_mapset.append(line)

eurp_bbid_map_file = "../../map/eurp_bbid_ticker_with_date_range"
eurp_bbid_mapset = []
with open(eurp_bbid_map_file,'r') as inf:
  for line in inf:
    eurp_bbid_mapset.append(line)

def find_bbid_by_ticker_and_date(ticker,date=20171231,source='rp'):
  bbid_max_start = 0
  bbid_mapset = us_bbid_mapset
  if source == "eurp":
    bbid_mapset = eurp_bbid_mapset
  # Search with the date limit
  for elem in bbid_mapset:
    elems = elem.split('|')
    if ticker == elems[1] and int(date) <= int(elems[3]) and int(date) >= int(elems[2]):
      if int(elems[2]) > bbid_max_start:
        bbid_max_start = int(elems[2])
        bbid = elems[0]
  # If use some outdate ticker, search without date limit and use the last start_date.
  if bbid_max_start == 0:
    for elem in bbid_mapset:
      elems = elem.split('|')
      if ticker == elems[1]:
        if int(elems[2]) > bbid_max_start:
          bbid_max_start = int(elems[2])
          bbid = elems[0]
  if bbid_max_start >0:
    return bbid
  else:
    return -1

#### Common function ####
def clean_ticker(ticker):
  ticker = re.sub("\.A$", "", ticker).rstrip()
  ticker = re.sub("\.B$", "", ticker).rstrip()

  return ticker

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

  result = re.sub(" b\/f$", "", result).rstrip()
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

def is_valid_us_ticker(ticker):
  if len(ticker) == 0 or len(ticker) >= 6:
    return False
  return True

def exclude_three_part(ticker_set,data_source='rp'):
  three_party_set = us_three_party_set
  if data_source in ('eurp','eusa'):
    three_party_set = eu_three_party_set
  normal_set = set()
  three_set = set()
  for elem in ticker_set:
    if elem in three_party_set:
      three_set.add(elem)
    else:
      normal_set.add(elem)
  return list(normal_set),list(three_set)

#### map ####
us_core_file = "../../map/us_core"
us_auto_file = "../../map/us_auto"
us_three_party_file = "../../map/us_three_party"
us_index_list_file = "../../map/us_index_list"

eu_core_file = "../../map/eu_core"
eurp_auto_file = "../../map/eurp_auto"
eusa_auto_file = "../../map/eusa_auto"
eu_three_party_file = "../../map/eurp_three_party"

us_core_dict = {}
with open(us_core_file, "r",encoding="utf-8") as inf:
  for line in inf:
    us_core_dict[line.split("|")[1]] = line.split("|")[2].rstrip("\n")
us_auto_dict = {}
with open(us_auto_file, "r",encoding="utf-8") as inf:
  for line in inf:
    us_auto_dict[line.split("|")[1]] = line.split("|")[2].rstrip("\n")
us_three_party_set = []
with open(us_three_party_file,"r",encoding="utf-8") as inf:
  for line in inf:
    us_three_party_set.append(line.split("|")[1].strip())
with open(us_index_list_file,"r",encoding="utf-8") as inf:
  for line in inf:
    us_three_party_set.append(line.split("|")[1].strip())
us_core_ticker_set = set()
for key,value in us_core_dict.items():
  us_core_ticker_set.add(value.strip())

eu_core_dict = {}
# need add ... ...
eurp_auto_dict = {}
with open(eurp_auto_file,"r",encoding="utf-8") as inf:
  for line in inf:
    eurp_auto_dict[line.split("|")[1]] = line.split("|")[2].rstrip("\n")
eusa_auto_dict = {}
with open(eusa_auto_file,"r",encoding="utf-8") as inf: 
  for line in inf:
    eusa_auto_dict[line.split("|")[1]] = line.split("|")[2].rstrip("\n")
eu_three_party_set = []
with open(eu_three_party_file,"r",encoding="utf-8") as inf:
  for line in inf:
    eu_three_party_set.append(line.split("|")[1].strip())


### Judge wether candidate's pos is PROPN or not
def is_PROPN(reg_key,token_pos):
  for token,pos in token_pos.items():
    if reg_key.find(token.lower()) != -1 and pos == "PROPN":
      return True
  return False

### Regular org name and headline
def regular_sentence(key,headline):
  equal_pair = {' & ':' and ', '-':' '}
  for k,v in equal_pair.items():
    reg_key = key.replace(k, v)
    reg_headline = headline.replace(k, v)
  return (reg_key,reg_headline)

#### long prefix matching
def longest_prefix_matching(org_set,key):
  for ele in org_set:
    if ele != key and ele.find(key) == 0 and not ele[ele.find(key)+len(key)].isalpha():
      return True
    if ele != key and ele.find(key) > 0 and not ele[ele.find(key)-1].isalpha():
      return True
  return False

#### NER module ####
def extract_ticker_ner(headline,source = 'rp',is_missing=False):
  ticker_set = set()
  org_set = set()
  org2ticker_dict = us_core_dict
  if source == "eurp":
    org2ticker_dict = eurp_auto_dict
  if is_missing:
    org2ticker_dict = us_auto_dict
  ents = nlp(headline.lower())[0]
  for ent in ents:
    if(ent.label_ in ('ORG','')):
      target = ent.text
      target = clean_company_name(target)
      org_set.add(target.strip())
      ticker = org2ticker_dict.get(target.strip(),"")   
      if ticker != "":
        ticker_set.add(ticker)
  return list(org_set),exclude_three_part(ticker_set,data_source=source)[0],exclude_three_part(ticker_set,data_source=source)[1]

#### Match by Format ####
def extract_ticker_format(headline):
  ticker_set = set()
  tickers = re.findall('>(\w+)$', headline.strip())
  for ticker in tickers:
    if is_valid_us_ticker(ticker):
      ticker_set.add(clean_ticker(ticker))
  ticker_set_clear = ticker_set
  if len(ticker_set_clear) != 0:
    return list(ticker_set_clear),list(ticker_set_clear),[]
  else:
    ticker = re.search('\((\w+)\)', headline.strip())
    if ticker is not None:
      if ticker.start() > 3 and ticker not in ("R", "C"):
        ticker_str = ticker.group(1)
        if is_valid_us_ticker(ticker_str):
          ticker_set.add(clean_ticker(ticker_str))
  #### make sure the ticker is in our ticker list(which means can find bbid at last)
    ticker_set_clear = set()
    for elem in ticker_set:
      if elem in us_core_ticker_set:
        ticker_set_clear.add(elem)
  return list(ticker_set_clear),exclude_three_part(ticker_set_clear)[0],exclude_three_part(ticker_set_clear)[1]

#### Directly mapping ####
def extract_ticker_directly(headline,source="rp",is_missing=False):
  ticker_list = list()
  org_list = list()
  org2ticker_dict = us_core_dict
  if is_missing == True:
    org2ticker_dict = us_auto_dict
  if source == "eurp":
    org2ticker_dict = eurp_auto_dict

  token_pos = nlp(headline.lower())[1]
  for key,value in org2ticker_dict.items():
    (reg_key,reg_headline) = regular_sentence(key,headline)
    location = reg_headline.lower().find(reg_key.lower())
    if(location!=-1 and (location == 0 or not reg_headline[location-1].isalpha()) and (location+len(reg_key) == len(reg_headline) or not reg_headline[location+len(reg_key)].isalpha())):
      if source == "rp" and (not reg_headline[location:location+len(reg_key)].islower() or not is_missing) and \
        (value.lower().strip() != key.lower().strip() or (reg_headline[location:location+len(reg_key)] in [k.upper() for k in token_pos.keys()] and len(reg_key) > 2)):
        if len(org_list) == 0:
          ticker_list.append(value)
          org_list.append(key)
        if len(org_list) > 0 and key not in org_list and not longest_prefix_matching(org_list,key):  # Only match the org_name with the longest prefix
          ticker_list.append(value)
          org_list.append(key)

      if source == "eurp":
        if len(org_list) == 0:
          ticker_list.append(value)
          org_list.append(key)
        if len(org_list) > 0 and key not in org_list and not longest_prefix_matching(org_list,key):  # Only match the org_name with the longest prefix
          ticker_list.append(value)
          org_list.append(key)      

      if source == "bf" and is_PROPN(reg_key,token_pos) and value.lower().strip() != key.lower().strip() and (not reg_headline[location:location+len(reg_key)].islower() or not is_missing):
        if len(org_list) == 0:
          ticker_list.append(value)
          org_list.append(key)
        if len(org_list) > 0 and key not in org_list and not longest_prefix_matching(org_list,key): 
          ticker_list.append(value)
          org_list.append(key)
  
  if len(org_list) > 1 and longest_prefix_matching(org_list[1:],org_list[0]):                       
    org_list.pop(0)
    ticker_list.pop(0)
  
  return org_list,exclude_three_part(set(ticker_list),data_source=source)[0],exclude_three_part(set(ticker_list),data_source=source)[1]

### extract ticker by abbreviation
def extract_ticker_abbreviation(headline,is_missing=False):
  org_set = set()
  ticker_set = set()
  org2ticker_set = us_core_dict
  if is_missing:
    org2ticker_dict = us_auto_dict

  for key,value in org2ticker_dict.items():
    if key.lower().strip() == value.lower().strip():
      (reg_key,reg_headline) = regular_sentence(key,headline)
      location = reg_headline.lower().find(reg_key.lower().strip())
      if location != -1: 
        key_of_headline = reg_headline[location:location+len(reg_key)]
      if location == 0 and not key_of_headline.islower() and\
        ((location+len(reg_key) < len(reg_headline) and (reg_headline[location+len(reg_key)] == " " or reg_headline[location+len(reg_key)] == ":")) or location+len(reg_key) == len(reg_headline)):
        ticker_set.add(value)
        org_set.add(key)
      if location > 0 and reg_headline[location-1] == " " and not key_of_headline.islower() and\
        ((location+len(reg_key) < len(reg_headline) and (reg_headline[location+len(reg_key)] == " " or reg_headline[location+len(reg_key)] == ":")) or location+len(reg_key) == len(reg_headline)):
        ticker_set.add(value)
        org_set.add(key)
  return list(org_set),exclude_three_part(ticker_set,data_source=source)[0],exclude_three_part(ticker_set,data_source=source)[1]
