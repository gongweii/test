#!/usr/bin/env python                                                                                                                                              
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------
# File       : extract_prod_ticker.py
# Author     : 
# Copyright  : Dynamic Technology Lab Pte Ltd
# Description: Interface: extract ticker by production
# Created    : Wed. 15 Jan 2020 05:43:15 PM +08
# Revision   : none
#----------------------------------------------------------------------
import en_ticker_extract as ente
"""
Production info: Only lang is en, both region is eu or us
Required parameters: headline  region(us or eu)
Optional parameters: date

"""

def extract_ticker(headline,region="us",date=20171231):
  if len(headline.strip()) == 0:
    return set(),set()
  (org_list,ticker_list,three_list) = ente.extract_ticker_prod(headline,region)
  ### find bbid, return ticker_set, bbid_set
  ticker_set = set(ticker_list)
  bbid_set = set()
  for ticker in ticker_set:
    bbid_set.add(ente.find_bbid_by_ticker_and_date(ticker,region,date))
  bbid_set.discard(-1)

  return ticker_set,bbid_set
