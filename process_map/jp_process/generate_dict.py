import pdb

mix_jp_core_file = "../../map/jp_mix_core"
jp_core = []
with open(mix_jp_core_file,"r",encoding="utf-8") as inf:
  for line in inf:
    #prim_org = line.split("|")[1].strip()
#    if not all(ord(char)<128 for char in prim_org):
    jp_core.append(line.rstrip("\n"))

jp_org_dict_file = "../../map/jp_org_dict.csv"
with open(jp_org_dict_file,"a",encoding="utf-8") as outf:
  for line in jp_core:
    pri_org = line.split("|")[1].strip()
    h_org = line.split("|")[1].strip()
    k_org = line.split("|")[1].strip()
    a_org = line.split("|")[1].strip()
    line = pri_org + ",1292,1292,1,名詞,固有名詞,組織,*,*,*," + h_org + "," + k_org + "," + a_org
    print(line.rstrip("\n"),file=outf)


