import glob
import os
from shutil import copyfile
import random
import json
import argparse
from generate_synthetic_image import generate_synthetic_image
from helpers import multiple_replace, createPath, iterative_sample_without_replacement
from get_distribution import return_distribution

def generate_synthetic_dataset(implantable_objects_dir, out_shape, augmented_images_results_dir, random_seed, num_objects_to_sample_per_image_percentile, num_objects_to_sample_per_image_constant,
                               offset_ctr, gp_gan_blend_offset, real_label_dir, background_images_dir, final_results_dir, domains, num_synthetic_images_per_domain, generate_unique_src_augmentations,
                               verbose=False):
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
    
    metadata_dict = {}

    if num_objects_to_sample_per_image_constant is not None:
      num_objects_to_sample_per_image = num_objects_to_sample_per_image_constant
    
    for src_domain in domains:
        
        src_img_dir = f"{implantable_objects_dir}/images/{src_domain}/"

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
            
            print(src_domain, target_domain)

            dict_name = f"s_{src_domain}_t_{target_domain}"
            current_subdir = f"{final_results_dir}/{dict_name}/"
            createPath(current_subdir)

            dest_dir = f"{background_images_dir}/{target_domain}/Background/"
            all_dsts = glob.glob(dest_dir + "*.jpg")

            # Randomly sample n images from all_dsts
            dst_imgs = iterative_sample_without_replacement(all_dsts, num_synthetic_images_per_domain)

            metadata_dict[dict_name] = []

            for i in range(num_synthetic_images_per_domain):
                out_fname  = f"src_{src_domain}_mask{i}"
                if verbose:
                    print(out_fname)

                # Determine whether to generate augmentations for src_domain
                generate_src_augmentations = j == 0 or generate_unique_src_augmentations

                dst_img = dst_imgs[i]

                dst_address = os.path.splitext(os.path.basename(dst_img))[0]
                blended_img_out_path = f"{current_subdir}{dst_address}.jpg"

                generate_synthetic_image(objects_to_implant_img_fpaths, out_shape, objects_to_implant_lbl_fpaths, augmented_images_results_dir, out_fname, random_seed, num_objects_to_sample_per_image,
                                         offset_ctr, gp_gan_blend_offset, dst_img, blended_img_out_path, generate_src_augmentations, verbose)
    
    return metadata_dict

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Creates a synthetic image dataset by placing random objects and blending them with background images blending images through the GP-GAN')
    parser.add_argument(
        "--implantable-objects-dir",
        type=str,
        help="A directory holding the image paths for the objects to be implanted."
    )
    parser.add_argument(
        "--out-shape",
        type=int,
        nargs="+",
        default=[608, 608],
        help="The desired shape (width, height) of the output image."
    )
    parser.add_argument(
        "--augmented-images-results-dir",
        type=str,
        help="The directory where the augmented images (canvas/masks) will be saved."
    )
    parser.add_argument(
        "--random-seed",
        type=int,
        default=42,
        help="The random seed for reproducibility."
    )
    parser.add_argument('--num-objects-to-sample-per-image-percentile', type=int, default=None, help='Number of crops to augment into new image (based on percentile of distribution for given domain)')
    parser.add_argument('--num-objects-to-sample-per-image-constant', type=int, default=None, help='Number of crops to augment into new image (constant)')
    parser.add_argument(
        "--offset-ctr",
        type=int,
        default=20,
        help="The offset center used for random positioning of turbine images."
    )
    parser.add_argument(
        "--gp-gan-blend-offset",
        type=int,
        default=20,
        help="The blend offset used for masking."
    )
    parser.add_argument('--real-label-dir', type=str, default=None, required=False, help='Directory (no final slash) holding real labels to get distribution from (subdirs are domains)')

    # GP-GAN arguments
    parser.add_argument('--background-images-dir', type=str, required=True, help='Directory (do not include the final slash) for backgrounds (subdir of domain, subdir of Background)')
    parser.add_argument('--final-results-dir', type=str, required=True, help='Directory (do not include the final slash) for output_images (subdir of s-src-t-target per domain combination)')

    # Dataset arguments
    parser.add_argument('--domains',
                        type=str,
                        nargs="+",
                        help='Domains in dataset'
    )
    parser.add_argument('--num-synthetic-images-per-domain', type=int, required=True, help='Number of augmented images to produce')
    parser.add_argument('--generate-unique-src-augmentations', action='store_true', help='Generate unique source augmentations for each target domain')
    parser.add_argument('--verbose', action='store_true', help='Print out progress of augmentation')

    args = parser.parse_args()

    assert not (args.num_objects_to_sample_per_image_percentile and args.num_objects_to_sample_per_image_constant), "Cannot use both percentile and constant for number of crops to augment into new image"
    assert args.num_objects_to_sample_per_image_constant or (args.num_objects_to_sample_per_image_percentile and args.real_label_dir), "Must use either percentile or constant for number of crops to augment into new image. Must use real label dir to get distribution from if using percentile for number of crops to augment into new image"

    # Augment image arguments
    implantable_objects_dir = args.implantable_objects_dir
    out_shape = tuple(args.out_shape)
    augmented_images_results_dir = args.augmented_images_results_dir
    random_seed = args.random_seed
    num_objects_to_sample_per_image_percentile = args.num_objects_to_sample_per_image_percentile
    num_objects_to_sample_per_image_constant = args.num_objects_to_sample_per_image_constant
    offset_ctr = args.offset_ctr
    gp_gan_blend_offset = args.gp_gan_blend_offset
    real_label_dir = args.real_label_dir

    # GP-GAN arguments
    background_images_dir = args.background_images_dir
    final_results_dir = args.final_results_dir

    # Dataset arguments
    domains = args.domains
    num_synthetic_images_per_domain = args.num_synthetic_images_per_domain
    generate_unique_src_augmentations = args.generate_unique_src_augmentations
    verbose = args.verbose

    generate_synthetic_dataset(implantable_objects_dir, out_shape, augmented_images_results_dir, random_seed, num_objects_to_sample_per_image_percentile, num_objects_to_sample_per_image_constant,
                               offset_ctr, gp_gan_blend_offset, real_label_dir, background_images_dir, final_results_dir, domains, num_synthetic_images_per_domain, generate_unique_src_augmentations,
                               verbose)