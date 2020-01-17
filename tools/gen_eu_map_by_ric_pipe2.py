import pdb
import os

ric_dir = "/export/scratch/for_wgong/eu_data/ric_map_eu"
eu_map = []
count = 0
for file_name  in os.listdir(ric_dir):
  print(count)
  count += 1
  ric_path = os.path.join(ric_dir,file_name)
  with open(ric_path,"r",encoding="utf-8") as inf:
    for line in inf:
      if len(line.split("|")) == 3 and line.split("|")[2].strip() != "" and line.split("|")[1].strip() not in ["n/a","n/s"]:
        org_name = line.split("|")[2].strip().lower()
        ticker = line.split("|")[1].strip()
        output_line = "1|"+org_name+"|"+ticker
        if output_line not in eu_map:
          eu_map.append(output_line)

eu_map_path = "eu_map_by_ric"
with open(eu_map_path,"a",encoding="utf-8") as outf:
  for line in eu_map:
    print(line.strip(),file=outf)
  
