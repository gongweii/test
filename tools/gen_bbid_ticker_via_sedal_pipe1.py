import pandas as pd
import numpy as np
import os
import pdb

def read_ric_map(path):
  df_ric = pd.read_csv(path,header=None,names=["sedal_ticker"])
  #df_ric.insert(1,'sedal',df['sedal_ticker']) 
  df_ric['sedal'] = df_ric['sedal_ticker'].map(lambda x:x.split("|")[0].strip())
  df_ric['ticker'] = df_ric['sedal_ticker'].map(lambda x:x.split("|")[1].strip())
  df_ric = df_ric.drop('sedal_ticker',axis=1)
  
  return df_ric

def read_raw_prc(path):
  df_raw = pd.read_csv(path,header=None,names=range(1,23))
  df_raw = df_raw[[1,2]]
  df_raw.rename(columns={1:"bbid",2:"sedal"},inplace=True)
  
  return df_raw

def merge_df(df_raw,df_ric):
  df = pd.merge(df_raw,df_ric)
  df = df.drop('sedal',axis=1)
  df = df.drop_duplicates()
  df = df.sort_values(by="bbid")
  df = df.reset_index(drop=True)

  df = df.dropna(axis=0,how="any")
  df = df[~(df['ticker'] == 'n/a')]
  
  return df

df_all = pd.DataFrame(columns=["bbid","ticker"])

### reverse ric dir
ric_dir = "/export/scratch/for_wgong/eu_data/ric_map_eu"
raw_dir = "/export/scratch/for_wgong/eu_data/raw_prc_eu"
count = 0
for file_name  in os.listdir(raw_dir):
  count += 1
  print("Done: " + str(count) + "file is " + file_name)
  
  date = file_name[-8:]
  raw_path = os.path.join(raw_dir,file_name)
  ric_path = ric_dir + '/' + "ric_map." + date

  df_raw = read_raw_prc(raw_path)
  try:
    df_ric = read_ric_map(ric_path)
  except:
    print("file read error:  ric_map.",date)
  df = merge_df(df_raw,df_ric)
  df_all = pd.concat([df_all,df])
  df_all = df_all.drop_duplicates()

df_all = df_all.drop_duplicates()
df_all = df_all.sort_values(by="bbid")

### write file
bbid_path = "bbid_eu"
last_bbid = ""
with open(bbid_path,"a",encoding="utf-8") as outf:
  for index,row in df_all.iterrows():
    bbid = row["bbid"]
    ticker = row['ticker']
    if bbid == last_bbid:
      print("confilt: " + bbid + " " + ticker)
    output_line = bbid.strip() + "|" + ticker.strip() + "|" + "20100101|20171229"
    print(output_line,file=outf)

pdb.set_trace()




