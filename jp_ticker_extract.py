#!/usr/bin/env python                                                                                                                                               
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------
# File       : jp_ticker_extract.py
# Author     : 
# Copyright  : Dynamic Technology Lab Pte Ltd
# Description: Japanese Language
# Created    : Fri 9 Aug 2019 09:00:00 AM SGT
# Revision   : none
#----------------------------------------------------------------------
import re
import MeCab
import string
import pdb

mecab = MeCab.Tagger("-Ochasen")
string.punctuation += " 【 】「」~・:："
dbc_katakana = "ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁｯﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛｦﾝｬｭｮｰｧｨｩｪｫ･◎★◇*"
sbc_katakana = "アイウエオカキクケコサシスセソタチッツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロヲンャュョーァィゥェォ・    "
sbc_katakana_sign = "アイウエオカキクケコサシスセソタチッツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロヲンャュョーァィゥェォデブいプビボグパデジデザポド"

#### Read map ####
jp_core_file = "map/jp_mix_core"
jp_core_dict = {}
with open(jp_core_file,"r",encoding="utf-8") as inf:
  for line in inf:
    jp_core_dict[line.split("|")[1].strip()] = line.split("|")[5].rstrip("\n")
        
jp_auto_file = "map/jp_auto"
jp_auto_dict = {}
with open(jp_auto_file,"r",encoding="utf-8") as inf:
  for line in inf:
    jp_auto_dict[line.split("|")[1].strip()] = line.split("|")[2].rstrip("\n")
jp_auto_plus_file = "map/jp_auto_plus"
jp_plus_dict = {}
with open(jp_auto_plus_file,"r",encoding="utf-8") as inf:
  for line in inf:
    jp_plus_dict[line.split("|")[1].strip()] = line.split("|")[2].rstrip("\n")

three_party_file = "map/jp_three_party"
three_party_set = set()
with open(three_party_file,"r",encoding="utf-8") as inf:
  for line in inf:
    three_party_set.add(line.split("|")[1].strip())

jp_exclude_words_file = "map/jp_exclude_words"
jp_exclude_words_set = set()
with open(jp_exclude_words_file,"r",encoding="utf-8") as inf:
  for line in inf:
    jp_exclude_words_set.add(line.rstrip("\n"))

def exclude_three_part(symbol_set):
  normal_set = set()
  three_set = set()
  for elem in symbol_set:
    if elem in three_party_set:
      three_set.add(elem)
    else:
      normal_set.add(elem)
  return normal_set,three_set

#### transform SBC to DBC case ####
def alphabet_SBC_to_DBC(ustring):
  rstring = ""
  for uchar in ustring:
    inside_code=ord(uchar)
    if inside_code == 12288:
      inside_code = 32
    if (inside_code >= 65281 and inside_code <= 65374):
      inside_code -= 65248
    rstring += chr(inside_code)
  
  return rstring

def katakana_SBC_to_DBC(ustring):
  sbc_string = ""
  for char in ustring:
    if char in dbc_katakana:
      location = dbc_katakana.index(char)
      sbc_char = sbc_katakana[location]
      sbc_string += sbc_char
    else:
      sbc_string += char

  return sbc_string

def reduce_org_by_exclude_words(org_name,headline):
  for elem in jp_exclude_words_set:
    if org_name in elem and elem in headline:
      return -1

  return org_name

## Only remove space between Japanese, not English
def remove_space(headline):
  pattern = re.compile(u"[(\u0800-\u4e00|\u4e00-\u9fa5)\\\.\:\(\)\~【】\[\]]+|[a-zA-Z0-9\.\(\)\-「」、\&\!\#\$\%\&\*\+\,\-\.\/\:\;\<\=\>\?\@\^_\`\{\|\}\~]+|[a-zA-Z0-9\.\\\(\)\-\~【】\&「」]+")
  en_text = re.findall(pattern,headline)
  result = ""
  for i in range(len(en_text)):
    if i == 0:
      result += en_text[i]
    elif all(ord(char)<128 for char in en_text[i-1]) and all(ord(char)<128 for char in en_text[i]) and en_text[i-1][-1] not in ('('):
      result += " " + en_text[i]
    else:
      result += en_text[i]
  return result

  
def clean_sentence(headline):
  # transform SBC case to DBC case
  headline = alphabet_SBC_to_DBC(headline)
  headline = katakana_SBC_to_DBC(headline)
#  headline = remove_space(headline)
  headline = headline.lower()
  
  return headline

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

def is_valid_katakana_comapny_name(org_name,headline):
  headline = clean_sentence(headline)
  flag = False
  for char in org_name:
    if not (char >= u'\u30a0' and char <= u'\u30ff'):
      flag = True
  if flag == False:
    location = headline.find(org_name) 
        
    if location != -1: 
      if (location > 0 and (headline[location-1] in sbc_katakana_sign)) \
        or (location + len(org_name) < len(headline) and (headline[location+len(org_name)] in sbc_katakana_sign)):
        flag = False
      elif headline.find("/") < len(headline)-1 and headline[headline.find("/")+1] == org_name[0]:
        flag = True
      else:
        flag = True
    else:                                                                                                                                                                                                   
      flag = True
  return flag

### extract by format ####
def extract_ticker_format(headline):
  org_set = set()
  symbol_set = set()
  symbol_set = re.findall('\<(\d{4}\.T)\>', headline, flags=re.IGNORECASE)  
  if len(symbol_set) == 0:
    symbol_set = re.findall('\((\d{4})\s*\**\s*[J]*\)', headline,flags=re.IGNORECASE)
    if len(symbol_set) == 0:
      symbol_set = re.findall("\(.*コード\s*\:*\s*(\d{4})\)",headline,flags=re.IGNORECASE)
      if len(symbol_set) == 0:
        symbol_set = re.findall("\(東証\w*\s*\:*\s*(\d{4})\)",headline,flags=re.IGNORECASE)
    symbol_set = [elem.rstrip('.T')+'.T' for elem in symbol_set]
  symbol_set = set(symbol_set)   

  return org_set, symbol_set, set()

### extract by ner ### 
def extract_ticker_ner(headline):
  # using user-customize orgniazation dictionary
  org_list_temp = []
  symbol_list_temp = []
  headline = clean_sentence(headline)
  tag_result = mecab.parse(headline)
  tag_result = tag_result.split("\t")
  tag_result = [elem.strip() for elem in tag_result if elem != '']
  org_tagging_set = set()
  # ignore EOS flag 
  for i in range(len(tag_result)-1):
    if "組織" in tag_result[i] and i >= 3:
      tag_result[i-3] = tag_result[i-3].strip()
      if reduce_org_by_exclude_words(tag_result[i-3],headline) != -1 and not all(ord(char)<128 for char in tag_result[i-3].strip()) and is_valid_katakana_comapny_name(tag_result[i-3],headline):
        org_tagging_set.add(tag_result[i-3].strip())
      location = headline.find(tag_result[i-3].strip())
      if reduce_org_by_exclude_words(tag_result[i-3],headline) != -1 and all(ord(char) < 128 for char in tag_result[i-3].strip()):
        if location == 0 and ((location+len(tag_result[i-3]) < len(headline) and ((headline[location+len(tag_result[i-3])] in string.punctuation) or ord(headline[location+len(tag_result[i-3])])>=128))  or location+len(tag_result[i-3]) == len(headline)):
          org_tagging_set.add(tag_result[i-3].strip())
        if location > 0 \
          and ((location+len(tag_result[i-3]) < len(headline) and ((headline[location+len(tag_result[i-3])] in string.punctuation) or ord(headline[location+len(tag_result[i-3])])>=128))  or location+len(tag_result[i-3]) == len(headline)) and (ord(headline[location-1]) >= 128 or headline[location-1] in string.punctuation):
          org_tagging_set.add(tag_result[i-3].strip())
  for org in org_tagging_set:
    if jp_core_dict.get(org.strip(),-1) != -1:
      org_list_temp.append(org.strip())
      symbol_list_temp.append(jp_core_dict.get(org.strip(),-1))

  org_list = longest_prefix_matching(org_list_temp)
  retain_index = [org_list_temp.index(elem) for elem in org_list]
  symbol_list = [symbol_list_temp[i] for i in retain_index]

  return set(org_list), exclude_three_part(set(symbol_list))[0],exclude_three_part(set(symbol_list))[1]        

### extract by directly ###
def extract_ticker_directly(headline,is_missing=False):
  org_list_temp = []
  symbol_list_temp = []
  headline = clean_sentence(headline)
  
  if is_missing:
    for key,value in jp_plus_dict.items():
      location = headline.find(key)
      if location != -1 and all(ord(char)<128 for char in key) and reduce_org_by_exclude_words(key,headline) != -1: 
        if location == 0 and \
        ((location+len(key) < len(headline) and ((headline[location+len(key)] in string.punctuation) or ord(headline[location+len(key)])>=128)) or location+len(key) == len(headline)):
          org_list_temp.append(key)
          symbol_list_temp.append(value)
        if location > 0\
          and ((location+len(key) < len(headline) and (ord(headline[location+len(key)]) >= 128 or headline[location+len(key)] in string.punctuation)) or location+len(key) == len(headline)) \
          and (ord(headline[location-1]) >= 128 or headline[location-1] in string.punctuation):
          org_list_temp.append(key)
          symbol_list_temp.append(value)
      if location != -1 and not all(ord(char)<128 for char in key) and reduce_org_by_exclude_words(key,headline) != -1 and is_valid_katakana_comapny_name(key,headline):
        org_list_temp.append(key)
        symbol_list_temp.append(value) 

    org_list = longest_prefix_matching(org_list_temp)
    retain_index = [org_list_temp.index(elem) for elem in org_list]
    symbol_list = [symbol_list_temp[i] for i in retain_index]

    return set(org_list), exclude_three_part(set(symbol_list))[0],exclude_three_part(set(symbol_list))[1]
 
  for key,value in jp_core_dict.items():
    location = headline.find(key)
    if location != -1 and all(ord(char)<128 for char in key) and reduce_org_by_exclude_words(key,headline) != -1:
      if location == 0 and ((location+len(key) < len(headline) \
        and (ord(headline[location+len(key)]) >= 128) or headline[location+len(key)] in string.punctuation) or location+len(key) == len(headline)):
        org_list_temp.append(key)
        symbol_list_temp.append(value)
      if location > 0 \
        and ((location+len(key) < len(headline) and (ord(headline[location+len(key)]) >= 128 or headline[location+len(key)] in string.punctuation)) or location+len(key) == len(headline)) \
        and (ord(headline[location-1]) >= 128 or headline[location-1] in string.punctuation):
        org_list_temp.append(key)
        symbol_list_temp.append(value)
    if location != -1 and not all(ord(char)<128 for char in key) and reduce_org_by_exclude_words(key,headline) != -1 and is_valid_katakana_comapny_name(key,headline):
      org_list_temp.append(key)
      symbol_list_temp.append(value) 
    
  if len(exclude_three_part(set(symbol_list_temp))[0]) == 0:
    for key,value in jp_auto_dict.items():
      location = headline.find(key)
      if location != -1 and all(ord(char)<128 for char in key) and reduce_org_by_exclude_words(key,headline) != -1:
        if location == 0 and ((location+len(key) < len(headline) \
          and (ord(headline[location+len(key)]) >= 128) or headline[location+len(key)] in string.punctuation) or location+len(key) == len(headline)):
          org_list_temp.append(key)
          symbol_list_temp.append(value)
        if location > 0 \
          and ((location+len(key) < len(headline) and (ord(headline[location+len(key)]) >= 128 or headline[location+len(key)] in string.punctuation)) or location+len(key) == len(headline)) \
          and (ord(headline[location-1]) >= 128 or headline[location-1] in string.punctuation):
          org_list_temp.append(key)
          symbol_list_temp.append(value)
      if location != -1 and not all(ord(char)<128 for char in key) and reduce_org_by_exclude_words(key,headline) != -1 and is_valid_katakana_comapny_name(key,headline):
        org_list_temp.append(key)
        symbol_list_temp.append(value) 

  org_list = longest_prefix_matching(org_list_temp)
  retain_index = [org_list_temp.index(elem) for elem in org_list]
  symbol_list = [symbol_list_temp[i] for i in retain_index]

  return set(org_list), exclude_three_part(set(symbol_list))[0],exclude_three_part(set(symbol_list))[1]
