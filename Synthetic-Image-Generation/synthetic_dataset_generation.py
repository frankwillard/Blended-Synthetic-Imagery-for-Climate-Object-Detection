import glob
import json
import os
import random
import argparse
from generate_synthetic_image import generate_synthetic_image
from helpers import (
    multiple_replace,
    createPath,
    iterative_sample_without_replacement,
    move_synthetic_files_to_domain_pair_subdirectories,
)
from get_distribution import return_distribution
from augment_image import augment_image
from blend_with_gp_gan import blend_with_gp_gan


def generate_synthetic_dataset(
    implantable_objects_dir,
    out_shape,
    augmented_images_results_dir,
    random_seed,
    num_objects_to_sample_per_image_percentile,
    num_objects_to_sample_per_image_constant,
    offset_ctr,
    gp_gan_blend_offset,
    real_label_dir,
    final_results_dir,
    gp_gan_dir,
    g_path,
    domains,
    root,
    domain_dict_path,
    num_target_background_images,
    num_synthetic_images_per_domain,
    objects_augmenter_has_access_to,
    generate_unique_src_augmentations,
    generate_all_augmentations_first,
    experiment_name,
    verbose=False,
):
    """
    Generate a synthetic image dataset by placing random objects and blending them with background images using GP-GAN.

    Parameters:
    ----------
        implantable_objects_dir (str): Directory holding the image paths for the objects to be implanted.
        out_shape (tuple): The desired shape (width, height) of the output image.
        augmented_images_results_dir (str): The directory where the augmented images (canvas/masks) will be saved.
        random_seed (int): The random seed for reproducibility.
        num_objects_to_sample_per_image_percentile (int): Number of crops to augment into a new image (based on percentile of distribution for the given domain).
        num_objects_to_sample_per_image_constant (int): Number of crops to augment into a new image (constant).
        offset_ctr (int): The offset center used for random positioning of turbine images.
        gp_gan_blend_offset (int): The blend offset used for masking.
        real_label_dir (str): Directory holding real labels to get distribution from (subdirs are domains).
        final_results_dir (str): Directory for output_images (subdir of s-src-t-target per domain combination).
        gp_gan_dir (str): Directory including the GP-GAN code.
        g_path (str): Path to the pretrained blending GP-GAN model.
        domains (list): Domains in the dataset.
        root (str): Root of the directory containing the experiment images and labels.
        domain_dict_path (str): Path to domain dict controlling images accessible for the experiment.
        num_target_background_images (int): Number of target background images available to the synthetic image generator.
        num_synthetic_images_per_domain (int): Number of augmented images to produce.
        objects_augmenter_has_access_to (int): Number of implanted objects to be able to sample from (will be randomly sampled from the directory).
        generate_unique_src_augmentations (bool): Generate unique source augmentations for each target domain.
        generate_all_augmentations_first (bool): Generate augmentations first, then blend with background images.
        experiment_name (str): Name of the experiment.
        verbose (bool): Print out progress of augmentation.

    Returns:
    ----------
        metadata_dict (dict): A dictionary containing the metadata for the generated synthetic images.
    """
    
    domain_dict = json.load(open(domain_dict_path, 'r'))

    replacer = {"images": "labels", ".jpg": ".txt", ".png": ".txt"}

    file_types = ("*.jpg", "*.png")

    metadata_dict = {}

    if num_objects_to_sample_per_image_constant is not None:
        num_objects_to_sample_per_image = num_objects_to_sample_per_image_constant

    total_imgs_count = 1

    if generate_all_augmentations_first:
        list_path_subdir = f"{os.getcwd()}/{experiment_name}/"
        os.makedirs(list_path_subdir, exist_ok=True)
        list_path_csv_fname = os.path.join(list_path_subdir, "list_path.csv")
        list_path_csv = open(list_path_csv_fname, "w")

    for src_domain in domains:
        src_img_dir = f"{implantable_objects_dir}/images/{src_domain}/"

        # Cropped images
        objects_to_implant_img_fpaths = []
        implantable_objects_file_paths = []
        for file_type in file_types:
            implantable_objects_file_paths.extend(glob.glob(src_img_dir + file_type))

        assert (
            len(implantable_objects_file_paths) >= objects_augmenter_has_access_to
        ), "Not enough objects to augment with as designated in variable objects_augmenter_has_access_to."

        random.seed(random_seed)
        objects_to_implant_img_fpaths = random.sample(
            implantable_objects_file_paths, objects_augmenter_has_access_to
        )

        # Labels in exact same order as images
        objects_to_implant_lbl_fpaths = [
            multiple_replace(replacer, src_img)
            for src_img in objects_to_implant_img_fpaths
        ]

        # Determine number of objects to sample per image
        if num_objects_to_sample_per_image_percentile is not None:
            # If use for real, would need to only use first 100 from domain file
            sorted_turbine_heights = sorted(
                return_distribution(real_label_dir, src_domain, out_shape)[2]
            )

            num_objects_to_sample_per_image = sorted_turbine_heights[
                int(num_objects_to_sample_per_image_percentile / 100)
                * len(sorted_turbine_heights)
            ]

        for j, target_domain in enumerate(domains):
            print(src_domain, target_domain)

            dict_name = f"s_{src_domain}_t_{target_domain}"
            current_subdir = f"{final_results_dir}/{dict_name}/"
            createPath(current_subdir)
            
            # Fetch target background filepaths.
            background_image_keys = domain_dict[target_domain]['Background'][:num_target_background_images]
            all_dsts = [os.path.join(root, 'images', target_domain, 'Background', f'{_}.jpg') for _ in background_image_keys]

            # Randomly sample n target backgrounds.
            random.seed(random_seed)
            dst_imgs = iterative_sample_without_replacement(
                all_dsts, num_synthetic_images_per_domain
            )

            metadata_dict[dict_name] = []

            for i in range(num_synthetic_images_per_domain):
                out_fname = f"src_{src_domain}_dst_{target_domain}_mask{i}"
                if verbose:
                    print(out_fname)

                # Determine whether to generate augmentations for src_domain
                generate_src_augmentations = j == 0 or generate_unique_src_augmentations

                dst_img = dst_imgs[i]

                dst_address = os.path.splitext(os.path.basename(dst_img))[0]
                blended_img_out_path = f"{current_subdir}{dst_address}.jpg"

                # Want to ensure that each image is unique
                random_seed_added = random_seed + total_imgs_count

                if not generate_all_augmentations_first:
                    generate_synthetic_image(
                        objects_to_implant_img_fpaths,
                        out_shape,
                        objects_to_implant_lbl_fpaths,
                        augmented_images_results_dir,
                        out_fname,
                        random_seed_added,
                        num_objects_to_sample_per_image,
                        offset_ctr,
                        gp_gan_blend_offset,
                        gp_gan_dir,
                        g_path,
                        dst_img,
                        blended_img_out_path,
                        generate_src_augmentations,
                        verbose,
                    )
                else:
                    src_img_fpath, mask_img_fpath, turbines_used = augment_image(
                        objects_to_implant_img_fpaths,
                        out_shape,
                        objects_to_implant_lbl_fpaths,
                        augmented_images_results_dir,
                        out_fname,
                        random_seed_added,
                        num_objects_to_sample_per_image,
                        offset_ctr,
                        gp_gan_blend_offset,
                    )
                    list_path_csv.write(f"{src_img_fpath};{dst_img};{mask_img_fpath}\n")

                total_imgs_count = total_imgs_count + 1

    list_path_csv.close()

    if generate_all_augmentations_first:
        blend_with_gp_gan(
            gp_gan_dir,
            g_path,
            src_img=None,
            dst_img=None,
            mask_img=None,
            blended_img_out_path=None,
            results_folder=final_results_dir,
            list_path=list_path_csv_fname,
            verbose=verbose,
        )
        move_synthetic_files_to_domain_pair_subdirectories(
            final_results_dir, verbose=verbose
        )

    return metadata_dict


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Creates a synthetic image dataset by placing random objects and blending them with background images blending images through the GP-GAN"
    )
    parser.add_argument(
        "--implantable-objects-dir",
        type=str,
        help="A directory holding the image paths for the objects to be implanted.",
    )
    parser.add_argument(
        "--out-shape",
        type=int,
        nargs="+",
        default=[608, 608],
        help="The desired shape (width, height) of the output image.",
    )
    parser.add_argument(
        "--augmented-images-results-dir",
        type=str,
        help="The directory where the augmented images (canvas/masks) will be saved.",
    )
    parser.add_argument(
        "--random-seed",
        type=int,
        default=42,
        help="The random seed for reproducibility.",
    )
    parser.add_argument(
        "--num-objects-to-sample-per-image-percentile",
        type=int,
        default=None,
        help="Number of crops to augment into new image (based on percentile of distribution for given domain)",
    )
    parser.add_argument(
        "--num-objects-to-sample-per-image-constant",
        type=int,
        default=None,
        help="Number of crops to augment into new image (constant)",
    )
    parser.add_argument(
        "--offset-ctr",
        type=int,
        default=20,
        help="The offset center used for random positioning of turbine images.",
    )
    parser.add_argument(
        "--gp-gan-blend-offset",
        type=int,
        default=20,
        help="The blend offset used for masking.",
    )
    parser.add_argument(
        "--real-label-dir",
        type=str,
        default=None,
        required=False,
        help="Directory (no final slash) holding real labels to get distribution from (subdirs are domains)",
    )

    # GP-GAN arguments
    parser.add_argument(
        "--final-results-dir",
        type=str,
        required=True,
        help="Directory (do not include the final slash) for output_images (subdir of s-src-t-target per domain combination)",
    )
    parser.add_argument(
        "--gp-gan-dir",
        type=str,
        required=True,
        help="Directory including the GP-GAN code",
    )
    parser.add_argument("--g-path", help="Path for pretrained Blending GAN model")

    # Dataset arguments
    parser.add_argument("--domains", type=str, nargs="+", help="Domains in dataset")
    parser.add_argument(
        "--num-synthetic-images-per-domain",
        type=int,
        required=True,
        help="Number of augmented images to produce",
    )
    
    parser.add_argument(
        "--root",
        type=str,
        required=True,
        help="Root of the directory containing the experiment images and labels.",
    )
    
    parser.add_argument(
        "--domain-dict-path",
        type=str,
        required=True,
        help="Path to domain dictionary containing images for experiments.",
    )
    
    parser.add_argument(
        "--num-target-background-images",
        type=int,
        required=True,
        help="Number of target background images available to the synthetic image generator",
    )
    
    parser.add_argument(
        "--objects-augmenter-has-access-to",
        type=int,
        required=True,
        help="Number of implanted objects to be able to sample from (will be randomly sampled from directory)",
    )
    parser.add_argument(
        "--generate-unique-src-augmentations",
        action="store_true",
        help="Generate unique source augmentations for each target domain",
    )
    parser.add_argument(
        "--generate-all-augmentations-first",
        action="store_true",
        help="Generate all augmentations first, then blend with background images",
    )
    parser.add_argument(
        "--experiment-name",
        type=str,
        required=True,
        help="Name of experiment (used for saving results)",
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Print out progress of augmentation"
    )

    args = parser.parse_args()

    assert not (
        args.num_objects_to_sample_per_image_percentile
        and args.num_objects_to_sample_per_image_constant
    ), "Cannot use both percentile and constant for number of crops to augment into new image"
    assert args.num_objects_to_sample_per_image_constant or (
        args.num_objects_to_sample_per_image_percentile and args.real_label_dir
    ), "Must use either percentile or constant for number of crops to augment into new image. Must use real label dir to get distribution from if using percentile for number of crops to augment into new image"

    # Augment image arguments
    implantable_objects_dir = args.implantable_objects_dir
    out_shape = tuple(args.out_shape)
    augmented_images_results_dir = args.augmented_images_results_dir
    random_seed = args.random_seed
    num_objects_to_sample_per_image_percentile = (
        args.num_objects_to_sample_per_image_percentile
    )
    num_objects_to_sample_per_image_constant = (
        args.num_objects_to_sample_per_image_constant
    )
    offset_ctr = args.offset_ctr
    gp_gan_blend_offset = args.gp_gan_blend_offset
    real_label_dir = args.real_label_dir

    # GP-GAN arguments
    final_results_dir = args.final_results_dir
    gp_gan_dir = args.gp_gan_dir
    g_path = args.g_path

    # Dataset arguments
    domains = args.domains
    root = args.root
    domain_dict_path = args.domain_dict_path
    num_target_background_images = args.num_target_background_images
    num_synthetic_images_per_domain = args.num_synthetic_images_per_domain
    objects_augmenter_has_access_to = args.objects_augmenter_has_access_to
    generate_unique_src_augmentations = args.generate_unique_src_augmentations
    generate_all_augmentations_first = args.generate_all_augmentations_first
    experiment_name = args.experiment_name
    verbose = args.verbose

    generate_synthetic_dataset(
        implantable_objects_dir,
        out_shape,
        augmented_images_results_dir,
        random_seed,
        num_objects_to_sample_per_image_percentile,
        num_objects_to_sample_per_image_constant,
        offset_ctr,
        gp_gan_blend_offset,
        real_label_dir,
        final_results_dir,
        gp_gan_dir,
        g_path,
        domains,
        root,
        domain_dict_path,
        num_target_background_images,
        num_synthetic_images_per_domain,
        objects_augmenter_has_access_to,
        generate_unique_src_augmentations,
        generate_all_augmentations_first,
        experiment_name,
        verbose,
    )
