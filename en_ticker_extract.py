#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------
# File       : en_ticker_extract.py
# Author     : htao
# Copyright  : Dynamic Technology Lab Pte Ltd
# Description: English Language
# Created    : Fri 23 Nov 2018 04:27:46 PM SGT
# Revision   : none
#----------------------------------------------------------------------
import re
import pdb
import spacy
nlp = spacy.load("ner_model_version_1.0")

#### ner model's optimizer ####
def optimization_component(doc):
  # Named Entity Recognition
  new_ents = list(doc.ents)
  add_ent_set = ("apple",)
  for elem in add_ent_set:
    if doc.text.find(elem) != -1: 
      new_ents.append(spacy.tokens.span.Span(nlp.make_doc(elem),0,1))

  # part-of-sppech tagging
  token_pos = {}
  for token in doc:
    token_pos[token.text.strip()] = token.pos_
  if token_pos.get(list(token_pos.keys())[0]) != 'PROPN':
    if list(token_pos.keys())[0].lower().strip() not in ('a','an','the'):
      token_pos[list(token_pos.keys())[0]] = 'PROPN'
  return new_ents,token_pos

nlp.add_pipe(optimization_component,name="last_optimization_pipeline", after='ner') 

#### The module of match ticker with bbid by date ####
us_bbid_map_file = "map/us_bbid_ticker_with_date_range"
us_bbid_mapset = []
with open(us_bbid_map_file,'r') as inf:
  for line in inf:
    us_bbid_mapset.append(line)

eu_bbid_map_file = "map/eu_bbid_ticker_with_date_range"
eu_bbid_mapset = []
with open(eu_bbid_map_file,'r') as inf:
  for line in inf:
    eu_bbid_mapset.append(line)

def find_bbid_by_ticker_and_date(ticker,region,date=20171231):
  bbid_max_start = 0
  bbid_mapset = us_bbid_mapset
  if region == "us":
    bbid_mapset = us_bbid_mapset
  if region == "eu":
    bbid_mapset = eu_bbid_mapset

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

### find European company's bbid ###
def find_bbid_by_ticker_with_exchange(ticker,region="eu",date=201771231):
  bbid = find_bbid_by_ticker_and_date(ticker,region,date)
  if bbid == -1:
    ticker_noexchg = ticker[:ticker.find('.')]
    bbid = find_bbid_by_ticker_and_date(ticker_noexchg.upper(),region,date)
    if bbid == -1 and len(ticker) > 2 and ticker[-3:] == '.DE':
      ticker_node = re.sub("G\.DE|Gn\.DE|Gnq\.DE|G_p\.DE$","",ticker)
      bbid = find_bbid_by_ticker_and_date(ticker_node.upper(),region,date)
      if bbid == -1:
        ticker_noudl = re.sub("_","",ticker)
        bbid = find_bbid_by_ticker_and_date(ticker_noudl.upper(),region,date)
        if bbid == -1:
          ticker_noudl_noaz = re.sub("[a-z_]","",ticker)
          bbid = find_bbid_by_ticker_and_date(ticker_noudl_noaz.upper(),region,date)
          if bbid == -1 and len(ticker_noudl_noaz) > 2 and ticker_noudl_noaz[-3:] == '.DE':
            ticker_node = re.sub("G\.DE$","",ticker)
            bbid = find_bbid_by_ticker_and_date(ticker_node.upper(),region,date)
            if bbid == -1:
              ticker_noudlpre = ticker_noudl[:ticker_noudl.find('.')]
              bbid = find_bbid_by_ticker_and_date(ticker_noudlpre.upper(),region,date)
              if bbid == -1:
                ticker_noudl_noazpre = ticker_noudl_noaz[:ticker_noudl_noaz.find('.')]
                bbid = find_bbid_by_ticker_and_date(ticker_noudl_noazpre.upper(),region,date)
  return bbid

### Common function ####
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

def is_valid_ticker(ticker):
  if len(ticker) == 0 or len(ticker) >= 15:
    return False
  return True

def exclude_three_part(ticker_set,region="us"):
  if region == "us":
    three_party_set = us_three_party_set
  if region == "eu":
    three_party_set = eu_three_party_set

  normal_set = set()
  three_set = set()
  for elem in ticker_set:
    if elem in three_party_set:
      three_set.add(elem)
    else:
      normal_set.add(elem)
  return list(normal_set),list(three_set)

#### extract more important companies ####
def soft_exclude_three_part(org_set, headline):
  headline = headline.lower()
  exclude_set = (' at ',)
  primary_org_set = list()

  if len(org_set) == 0 or len(org_set) == 1:
    return org_set

  for org in org_set:
    for elem in exclude_set:
      if headline.find(elem) != -1 and headline.find(org.lower()) <= headline.find(elem):
        primary_org_set.append(org)
        break

  if len(primary_org_set) == 0:
    return org_set
  return primary_org_set

#### map ####
us_core_file = "map/us_core"
us_auto_file = "map/us_auto"
us_prod_file = "map/us_prod"
us_three_party_file = "map/us_three_party"
us_index_list_file = "map/us_index_list"

eu_core_file = "map/eu_core"
eu_prod_file = "map/eu_prod"
eu_three_party_file = "map/eu_three_party"
equal_pair_file = "map/eu_equal_pair"

## US region
us_core_dict = {}
with open(us_core_file, "r", encoding="utf-8") as inf:
  for line in inf:
    us_core_dict[line.split("|")[1]] = line.split("|")[2].rstrip("\n")
us_auto_dict = {}
with open(us_auto_file, "r", encoding="utf-8") as inf:
  for line in inf:
    us_auto_dict[line.split("|")[1]] = line.split("|")[2].rstrip("\n")
us_prod_dict = {}
with open(us_prod_file,"r",encoding="utf-8") as inf:
  for line in inf:
    us_prod_dict[line.split("|")[1]] = line.split("|")[2].rstrip("\n")
us_three_party_set = []
with open(us_three_party_file,"r", encoding="utf-8") as inf:
  for line in inf:
    us_three_party_set.append(line.split("|")[1].strip())
with open(us_index_list_file,"r", encoding="utf-8") as inf:
  for line in inf:
    us_three_party_set.append(line.split("|")[1].strip())
us_core_ticker_set = set()
for key,value in us_core_dict.items():
  us_core_ticker_set.add(value.strip())

## EU region
eu_core_dict = {}
with open(eu_core_file,"r",encoding="utf-8") as inf:
  for line in inf:
    eu_core_dict[line.split("|")[1]] = line.split("|")[2].rstrip("\n")
eu_prod_dict = {}
with open(eu_prod_file,"r",encoding="utf-8") as inf:
  for line in inf:
    eu_prod_dict[line.split("|")[1]] = line.split("|")[2].rstrip("\n")
eu_three_party_set = []
with open(eu_three_party_file,"r",encoding="utf-8") as inf:
  for line in inf:
    eu_three_party_set.append(line.split("|")[1].strip())
equal_pair = {}
with open(equal_pair_file,"r",encoding="utf-8") as inf:
  for line in inf:
    equal_pair[line.split("|")[0].rstrip("\n")] = line.split("|")[1].rstrip("\n")

#### Regular org name or headline ####
def regular_sentence(key,region="us"):
  ## treat similiar words as equivalent,such as '&' and 'and'
  if region == "eu":
    reg_key = ' '.join(key.split())
    for k,v in equal_pair.items():
      reg_key = ' ' + ' '.join(reg_key.split()) + ' '
      reg_key = reg_key.replace(k, v)
  else:
    us_equal_pair = {' & ':' and ', '-':' '}
    reg_key = ' '.join(key.split())
    for k,v in us_equal_pair.items():
      reg_key = reg_key.replace(k, v)
  reg_key = ' '.join(reg_key.split())
  return reg_key

#### Judge wether candidate's pos is PROPN or not ####
def is_PROPN(key,token_pos,is_missing):
  for token,pos in token_pos.items():
    if not is_missing and key.find(token.lower()) != -1 and pos in ("PROPN",):
      return True
    if is_missing and key.find(token.lower()) != -1 and pos in ("PROPN","NOUN"):
      return True
  return False

#### long prefix matching ####
def longest_prefix_matching(org_set,key):
  # Make sure that some company called xxx XYZ is more likely picked than which called xxx
  for elem in org_set:
    if elem != key and elem.find(key) == 0 and not elem[elem.find(key)+len(key)].isalpha():
      return True
    if elem != key and elem.find(key) > 0 and not elem[elem.find(key)-1].isalpha():
      return True
  return False

#### NER module ####
def extract_ticker_ner(headline,region,is_missing=False):
  ticker_set = set()
  org_set = set()
  if region == "us" and is_missing == False:
    org2ticker_dict = us_core_dict
  if region == "us" and is_missing == True:
    org2ticker_dict = us_auto_dict
  if region == "eu":
    org2ticker_dict = eu_core_dict
  if region == "us":
    ents = nlp(headline.lower())[0]
  else:
    ents = nlp(headline)[0]

  for ent in ents:
    if(ent.label_ in ('ORG','')):
      target = ent.text
      org_set.add(target.strip())
  # extract primary company
  org_set = soft_exclude_three_part(org_set,headline)
  org_set = set([clean_company_name(org) for org in org_set])
  ticker_set = [org2ticker_dict.get(org.strip(),"") for org in org_set]
  ticker_set = set([ticker for ticker in ticker_set if ticker != ""])

  return list(org_set),exclude_three_part(ticker_set,region)[0],exclude_three_part(ticker_set,region)[1]

#### Match by Format ####
def extract_ticker_format(headline,region='eu'):
  ticker_set = set()
  if region == "eu":
    tickers = re.findall('\<([0-9a-zA-Z_]*[^>]*\.[A-Z]{1,3})\>',headline.strip())
    for ticker in tickers:
      if is_valid_ticker(ticker):
        ticker_set.add(clean_ticker(ticker))
    return list(ticker_set),exclude_three_part(ticker_set)[0],exclude_three_part(ticker_set)[1]
  ### region is 'us'
  else:
    tickers = re.findall('>(\w+)$', headline.strip())
    for ticker in tickers:
      if is_valid_ticker(ticker):
        ticker_set.add(clean_ticker(ticker))
    ticker_set_clear = ticker_set
    if len(ticker_set_clear) != 0:
      return list(ticker_set_clear),list(ticker_set_clear),[]
    else:
      ticker = re.search('\((\w+)\)', headline.strip())
      if ticker is not None:
        if ticker.start() > 3 and ticker not in ("R", "C"):
          ticker_str = ticker.group(1)
          if is_valid_ticker(ticker_str):
            ticker_set.add(clean_ticker(ticker_str))
      ## make sure the ticker is in our ticker list(which means can find bbid at last)
      ticker_set_clear = set()
      for elem in ticker_set:
        if elem in us_core_ticker_set:
          ticker_set_clear.add(elem)
    return list(ticker_set_clear),exclude_three_part(ticker_set_clear)[0],exclude_three_part(ticker_set_clear)[1]

#### Directly mapping ####
def extract_ticker_directly(headline,region,source="rp",is_missing=False):
  ticker_list_temp = list()
  org_list_temp = list()
  if region == "us" and is_missing == False:
    org2ticker_dict = us_core_dict
  if region == "us" and is_missing == True:
    org2ticker_dict = us_auto_dict
  if region == "eu":
    org2ticker_dict = eu_core_dict

  token_pos = nlp(headline.lower())[1]
  reg_headline = regular_sentence(headline,region)
  for key,value in org2ticker_dict.items():
    location = reg_headline.lower().find(key.lower())
    if(location!=-1 and (location == 0 or not reg_headline[location-1].isalpha()) and (location+len(key) == len(reg_headline) or not reg_headline[location+len(key)].isalpha())):
      ## The processing of unknown source dataset called us is the same with usrp
      if region == "us" and source == "rp" and (not reg_headline[location:location+len(key)].islower() or not is_missing) and \
        (value.lower().strip() != key.lower().strip() or (reg_headline[location:location+len(key)] in [k.upper() for k in token_pos.keys()] and len(key) > 2)):
        if len(org_list_temp) == 0:
          ticker_list_temp.append(value)
          org_list_temp.append(key)
        # Only match the org_name with the longest prefix
        if len(org_list_temp) > 0 and key not in org_list_temp and not longest_prefix_matching(org_list_temp,key):
          ticker_list_temp.append(value)
          org_list_temp.append(key)
      ## Search with the part-of-speech tagging and capitalization  limit       
      if region == "us" and source == "bf" and is_PROPN(key,token_pos,is_missing) and value.lower().strip() != key.lower().strip() and \
         (not reg_headline[location:location+len(key)].islower() or not is_missing):
        if len(org_list_temp) == 0:
          ticker_list_temp.append(value)
          org_list_temp.append(key)
        if len(org_list_temp) > 0 and key not in org_list_temp and not longest_prefix_matching(org_list_temp,key): 
          ticker_list_temp.append(value)
          org_list_temp.append(key)
      
      ## These EU region's datasets are processed in the same way
      if region == "eu":
        if key[0].isdigit() and location > 0 and reg_headline[location-1].isdigit():
          continue
        if key[-1].isdigit() and location+len(key) < len(reg_headline) and reg_headline[location+len(key)].isdigit():
          continue
        if len(org_list_temp) == 0:
          ticker_list_temp.append(value)
          org_list_temp.append(key)
        if len(org_list_temp) > 0 and key not in org_list_temp and not longest_prefix_matching(org_list_temp,key):
          ticker_list_temp.append(value)
          org_list_temp.append(key)
  
  if len(org_list_temp) > 1 and longest_prefix_matching(org_list_temp[1:],org_list_temp[0]):                       
    org_list_temp.pop(0)
    ticker_list_temp.pop(0)

  # extract primary company
  org_list = soft_exclude_three_part(org_list_temp,reg_headline)
  retain_index = [org_list_temp.index(ele) for ele in org_list]
  ticker_list = [ticker_list_temp[i] for i in retain_index]

  return org_list,exclude_three_part(set(ticker_list),region)[0],exclude_three_part(set(ticker_list),region)[1]

#### extract ticker by abbreviation  ####
# Extract ticker which same with company name except capitalization
def extract_ticker_abbreviation(headline,is_missing=False):
  org_set = set()
  ticker_set = set()
  org2ticker_dict = us_core_dict
  if is_missing:
    org2ticker_dict = us_auto_dict
  reg_headline = regular_sentence(headline)
  for key,value in org2ticker_dict.items():
    if key.lower().strip() == value.lower().strip():
      location = reg_headline.lower().find(key.lower().strip())
      if location != -1: 
        key_of_headline = reg_headline[location:location+len(key)]
      if location == 0 and not key_of_headline.islower() and\
        ((location+len(key) < len(reg_headline) and (reg_headline[location+len(key)] == " " or reg_headline[location+len(key)] == ":")) or location+len(key) == len(reg_headline)):
        ticker_set.add(value)
        org_set.add(key)
      if location > 0 and reg_headline[location-1] == " " and not key_of_headline.islower() and\
        ((location+len(key) < len(reg_headline) and (reg_headline[location+len(key)] == " " or reg_headline[location+len(key)] == ":")) or location+len(key) == len(reg_headline)):
        ticker_set.add(value)
        org_set.add(key)
  return list(org_set),exclude_three_part(ticker_set)[0],exclude_three_part(ticker_set)[1]

#### extract ticker by similarity ####
def extract_ticker_similarity(headline,region,is_missing=False):
  if region == "us":
    org2ticker_dict = us_core_dict
  if region == "eu":
    org2ticker_dict = eu_core_dict
  org_set = set()
  ticker_set = set()
  reg_headline = regular_sentence(headline.lower(),region) 
  for key,value in org2ticker_dict.items():
    if key.upper().strip() != value.strip():
      key_list = key.split()
      headline_list = reg_headline.split()
      ## Use sliding window to match
      for i in range(len(headline_list)-len(key_list)+1):
        org_name_list = headline_list[i:i+len(key_list)]
        if org_name_list[0][0] != key_list[0][0]:
          continue 
        ## eliminate the effects of singular and plural
        org_name_list = [org.rstrip('s').strip() if len(org.strip()) >= 5 else org.strip() for org in org_name_list]
        key_list = [org.rstrip('s').strip() if len(org.strip()) >= 5 else org.strip() for org in key_list]
        if ' '.join(org_name_list) == ' '.join(key_list):
          ticker_set.add(value)
          org_set.add(key)
          break
  return list(org_set),exclude_three_part(ticker_set)[0],exclude_three_part(ticker_set)[1]

#### extract ticker by productions ####
## only run this module when use_prob is True
def extract_ticker_prod(headline,region):
  ticker_list_temp = list()
  org_list_temp = list()
  if region == "us":
    org2ticker_dict = us_prod_dict
  if region == "eu":
    org2ticker_dict = eu_prod_dict
  reg_headline = regular_sentence(headline,region)
  ## this module is similiar with directly module
  for key,value in org2ticker_dict.items():
    location = reg_headline.lower().find(key.lower())
    if(location!=-1 and (location == 0 or not reg_headline[location-1].isalpha()) and (location+len(key) == len(reg_headline) or not reg_headline[location+len(key)].isalpha())):
      if len(org_list_temp) == 0:
        ticker_list_temp.append(value)
        org_list_temp.append(key)
      if len(org_list_temp) > 0 and key not in org_list_temp and not longest_prefix_matching(org_list_temp,key):
        ticker_list_temp.append(value)
        org_list_temp.append(key)
  if len(org_list_temp) > 1 and longest_prefix_matching(org_list_temp[1:],org_list_temp[0]):
    org_list_temp.pop(0)
    ticker_list_temp.pop(0)
  org_list = soft_exclude_three_part(org_list_temp,reg_headline)
  retain_index = [org_list_temp.index(ele) for ele in org_list]
  ticker_list = [ticker_list_temp[i] for i in retain_index]

  return org_list,exclude_three_part(set(ticker_list),region)[0],exclude_three_part(set(ticker_list),region)[1]

