import pdb

#data_file = "/export/scratch/for_wgong/nq_jp_2018_h1"
#data_file = "../cn_data/ns_cn_till_2015"
data_file = "/export/scratch/for_wgong/ns_eu_2016"
train_data = []
with open(data_file,"r",encoding="utf-8") as inf:
  for line in inf:
    train_data.append(line.strip())

n = len(train_data)
step = n//200
rand_data = train_data[::step]
rand_data = rand_data[0:200]

data_file="../eu_data/eunsos_200"
with open(data_file,"a",encoding="utf-8") as outf:
  for line in rand_data:
    print(line.strip(),file=outf)
