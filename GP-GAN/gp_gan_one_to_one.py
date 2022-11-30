import glob
import os
from shutil import copyfile
import random
import itertools
import json

def createPath(curr_subdir):
    """[summary]

    Args:
        curr_subdir ([type]): [description]
    """
    if not os.path.exists(curr_subdir):
        os.makedirs(curr_subdir)
        print(curr_subdir + " directory was made")

def run_one_to_one(gen_aug_dir, gen_dst_dir, results_dir, domains, n):
    """[summary]

    Args:
        src_dir ([type]): [description]
        dst_dir ([type]): [description]
        store_dir ([type]): [description]
        results_dir ([type]): [description]
        domains ([type]): [description]
        n ([type]): [description]
    """
    
    random.seed(42)

    domain_combos = list(itertools.product(domains, repeat=2))

    my_dict = {}

    for (src_domain, target_domain) in domain_combos:

        src_dir = f"{gen_aug_dir}{src_domain}/canvases/"
        mask_dir = f"{gen_aug_dir}{src_domain}/masks/"
        lbl_dir = f"{gen_aug_dir}{src_domain}/labels/"

        all_srcs = glob.glob(src_dir + "*.jpg")
        all_masks = glob.glob(mask_dir + "*.png")
        all_txts = glob.glob(lbl_dir + "*.txt")
        all_srcs.sort()
        all_masks.sort()
        all_txts.sort()

        #dst_dir = "/scratch/public/jitter/wt/images/"
        #REPLACE/Background/
        
        #dest_dir = f"{gen_dst_dir}{target_domain}/"

        dest_dir = f"{gen_dst_dir}{target_domain}/Background/"

                
        #Have background destination directories
        all_dsts = glob.glob(dest_dir + "*.jpg")

        dst_imgs = random.sample(all_dsts, n)

        #Could shuffle if desired

        #store_fname = ""

        #with open(store_dir + store_fname, "w") as f:
        #    for file in MW_dsts:
        #        f.write(file + "\n")

        dict_name = f"s_{src_domain}_t_{target_domain}"

        current_subdir = f"{results_dir}{dict_name}/"
        createPath(current_subdir)

        #Augmented: {s_src_t_target: [(augment, background)]
        #           }
        
        my_dict[dict_name] = []


        for i in range(n):
            my_src = all_srcs[i]
            my_mask = all_masks[i]
            my_txt = all_txts[i]

            src_address = my_src[my_src.rfind("/")+1:my_src.find(".jpg")]

            my_dst = dst_imgs[i]
            dst_address = my_dst[my_dst.rfind("/")+1:my_dst.find(".jpg")]

            my_dict[dict_name].append((src_address, dst_address))

            blended_out = f"{current_subdir}{dst_address}.jpg"
            #Removes space for GP GAN
            blended_out = blended_out.replace(" ", "")

            #Copies txt file of mask to synthetic output
            
            copyfile(my_txt, blended_out.replace(".jpg",".txt"))
            cmd = f"python run_gp_gan.py --src_image {my_src} --dst_image \"{my_dst}\" --mask_image {my_mask} --blended_image {my_mask} --gpu 1"
            print("Running command:")
            print(cmd)
            #os.system(cmd)
    
    return my_dict
