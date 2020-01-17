import pykakasi
import re
import pdb
kakasi = pykakasi.kakasi()

jp_core_file = "../../map/jp_core"
jp_core = []
with open(jp_core_file,"r",encoding="utf-8") as inf:
  for line in inf:
    jp_core.append(line.rstrip("\n"))

# transform to Hiragana
jp_core_h = []
kakasi.setMode("J","H")
conv = kakasi.getConverter()
for line in jp_core:
  elem = line.split("|")[1].strip()
  elem = conv.do(elem)
#  elem = re.sub("\<.*\>","",elem).strip()
  new_line = "1|" + elem + "|" + line.split("|")[2].rstrip("\n")
  jp_core_h.append(new_line)

# transform to Katakana
jp_core_k = []
kakasi.setMode("J","K")
kakasi.setMode("H","K")
conv = kakasi.getConverter()
for line in jp_core:
  elem = line.split("|")[1].strip()
  elem = conv.do(elem)
  elem = re.sub("\<.*\>","",elem).strip()
  new_line = "1|" + elem + "|" + line.split("|")[2].rstrip("\n")
  jp_core_k.append(new_line)

# transform to Alphabet
jp_core_a = []
kakasi.setMode("J","a")
kakasi.setMode("H","a")
kakasi.setMode("K","a")
kakasi.setMode("r","Hepburn")
kakasi.setMode("s", True)
conv = kakasi.getConverter()
for line in jp_core:
  elem = line.split("|")[1].strip()
  elem = conv.do(elem)
  elem = re.sub("\<.*\>","",elem).strip()
  new_line = "1|" + elem + "|" + line.split("|")[2].rstrip("\n")
  jp_core_a.append(new_line)


#
mix_jp_core_set = []
for i in range(len(jp_core)):
  prim_org = jp_core[i].split("|")[1].strip()
  h_org = jp_core_h[i].split("|")[1].strip()
  k_org = jp_core_k[i].split("|")[1].strip()
  a_org = jp_core_a[i].split("|")[1].strip()
  symbol = jp_core[i].split("|")[2].rstrip("\n")

  line = "1|" + prim_org + "|" + h_org + "|" + k_org + "|" + a_org + "|" + symbol
  mix_jp_core_set.append(line.rstrip("\n"))

mix_jp_core_file = "../../map/jp_mix_core"
with open(mix_jp_core_file,"a",encoding="utf-8") as outf:
  for line in mix_jp_core_set:
    print(line.rstrip("\n"),file=outf)

