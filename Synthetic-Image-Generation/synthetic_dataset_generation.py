import glob
import os
from shutil import copyfile
import random
import json
import argparse
from generate_synthetic_image import generate_synthetic_image
from helpers import multiple_replace, createPath
from get_distribution import return_distribution

def generate_synthetic_dataset(cropped_dir, num_objects_to_sample_per_image_percentile, num_objects_to_sample_per_image_constant, real_label_dir, verbose=False):
    """[summary]

    Args:
        src_dir ([type]): [description]
        dst_dir ([type]): [description]
        store_dir ([type]): [description]
        results_dir ([type]): [description]
        domains ([type]): [description]
        n ([type]): [description]
    """

    replacer = {
        "images":"labels",
        ".jpg":".txt",
        ".png":".txt"
    }

    file_types = ("*.jpg", "*.png")
    
    random.seed(42)

    metadata_dict = {}

    if num_objects_to_sample_per_image_constant is not None:
      num_objects_to_sample_per_image = num_objects_to_sample_per_image_constant

    for src_domain in domains:
        
        src_img_dir = f"{cropped_dir}/images/{src_domain}/"

        # Cropped images
        objects_to_implant_img_fpaths = []
        for file_type in file_types:
            objects_to_implant_img_fpaths.extend(glob.glob(src_img_dir + file_type))

        # Labels in exact same order as images
        objects_to_implant_lbl_fpaths = [multiple_replace(replacer, src_img) for src_img in objects_to_implant_img_fpaths]
        
        # Determine number of objects to sample per image
        if num_objects_to_sample_per_image_percentile is not None:
            #If use for real, would need to only use first 100 from domain file 
            sorted_turbine_heights = sorted(return_distribution(real_label_dir, src_domain, out_shape)[2])

            num_objects_to_sample_per_image = sorted_turbine_heights[int(num_objects_to_sample_per_image_percentile / 100) * len(sorted_turbine_heights)]


        for j, target_domain in enumerate(domains):
            dict_name = f"s_{src_domain}_t_{target_domain}"
            current_subdir = f"{final_results_dir}/{dict_name}/"
            createPath(current_subdir)

            metadata_dict[dict_name] = []

            for i in range(num_synthetic_images_per_domain):

                my_out_fname  = f"src_{src_domain}_mask{i}"
                if verbose:
                    print(my_out_fname)


                # Determine whether to generate augmentations for src_domain
                generate_src_augmentations = j == 0

                # cropped_turbines, out_shape, relative, results_dir, out_fname, random_seed, num_to_sample, offset_ctr, gp_gan_blend_offset, src_dir, dst_dir, final_results_dir
                generate_synthetic_image(objects_to_implant_img_fpaths, out_shape, objects_to_implant_lbl_fpaths, augmented_images_results_dir, out_fname, random_seed, num_objects_to_sample_per_image,
                                         offset_ctr, gp_gan_blend_offset, dst_dir, final_results_dir, generate_src_augmentations, verbose)
    
    return metadata_dict

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Creates a synthetic image dataset by placing random objects and blending them with background images blending images through the GP-GAN')
    parser.add_argument(
        "cropped_turbines",
        type=str,
        nargs="+",
        required=True,
        help="A list of paths to cropped turbine images."
    )
    parser.add_argument(
        "out_shape",
        type=int,
        nargs="+",
        default=[608, 608],
        help="The desired shape (width, height) of the output image."
    )
    parser.add_argument(
        "relative",
        type=str,
        nargs="+",
        required=True,
        help="A list of paths to files containing relative position and size information for the turbine images."
    )
    parser.add_argument(
        "augmented_images_results_dir",
        type=str,
        required=True,
        help="The directory where the augmented images (canvas/masks) will be saved."
    )
    parser.add_argument(
        "out_fname",
        type=str,
        required=True,
        help="The filename of the output image."
    )
    parser.add_argument(
        "random_seed",
        type=int,
        default=42,
        help="The random seed for reproducibility."
    )
    parser.add_argument('--num-to-sample-percentile', type=int, default = None, help='Number of crops to augment into new image (based on percentile of distribution for given domain)')
    parser.add_argument('--num-to-sample-constant', type=int, default = None, help='Number of crops to augment into new image (constant)')
    parser.add_argument(
        "offset_ctr",
        type=int,
        default=20,
        help="The offset center used for random positioning of turbine images."
    )
    parser.add_argument(
        "gp_gan_blend_offset",
        type=int,
        default=20,
        help="The blend offset used for masking."
    )
    parser.add_argument('--real-label-dir', type=str, default = None, required = False, help='Directory (no final slash) holding real labels to get distribution from (subdirs are domains)')
    
    
    # GP-GAN arguments
    parser.add_argument('--dst-dir', type=str, required = True, help='Directory (do not include the final slash) for backgrounds (subdir of domain, subdir of Background)')
    parser.add_argument('--final_results_dir', type=str, required = True, help='Directory (do not include the final slash) for output_images (subdir of s_src_t_target per domain combination)')

    # Dataset arguments
    parser.add_argument('--domains',
                        type=str,
                        nargs="+",
                        required=True,
                        help='Domains in dataset'
    )
    parser.add_argument('--num-synthetic-images-per-domain', type=int, required = True, help='Number of augmented images to produce')
    parser.add_argument('--verbose', action='store_true', help='Print out progress of augmentation')

    args = parser.parse_args()

    assert args.num_objects_to_sample_per_image_percentile or args.num_objects_to_sample_per_image_constant, "Must use either percentile or constant for number of crops to augment into new image"
    assert not (args.num_objects_to_sample_per_image_percentile and args.num_objects_to_sample_per_image_constant), "Cannot use both percentile and constant for number of crops to augment into new image"

    # Augment image arguments
    cropped_turbines = args.cropped_turbines
    out_shape = tuple(args.out_shape)
    relative = args.relative
    augmented_images_results_dir = args.augmented_images_results_dir
    out_fname = args.out_fname
    random_seed = args.random_seed
    num_objects_to_sample_per_image_percentile = args.num_objects_to_sample_per_image_percentile
    num_objects_to_sample_per_image_constant = args.num_objects_to_sample_per_image_constant
    offset_ctr = args.offset_ctr
    gp_gan_blend_offset = args.gp_gan_blend_offset
    real_label_dir = args.real_label_dir

    # GP-GAN arguments
    src_dir = args.src_dir
    dst_dir = args.dst_dir
    final_results_dir = args.final_results_dir

    # Dataset arguments
    domains = args.domains
    num_synthetic_images_per_domain = args.num_synthetic_images_per_domain

    generate_synthetic_dataset(src_dir, dst_dir, augmented_images_results_dir, domains, out_shape, out_fname, random_seed, num_objects_to_sample_per_image_percentile, num_objects_to_sample_per_image_constant,
                               offset_ctr, gp_gan_blend_offset, final_results_dir)