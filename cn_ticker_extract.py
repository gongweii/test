#!/usr/bin/env python                                                                                                                                            
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------
# File       : cn_ticker_extract.py
# Author     : 
# Copyright  : Dynamic Technology Lab Pte Ltd
# Description: Chinese Language
# Created    : Tues 30 Jul 2019 09:00:00 AM SGT
# Revision   : none
#----------------------------------------------------------------------

import re
from pyhanlp import *

# ner based on HMM
segment_hmm = HanLP.newSegment().enableOrganizationRecognize(True)
# ner based on CRF
segment_crf = HanLP.newSegment('crf').enableOrganizationRecognize(True)
# ner based on Perceptron
segment_perceptron = HanLP.newSegment('perceptron').enableOrganizationRecognize(True)

#### Add user-defined dictionary ####
CustomDictionary = JClass("com.hankcs.hanlp.dictionary.CustomDictionary")
cn_core_file = "map/cn_core"

with open(cn_core_file, "r", encoding="utf-8") as inf:
  for line in inf:
    CustomDictionary.add(line.split("|")[1].strip(),"ntc 1000")

#### Read map ####
cn_core_dict = {}
with open(cn_core_file, "r", encoding="utf-8") as inf:
  for line in inf:
    cn_core_dict[line.split("|")[1].strip()] = line.split("|")[2].rstrip("\n")

cn_auto_dict = {}
cn_auto_file = "map/cn_auto"
with open(cn_auto_file, "r", encoding="utf-8") as inf:
  for line in inf:
    cn_auto_dict[line.split("|")[1].strip()] = line.split("|")[2].rstrip("\n")

cn_exclude_words_set = set()
cn_exclude_words_file = "map/cn_exclude_words"
with open(cn_exclude_words_file, "r", encoding="utf-8") as inf:
  for elem in inf:
    cn_exclude_words_set.add(elem.rstrip("\n"))

#### transform SBC to DBC case ####
def SBC_to_DBC(ustring):
  rstring = ""
  for uchar in ustring:
    inside_code=ord(uchar)
    if inside_code == 12288:
      inside_code = 32
    if (inside_code >= 65281 and inside_code <= 65374):
      inside_code -= 65248
    rstring += chr(inside_code)

  return rstring

def clean_sentence(headline):
  headline = re.sub('\（.*\）','',headline).strip()  
  headline = re.sub('\＜.*\＞','',headline).strip()
  headline = re.sub('\《.*\》','',headline).strip()
  headline = re.sub('\〔.*\〕','',headline).strip()
  headline = re.sub('\[.*\]','',headline).strip()
  
  # transform SBC to DBC case
  headline = SBC_to_DBC(headline)
  # transform HK's Traditional Chinese to Simplified Chinese
  headline = HanLP.hk2s(headline)
  # remove internal space
  headline = "".join(headline.split())
  # tansform uppercase to lowercase
  headline = headline.lower()
  
  return headline

#### redefine length of words ####
def get_customize_length(org_name):
  length = 0
  for uchar in org_name:
    if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
      length += 2
    elif uchar >= u'\u0030' and uchar <= u'\u0039':
      length += 1
    elif (uchar >= u'\u0041' and uchar <= u'\u005a') or (uchar >= u'\u0061' and uchar <= u'\u007a'):
      length += 1
    else:
      length += 0

  return length  

#### if orgnization recognized contains word from cn_exclude_words table, then drop it ####
def reduce_org_by_exclude_words(org_set):
  no_wanted_orgnization_set = set()
  for org_name in org_set:
    for elem in cn_exclude_words_set:
      if org_name.find(elem) != -1: 
        no_wanted_orgnization_set.add(org_name)
        break
  org_set = set([org for org in org_set if org not in no_wanted_orgnization_set])

  return org_set

#### matching orgnization name by longest prefix ####
def longest_prefix_matching(org_set):
  if len(org_set) <= 1:
    return org_set

  org_list = list(org_set)
  no_wanted_orgnization_list = list()
  for i in range(len(org_list)):
    remain_orgnization_list = org_list[:i] + org_list[i+1:]
    for remain_orgnization in remain_orgnization_list:
      if remain_orgnization.find(org_list[i]) != -1: 
        no_wanted_orgnization_list.append(org_list[i])
  org_list = [org for org in org_list if org not in no_wanted_orgnization_list]

  return org_list

#### recognize orgnization by pyhanlp ####
def recognize_orgnization(sentence):
  total_result = []
  total_result +=  tagging_result_to_list(segment_perceptron.seg(sentence))
  total_result += tagging_result_to_list(segment_crf.seg(sentence))
  total_result += tagging_result_to_list(segment_hmm.seg(sentence))
    
  return total_result  

#### transform tagging result to list ####
def tagging_result_to_list(func_result_input):
  result = str(func_result_input)
  result = result[1:len(result)-1]
  result = result.split(",")
 
  return result

### return list of orgnization ####
def get_orgnization(total_result):
  orgnization_set = set()
  orgnization_type = ["nt","ntc","ntcb"]
  for elem in total_result:
    location = elem.find("/")
    if location != -1 and elem[location+1:].strip() in orgnization_type:
      orgnization_set.add(elem[:location].strip())

  return orgnization_set

  
#### ner module ####
def extract_ticker_ner(headline):
  org_set = set()
  symbol_set = set()
  headline = clean_sentence(headline)
  total_result = recognize_orgnization(headline)
  result = get_orgnization(total_result)
  result = reduce_org_by_exclude_words(result)                                                                                  
  result = longest_prefix_matching(result)   
  
  for org in result:
    if cn_core_dict.get(org.strip(),-1) != -1:
      org_set.add(org)
      symbol_set.add(cn_core_dict.get(org.strip(),-1))

  if len(symbol_set) == 0:
    for org in result:
      if cn_auto_dict.get(org.strip(),-1) != -1:
        org_set.add(org)
        symbol_set.add(cn_auto_dict.get(org.strip(),-1))

  return org_set, symbol_set

#### matching by identifier ####
def extract_ticker_identifier(headline): 
  org_set = set()
  symbol_set = set()
  headline = clean_sentence(headline)
  if headline.find(":") != -1:
    org_name = headline.split(":")[0].strip()
    if get_customize_length(org_name) <= 8 and cn_core_dict.get(org_name,-1) != -1:
      org_set.add(org_name) 
      symbol_set.add(cn_core_dict.get(org_name,-1))

    if len(symbol_set) == 0 and get_customize_length(org_name) <= 8 and cn_auto_dict.get(org_name,-1) != -1:
      org_set.add(org_name)
      symbol_set.add(cn_auto_dict.get(org_name,-1))
      
  return org_set, symbol_set
      
#### directly mapping ####
def extract_ticker_directly(headline):
  org_list_temp = list()
  symbol_list_temp = list()
  headline = clean_sentence(headline)
  for key,value in cn_core_dict.items():
    location = headline.find(key)
    if location != -1:
      org_list_temp.append(key)
      symbol_list_temp.append(value)  
  
  if len(symbol_list_temp) == 0:
    for key,value in cn_auto_dict.items():
      location = headline.find(key)
      if location != -1:
        org_list_temp.append(key)
        symbol_list_temp.append(value)
  org_list = longest_prefix_matching(org_list_temp)
  retain_index = [org_list_temp.index(elem) for elem in org_list]
  symbol_list = [symbol_list_temp[i] for i in retain_index]
  
  return set(org_list), set(symbol_list)

#### extract <symbol> ####
def extract_ticker_format(headline):
  org_set = set()
  symbol_set = set()
  symbol_set = re.findall('\<(\d{6}\.S[SZ])\>', headline, flags=re.IGNORECASE)  
  symbol_set = set(symbol_set)
  if len(symbol_set) == 0:
    hk_symbol_set = re.findall('\<(\d{4,5}\.HK)\>', headline, flags=re.IGNORECASE)
    for elem in hk_symbol_set:
      if cn_auto_dict.get(elem.lower(),-1) != -1:
        symbol_set.add(cn_auto_dict.get(elem.lower(),-1))

  return org_set, symbol_set
 
   












































