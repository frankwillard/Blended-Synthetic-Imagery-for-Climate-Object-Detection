
import glob
import os
from shutil import copyfile
import random
import itertools
import json
from gp_gan_one_to_one import run_one_to_one

src_dir = "/scratch/public/augmented_images/"
dst_dir = "/scratch/public/jitter/wt/images/"
#REPLACE/Background/
results_dir = "/scratch/public/jitter/wt/images/Synthetic/"

domains = ["EM", "NW", "SW"]

n = 182

run_one_to_one(src_dir, dst_dir, results_dir, domains, n)