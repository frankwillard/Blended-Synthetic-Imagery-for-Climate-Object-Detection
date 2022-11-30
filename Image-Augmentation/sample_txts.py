import random
import glob
import os

my_txt_dir = "/hdd/dataplus2021/share/data/synthetic_labels"
all_txt_files = glob.glob(my_txt_dir + "/*.txt")

my_txt_files = random.sample(all_txt_files, 100)

with open("experiment2txts.txt", "w") as f:
  f.writelines("%s\n" % l for l in my_txt_files)
