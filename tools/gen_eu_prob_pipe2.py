import pdb
import re

eu_bbid_file = "../map/eu_bbid_ticker_with_date_range"
eu_bbid_set = set()
with open(eu_bbid_file,"r",encoding="utf-8") as inf:
  for line in inf:
    bbid = line.split("|")[0].strip()
    ticker = line.split("|")[1].strip()
    eu_bbid_set.add(bbid+"|"+ticker)

add_bbid_set = set()
eu_prob = []
eu_prob_bbid_ticker_file = "eu_prob_bbid_ticker"
with open(eu_prob_bbid_ticker_file,"r",encoding="utf-8") as inf:
  for line in inf:
    bbid = line.split("|")[0].strip()
    ticker = line.split("|")[1].strip()
    ticker = re.sub("\s*-\s*",".",ticker)
    prob = line.split("|")[2].strip()
    bbid_ticker = bbid+"|"+ticker
    if bbid_ticker not in eu_bbid_set:
      add_bbid_set.add(bbid_ticker+"|20100101|20171229")
    eu_prob.append("1|"+prob+"|"+ticker)

eu_prob_file = "eu_prob"
with open(eu_prob_file,"a",encoding="utf-8") as outf:
  for line in eu_prob:
    print(line.strip(),file=outf)

with open(eu_bbid_file,"a",encoding="utf-8") as outf:
  for line in add_bbid_set:
    print(line.strip(),file=outf)
