import time
import pdb
import extract_ticker as et

missing_num = 0
error_num = 0
right_num = 0
perfect_num = 0
time0 = time.time()

#train_data = "jp_data/ns_jp_till_2015"
#train_data = "out_sample/bf_train_data_2016_10000"
#train_data = "/home/wgong/tt/tools/res/miss_more"
#train_data = "/home/wgong/tt/tools/res/miss_remain"
#train_data = "/export/scratch/for_wgong/nq_jp_2018_h1"
#train_data = "cn_data/ns_cn_100"
#train_data = "eu_data/ns_eu_till_2015"
train_data = "/export/scratch/for_wgong/ns_eu_2016"
#train_data = "eu_data/eunsos_200"
with open(train_data,"r",encoding="utf-8") as inf:
  for i,line in enumerate(inf):
    if (i+1)%100 == 0:
      print("done:",i+1,"missing:",missing_num,"error:",error_num,"right:",right_num,"perfect:",perfect_num,"take time:",time.time()-time0)
    headline = line.split("|")[1].strip()
    symbol = line.split("|")[3].strip()
    date = line.split("|")[0].strip()
    (name_set,symbol_set) = et.extract_ticker(headline,lang="en",region="eu",date=date,use_prod=False)
    ### compare by symbol
    outputfile_missing = "result/eu/missing_euos_all_noprod"
    outputfile_error = "result/eu/error_euos_all_noprod"
    outputfile_right = "result/eu/right_euos_all_noprod"
    outputfile_perfect = "result/eu/perfect_euos_all_noprod"
    ## record as missing
    if len(symbol_set) == 0:
      missing_num += 1
      with open(outputfile_missing,'a') as outf:
        print(line.strip(),file = outf)
    
    output_line = line.strip() + '|'
    for elem in name_set:
      output_line += elem.strip() + ',' 
    output_line = output_line.rstrip(',') + '|'        
    for elem in symbol_set:
      output_line += elem.strip() + ','
    output_line = output_line.rstrip(',')
    ## record as error
    if len(symbol_set) > 0 and symbol not in symbol_set:
      error_num += 1
      with open(outputfile_error,'a') as outf:
        print(output_line,file = outf)  
    if len(symbol_set) > 1 and symbol in symbol_set:
      right_num += 1
      with open(outputfile_right,'a') as outf:
        print(output_line,file = outf)
    if len(symbol_set) == 1 and symbol in symbol_set:
      perfect_num += 1
      with open(outputfile_perfect,'a') as outf:
        print(output_line,file = outf)
