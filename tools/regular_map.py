import pdb

equal_words_file = "../map/en_equal_pair"
equal_words = {}
with open(equal_words_file,"r",encoding="utf-8") as inf:
  for line in inf:
    equal_words[line.split("|")[0].rstrip("\n")] = line.split("|")[1].rstrip("\n")

#### Regular org name and headline ####
def regular_sentence(key,region="us"):
  # exclude interference from & and -
  if region == "eu":
    reg_key = ' '.join(key.split())
    for k,v in equal_words.items():
      reg_key = ' ' + ' '.join(reg_key.split()) + ' '
      reg_key = reg_key.replace(k, v)
  else:
    equal_pair = {' & ':' and ', '-':' '}
    reg_key = ' '.join(key.split())
    for k,v in equal_pair.items():
      reg_key = reg_key.replace(k, v)
  reg_key = ' '.join(reg_key.split())
  return reg_key

map_file = "eu_prob1"
map_list = []
with open(map_file,"r",encoding="utf-8") as inf:
  for line in inf:
    if len(line.split("|")) != 3:
      print(line)
    else:
      flag = line.split("|")[0].strip()
      raw_org = line.split("|")[1].strip()
      ticker = line.split("|")[2].strip()
#      bbid = line.split("|")[3].strip()
      org = regular_sentence(raw_org,region="eu")
 #     output_line = flag + "|" + org + "|" + ticker + "|" + bbid
      output_line = flag + "|" + org + "|" + ticker
      map_list.append(output_line)

map_file = "../map/eu_prob"
with open(map_file,"a",encoding="utf-8") as outf:
  for line in map_list:
    print(line.strip(),file=outf)

