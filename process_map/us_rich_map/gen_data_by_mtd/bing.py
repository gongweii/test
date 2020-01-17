#!/user/bin/env python 
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------
# File       : bing.py
# Author     : 
# Copyright  : Dynamic Technology Lab Pte Ltd                                                                                                                                                         
# Created    : 
# Revision   : none
#---------------------------------------------------------------------
import requests
import random
import time
import socket
import re
import pdb 
	
class BingAPI():
  def __init__(self):
    timeout = 20
    socket.setdefaulttimeout(timeout)
    self.headers = {
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Language': 'en-us;q=0.5,en;q=0.3',
      'Cache-Control': 'max-age=0',
      'Connection': 'keep-alive',
      'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'
    }
    self.base_url = "https://global.bing.com"

  def random_sleep(self):
    sleeptime = random.randint(1, 3)
    time.sleep(sleeptime)
  
  ### extract ticker symbol from HTMLText
  def parse_html_text(self,html):
    pattern = re.compile('<div class="fin_metadata b_demoteText">(.*?)(&|</div>)',re.S)
    res = re.search(pattern,html)
    if type(res) == type(None):
      return None
    res = res.group().strip()
    start_index = res.index(':')+1
    if res.find('&'):
      end_index = res.index('&')
    else:
      end_index = res.index('</div>')
    ticker = res[start_index:end_index].strip()
    return ticker
  
  ### send request
  def search(self, query, lang = 'en'):
    url = '%s/search?q=%s&qs=bs&ajf=60&first=1&Accept-Language=%s' % (self.base_url, query, lang)
    # if crawl failure,try it no more than 3 times
    retry = 3
    ticker = ''
    while retry > 0:
      try:
        r = requests.get(url=url, headers=self.headers)
        r.raise_for_status()
        html = r.content.decode('utf-8')
        ticker = self.parse_html_text(html)
        break
      except:
        print('crawl failure')
        retry -= 1
        self.random_sleep()
        continue
    return ticker

### start crawl
def crawler(org_set):
  ticker = None
  api = BingAPI()
  for org_mtd in org_set:
    ticker =  api.search(org_mtd+" ticker")
    if type(ticker) != type(None):
      break
  return ticker
