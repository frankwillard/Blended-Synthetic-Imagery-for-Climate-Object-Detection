from PIL import Image
import numpy as np
import os
import random
import glob
from augment_images import image_augmenter
from shutil import copyfile
import re
from get_distribution import return_distribution
from pathlib import Path
import json
import argparse

def multiple_replace(dict, text):
  # Create a regular expression  from the dictionary keys
  regex = re.compile("(%s)" % "|".join(map(re.escape, dict.keys())))

  # For each match, look-up corresponding value in dictionary
  return regex.sub(lambda mo: dict[mo.string[mo.start():mo.end()]], text) 

def csv_augment(my_out_shape, domains, cropped, output_dir, num_outputs, metadata_json):

  replacer = {
    "images":"labels",
    ".jpg":".txt",
    ".png":".txt"
  }

  output_dict = {}

  for domain in domains:

    src_img_dir = f"{cropped}/images/{domain}/"

    types = ("*.jpg", "*.png")
    #Cropped images
    cropped_imgs = []
    for file_type in types:
      cropped_imgs.extend(glob.glob(src_img_dir + file_type))
    
    #Relative labels
    cropped_labels = [multiple_replace(replacer, src_img) for src_img in cropped_imgs]

    #If use for real, would need to only use first 100 from domain file 
    num_imgs, width_turbines, height_turbines = return_distribution(domain)

    my_res_folder = f"{output_dir}/{domain}/"

    output_dict[domain] = {}

    #Change to src_files
    for i in range(0,num_outputs):

      random.seed(42)

      #windmill_file = src_imgs[i]
      #src_name = Path(windmill_file).stem

      my_out_fname  = f"src_{domain}_mask{i}"
      print(my_out_fname)

      #Can pass in all sources and all relatives
      turbines = image_augmenter(cropped_imgs, domain, my_out_shape,cropped_labels, my_res_folder,my_out_fname, i)

      output_dict[domain][my_out_fname] = turbines

  if metadata_json is not None:
    with open(metadata_json, "w") as f:
      json.dump(output_dict, f)


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Adds cropped images onto white canvas and creates GP-GAN masks and YOLO labels')
  parser.add_argument('--out-h', type=int, default=608, help='Height in output image shape')
  parser.add_argument('--out-w', type=int, default=608, help='Width in output image shape')
  parser.add_argument('--domains', action = 'append', default = [], required = True, help='Height in output image shape')
  parser.add_argument('--num-outputs', type=int, required = True, help='Number of augmented images to produce')
  parser.add_argument('--cropped-dir', type=str, required = True, help='Directory (do not include the final slash) for cropped images/labels - Has a subdir of images and a subdir of labels (whose subdirs are the domain names)')
  parser.add_argument('--out-dir', type=str, required = True, help='Directory (do not include the final slash) for output augmentations (subdirs by domain)')
  parser.add_argument('--metadata-json', type=str, default = None, help='File name of JSON to output metadata on matchings to')
  args = parser.parse_args()

#cropped = "/scratch/public/new_cropped_turbines/"
#domains = ["EM", "NW", "SW"]
#augmented_out_folder = "/scratch/public/augmented_images/"
#my_out_shape = (608,608)

#Check if (height, width) or (width, height)
out_shape = (args.out_h, args.out_w)
domains = args.domains
cropped_dir = args.cropped_dir
output_dir = args.out_dir
num_outputs = args.num_outputs
metadata_json = args.metadata_json

csv_augment(my_out_shape = out_shape, domains = domains, cropped = cropped_dir, output_dir = output_dir, num_outputs = num_outputs, metadata_json = metadata_json)
