import pdb

us_bbid_file = "../map/us_bbid_ticker_with_date_range"
prob_file = "/export/scratch/for_wgong/trade_mark/prod.20170516"
ticker_set = set()
with open(us_bbid_file,"r",encoding="utf-8") as inf:
  for line in inf:
    ticker = line.split("|")[1].strip()
    ticker_set.add(ticker)

prob_list = []
with open(prob_file,"r",encoding="utf-8") as inf:
  for line in inf:
    ticker = line.split("|")[1].strip()
    org_name = line.split("|")[5].strip()
    if ticker in ticker_set:
      prob_list.append("1|"+org_name.strip()+"|"+ticker.strip())

us_prob_file = "us_prob"
with open(us_prob_file,"a",encoding="utf-8") as outf:
  for line in prob_list:
    print(line.strip(),file=outf)
