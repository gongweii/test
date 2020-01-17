import pdb
import re

cn_file = "../map/cn_core"
cn_list = []
with open(cn_file,"r",encoding="utf-8") as inf:
  for line in inf:
    cn_list.append(line.strip())
    name = line.split("|")[1].strip()
    if name[:3] == "*st":
      name = 'st'+name[3:]
    if name[:3] == "sst":
      name = 'st' + name[3:]
    if name[:4] == "s*st":
      name = "st" + name[4:]
    output_line1 = "1|"+name.strip()+"|"+line.split("|")[2].strip()
    if output_line1.strip() != line.strip():
      cn_list.append(output_line1.strip())

    if name.find("ｂ股") != -1:
      name = name[:name.find("ｂ股")] + "b"
    if name.find("ａ股") != -1:
      name = name[:name.find("ａ股")] + "a"
    if name.find("ａ") != -1:
      name = name[:name.find("ａ")] + "a"
    if name.find("ｂ") != -1:
      name = name[:name.find("ｂ")] + "b"
    output_line = "1|"+name.strip()+"|"+line.split("|")[2].strip()
    if output_line.strip() != line.strip() and output_line.strip() != output_line1.strip():
      cn_list.append(output_line.strip())
cn_file = "../map/cn_core1"
with open(cn_file,"a",encoding="utf-8") as outf:
  for line in cn_list:
    print(line.strip(),file=outf)
pdb.set_trace()
