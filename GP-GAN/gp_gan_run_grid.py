import glob
import os
from shutil import copyfile
import random

############CHANGE directory with images
###Directory with augmented images
src_dir = "/scratch/public/Image-Augmentation/results9/"

##############CHANGE
###DESTINATION IMAGES folder
dest_dir = "/scratch/public/MW_images/train_background_cropped/"

#output_dir
results_dir = "/scratch/public/experimental_output_ratio_MW/"

#Store dir- used to stash choices for destination images
store_dir = "/home/fcw/GP-GAN/store_info/"
store_fname = "MW_dsts.txt"

all_srcs = glob.glob(src_dir + "*.jpg")
all_masks = glob.glob(src_dir + "*.png")
all_txts = glob.glob(src_dir + "*.txt")
all_srcs.sort()
all_masks.sort()
all_txts.sort()

#print(all_srcs[i].replace(".jpg", "__mask2.png") == all_masks[i])
random.seed(42)


#############NEED TO CHANGE BASED ON DESTINATIONS

#Change to NW
all_MW_dsts = glob.glob(dest_dir + "*.jpg")
MW_dsts = random.sample(all_MW_dsts, 25)

with open(store_dir + store_fname, "w") as f:
    for file in MW_dsts:
        f.write(file + "\n")



#Change to SW
#all_ne_dsts = glob.glob(dest_dir + "SW/*.jpg")
#NE_dsts = random.sample(all_ne_dsts, 25)



def run_a_grid(curr_subdir, all_dsts, my_src, my_mask, my_txt, src_address):
    if not os.path.exists(curr_subdir):
        os.makedirs(curr_subdir)
        print(curr_subdir + " directory was made")
    for j in range(len(all_dsts)):
        my_dst = all_dsts[j]
        dst_address = my_dst[my_dst.rfind("/")+1:]
        #blended_out = "{subdir}{src_addr}_{dst_addr}".format(subdir=curr_subdir,src_addr=src_address,dst_addr=dst_address)
        blended_out = "{subdir}{dst_addr}".format(subdir=curr_subdir,src_addr=src_address,dst_addr=dst_address)
        blended_out = blended_out.replace(" ", "")
        copyfile(my_txt, blended_out.replace(".jpg",".txt"))
        cmd = "python run_gp_gan.py --src_image {src} --dst_image \"{dst}\" --mask_image {mask} --blended_image {out}".format(src=my_src,dst=my_dst,mask=my_mask,out=blended_out)
        print("Running command:")
        print(cmd)
        os.system(cmd)

for i in range(len(all_srcs)):
    my_src = all_srcs[i]
    my_mask = all_masks[i]
    my_txt = all_txts[i]
    src_address = my_src[my_src.rfind("/")+1:my_src.find(".jpg")]

    #No slash as results_dir has /
    mw_subdir = "{results_dir}{src_addr}/".format(results_dir=results_dir,src_addr=src_address)

    run_a_grid(mw_subdir, MW_dsts, my_src, my_mask, my_txt, src_address)

    #ne_subdir = "/hdd/dataplus2021/fcw/experimental_output_ratio_SW/{src_addr}/".format(src_addr=src_address)
    
    #run_a_grid(ne_subdir, NE_dsts, my_src, my_mask, my_txt, src_address)

