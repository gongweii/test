import pandas as pd
import numpy as np
import os
import pdb

def read_raw_prc(path):
  df_raw = pd.read_csv(path,header=None,names=range(1,23))
  df_raw = df_raw[[1,2]]
  df_raw.rename(columns={1:"bbid",2:"sedol"},inplace=True)
  
  return df_raw

prob_file = "/export/scratch/for_wgong/trade_mark/prod.20170516"
def read_prob(prob_file):
  df_prob = pd.read_csv(prob_file,header=None,names=["mix_col"])
  df_prob["sedol"] = df_prob["mix_col"].map(lambda x:x.split("|")[3].strip())
  df_prob["ticker"] = df_prob["mix_col"].map(lambda x:x.split("|")[1].strip())
  df_prob["prob"] = df_prob["mix_col"].map(lambda x:x.split("|")[5].strip())
  df_prob = df_prob.drop("mix_col",axis=1)

  return df_prob


df_raw_ric = pd.DataFrame(columns=["bbid","sedol","ticker"])

### reverse ric dir
raw_dir = "/export/scratch/for_wgong/eu_data/raw_prc_eu"
count = 0
for file_name  in os.listdir(raw_dir):
  count += 1
  print("Done: " + str(count) + " file is " + file_name)
  if file_name[:9] == "raw_price":
    raw_path = os.path.join(raw_dir,file_name)
    df_raw = read_raw_prc(raw_path)

df_raw = df_raw.drop_duplicates()

df_prob = read_prob(prob_file)
df_all = df_raw.set_index('sedol').join(df_prob.set_index("sedol"))
df_all = df_all.dropna(axis=0,how="any")
df_all = df_all.drop_duplicates()

prob_bbid_ticker_file = "eu_prob_bbid_ticker"
with open(prob_bbid_ticker_file,"a",encoding="utf-8") as outf:
  for index,row in df_all.iterrows():
    bbid = row["bbid"]
    ticker = row["ticker"]
    prob = row["prob"]
    output_line = bbid + "|" + ticker + "|" + prob
    print(output_line,file=outf)
