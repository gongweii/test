#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------
# File       : extract_ticker.py
# Author     : 
# Copyright  : Dynamic Technology Lab Pte Ltd
# Description: Interface: extract ticker by company name and their productions
# Created    : Jan 15 Wed 2020 05:43:15 PM +08
# Revision   : none
#----------------------------------------------------------------------

import en_ticker_extract as ente
import cn_ticker_extract as cnte
import jp_ticker_extract as jpte
"""
If lang is English:
  Required parameters: headline  region('us' or 'eu')  lang('en')
  Optional parameters: date date_source('rp' or 'bf') use_prod(True or False)
  parameter date_source is only for US region

If lang is Chinese:
  Required parameters: headline lang('cn')
  Other parameters are not needed

If lang is Japanese:
  Required parameters: headline lang('jp')
  Other parameters are not needed
"""

def extract_ticker(headline,lang="en",region="us",date=20171231,data_source='rp',use_prod=False):
  if len(headline.strip()) == 0:
    return set(),set()
  #### US Region ####
  if lang == "en" and region == "us":
    ## first round, using us_core
    three_list_all = []
    (org_ner_list,ticker_ner_list,three_ner_list) = ente.extract_ticker_ner(headline,region)                                        # module ner
    (org_list,ticker_list,three_list) = ente.extract_ticker_format(headline)                                                        # module format  
    ticker_list += ticker_ner_list
    three_list_all += three_ner_list                                                
    three_list_all += three_list
    if data_source == "rp" and len(ticker_list) <= 0:
      (org_list,ticker_list,three_list) = ente.extract_ticker_directly(headline,region,source=data_source)                          # module directly
      three_list_all += three_list
      if len(ticker_list) <= 0:
        (org_list,ticker_list,three_list) = ente.extract_ticker_abbreviation(headline)                                              # module abbreviation
        three_list_all += three_list
    if data_source =="bf":
      (org_direct_list,ticker_direct_list,three_direct_list) = ente.extract_ticker_directly(headline,region,source=data_source)     # module directly
      ticker_list += ticker_direct_list
      three_list_all += three_direct_list
    if len(ticker_list) == 0 and len(three_list_all) > 0:
      ticker_list = three_list_all

    ## second round, using us_auto
    if len(ticker_list) <= 0:
      (org_list,ticker_list,three_list) = ente.extract_ticker_ner(headline,region,is_missing=True)                                   # module ner
      three_list_all += three_list
      if len(ticker_list) <= 0: 
        (org_list,ticker_list,three_list) = ente.extract_ticker_directly(headline,region,source=data_source,is_missing=True)         # module directly 
        three_list_all += three_list
        if len(ticker_list) <= 0:
          (org_list,ticker_list,three_list) = ente.extract_ticker_abbreviation(headline,is_missing=True)                             # module abbreviation
          three_list_all += three_list
    
          ## If use_prod is True, then call prod module
          if use_prod == True and len(ticker_list) <= 0:
            (org_list,ticker_list,three_list) = ente.extract_ticker_prod(headline,region)                                            # module production
            three_list_all += three_list
   
    if len(ticker_list) == 0 and len(three_list_all) > 0:
      ticker_list = three_list_all

    ## find bbid, return ticker_set, bbid_set
    ticker_set = set(ticker_list)
    bbid_set = set()
    for ticker in ticker_set:
      bbid_set.add(ente.find_bbid_by_ticker_and_date(ticker,region,date))
                             
    name_set = ticker_set
    symbol_set = bbid_set                                                                                                                                  
     
  #### EU region ####
  if lang == "en" and region == "eu":
    ## only one map, so one round
    three_list_all = []
    (org_ner_list,ticker_ner_list,three_ner_list) = ente.extract_ticker_ner(headline,region)                                         # module ner
    (org_list,ticker_list,three_list) = ente.extract_ticker_format(headline,region)                                                  # module format
    ticker_list += ticker_ner_list
    three_list_all += three_ner_list
    three_list_all += three_list
    
    ticker_set = set(ticker_list)
    bbid_set = set()
    for ticker in ticker_list:
      bbid = ente.find_bbid_by_ticker_with_exchange(ticker)        
      if bbid != -1:
        bbid_set.add(bbid)
        
    if len(bbid_set) <= 0:
      (org_list,ticker_list,three_list) = ente.extract_ticker_directly(headline,region,source=data_source)                            # module directly
      three_list_all += three_list
      if len(ticker_list) <= 0:
        (org_list,ticker_list,three_list) = ente.extract_ticker_similarity(headline,region)                                           # module similarity
        three_list_all += three_list

        ## If use_prod is True, then call prod module
        if use_prod == True and len(ticker_list) <= 0:
          (org_list,ticker_list,three_list) = ente.extract_ticker_prod(headline,region)                                               # module production
          three_list_all += three_list

      if len(ticker_list) == 0 and len(three_list_all) > 0:
        ticker_list = three_list_all

      ### find bbid, return ticker_set, bbid_set
      ticker_set = set(ticker_list)
      bbid_set = set()
      for ticker in ticker_set:
        bbid_set.add(ente.find_bbid_by_ticker_and_date(ticker,region,date))

    name_set = ticker_set
    symbol_set = bbid_set

  #### China Region ####
  if lang == "cn":
    (org_format_set,symbol_format_set) = cnte.extract_ticker_format(headline)                                                         # module format
    (org_set,symbol_set) = cnte.extract_ticker_identifier(headline)                                                                   # module identifier
    org_set = org_set | org_format_set
    symbol_set = symbol_set | symbol_format_set
    if len(symbol_set) <= 0:
      (org_set,symbol_set) = cnte.extract_ticker_ner(headline)                                                                        # module ner
      if len(symbol_set) <= 0:
        (org_set,symbol_set) = cnte.extract_ticker_directly(headline)                                                                 # module directly

    name_set = org_set

  #### Japan ####
  if lang == "jp":
    is_missing = False
    three_list_all = []
    (org_format_set,symbol_format_set,three_format_set) = jpte.extract_ticker_format(headline)                                         # module format
    (org_set,symbol_set,three_set) = jpte.extract_ticker_ner(headline)                                                                 # module ner
    org_set = org_set | org_format_set
    symbol_set = symbol_set | symbol_format_set
    three_list_all += list(three_format_set)
    three_list_all += list(three_set)
    if len(symbol_set) <= 0:
      (org_set,symbol_set,three_set) = jpte.extract_ticker_directly(headline,is_missing)                                               # module directly
      three_list_all += list(three_set)
    if len(symbol_set) == 0 and len(three_list_all) == 0:
      is_missing = True
      (org_set,symbol_set,three_set) = jpte.extract_ticker_directly(headline,is_missing)                                               # module directly
      three_list_all += list(three_set)
    if len(symbol_set) == 0 and len(three_list_all) > 0:
      symbol_set = set(three_list_all)

    name_set = org_set
  symbol_set.discard(-1)
  return name_set,symbol_set
