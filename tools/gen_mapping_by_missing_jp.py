import pdb
import MeCab
import string

import jp_ticker_extract as ts

mecab = MeCab.Tagger("-Ochasen")

#headline = "PCテクノロジー株式会社との業務提携及び出資について"
#headline = "株式会社キーポート・ソリューションズの株式取得(連結子会社化)に関するお知"
#headline = "株式会社ビーエス・ジェイの株式の取得(子会社化)に関する株式譲渡契約締結な"
headline = "株式会社Coolpatの全株式の取得(子会社化)と簡易吸収分割による事業承継につ"
#headline = "株式会社クオカードの株式の取得(子会社化)に関するお知らせ"
#headline = "シーエムジャパン株式会社の株式の取得(子会社)に関するお知らせ"

def get_subcorp(headline):
  org_list_temp = []
  symbol_list_temp = []
  headline = ts.clean_sentence(headline)
  tag_result = mecab.parse(headline)
  tag_result = tag_result.split("\t")
  tag_result = [elem.strip() for elem in tag_result if elem != '']
  org_tagging_set = set()
  # ignore EOS flag 
  remove_list = ["株式","社","事業","業務","基本","第三者","取締役","名詞","交通省","貸付","商号","孫","所在地","土地","その他","前受金","助詞","合弁","厚生",\
                 "債権","遺伝子","医科大","大学","国内","株","資本","取消","見通","知ら","人事","接続","債権","役員","特例","自己","投融資","グループ","カタリスト","半期","ストックオプシ"]
  for i in range(len(tag_result)-1):
    if "組織" in tag_result[i] and i >= 3 or "名詞-一般" in tag_result[i] and i >= 3:
      tag_result[i-3] = tag_result[i-3].strip()
      if ts.reduce_org_by_exclude_words(tag_result[i-3],headline) != -1 and not all(ord(char)<128 for char in tag_result[i-3].strip()) and ts.is_valid_katakana_comapny_name(tag_result[i-3],headline):
        org_tagging_set.add(tag_result[i-3].strip())
      location = headline.find(tag_result[i-3].strip())
      if ts.reduce_org_by_exclude_words(tag_result[i-3],headline) != -1 and all(ord(char) < 128 for char in tag_result[i-3].strip()):      
        if location == 0 and ((location+len(tag_result[i-3]) < len(headline) and ((headline[location+len(tag_result[i-3])] in string.punctuation) or ord(headline[location+len(tag_result[i-3])])>=128))  or location+len(tag_result[i-3]) == len(headline)):
          org_tagging_set.add(tag_result[i-3].strip())
        if location > 0 \
          and ((location+len(tag_result[i-3]) < len(headline) and ((headline[location+len(tag_result[i-3])] in string.punctuation) or ord(headline[location+len(tag_result[i-3])])>=128))  or location+len(tag_result[i-3]) == len(headline)) and (ord(headline[location-1]) >= 128 or headline[location-1] in string.punctuation):
          org_tagging_set.add(tag_result[i-3].strip())

  org_set = set()
  for org in org_tagging_set:
    num = 0
    for elem in remove_list:
      if org.find(elem) > -1:
        break
      else:
        num += 1
      if num == len(remove_list) and len(org) > 2:
        org_set.add(org)
  return org_set

def write_miss_more(miss_set):
  file_name = "res/miss_more"
  with open(file_name,"a",encoding="utf-8") as outf:
    for line in miss_set:
      print(line.strip(),file=outf)
def write_miss_zero(miss_set):
  file_name = "res/miss_zero"
  with open(file_name,"a",encoding="utf-8") as outf:
    for line in miss_set:
      print(line.strip(),file=outf)
def write_miss_one_wrong(miss_set):
  file_name = "res/miss_one_wrong"
  with open(file_name,"a",encoding="utf-8") as outf:
    for line in miss_set:
      print(line.strip(),file=outf)
def write_miss_one_right(miss_set):
  file_name = "res/miss_one_right"
  with open(file_name,"a",encoding="utf-8") as outf:
    for line in miss_set:
      print(line.strip(),file=outf)
def write_auto(auto_dict):
  file_name = "res/auto_dict"
  with open(file_name,"a",encoding="utf-8") as outf:
    for k,v in auto_dict.items():
      output_line = "2|"+k.lower().strip()+"|"+v.strip()
      print(output_line.strip(),file=outf)
def write_miss_remain(miss_set):
  file_name = "res/miss_remain"
  with open(file_name,"a",encoding="utf-8") as outf:
    for line in miss_set:
      print(line.strip(),file=outf)

jp_auto_plus = "../map/jp_auto_plus"
auto_dict = {}
with open(jp_auto_plus,"r",encoding="utf-8") as inf:
  for line in inf:
    auto_dict[line.split("|")[1].strip().lower()] = line.split("|")[2].strip().upper()
    
begain_index = 75812
missing_file = "missing_sort"
miss_more = []
miss_zero = []
miss_one_wrong = []
miss_one_right = []
miss_remain = []
with open(missing_file,"r",encoding="utf-8") as inf:
  for i,line in enumerate(inf):
    if begain_index >= i:
      continue
    if i%100 == 0:
      print("Done: ",i)

    headline = line.split("|")[1].strip()
    headline = ts.clean_sentence(headline)
    ticker = line.split("|")[2].strip()
    if headline.find("子会社") == -1 and headline.find("孫会社") == -1:
      miss_remain.append(line.strip())
      continue

    org_set = get_subcorp(headline) 
    
    # if more than 1 org_name,record it
    if len(org_set) > 1:
      miss_more.append(line.strip())
    if len(org_set) == 1:
      org = org_set.pop().lower()
      if org in auto_dict and ticker != auto_dict[org].upper():
        miss_one_wrong.append(line.strip())
      else:
        auto_dict[' '.join(org.split('\n'))] = ticker
        miss_one_right.append(line.strip())
        
    if len(org_set) == 0:
      miss_zero.append(line.strip())

write_miss_more(miss_more)
write_miss_zero(miss_zero)
write_miss_one_wrong(miss_one_wrong)
write_miss_one_right(miss_one_right)
write_auto(auto_dict)
write_miss_remain(miss_remain)
