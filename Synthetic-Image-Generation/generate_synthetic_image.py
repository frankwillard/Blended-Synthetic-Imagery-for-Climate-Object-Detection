from augment_image import augment_image
from blend_with_gp_gan import blend_with_gp_gan
import argparse

def generate_synthetic_image(objects_to_implant_img_fpaths, out_shape, objects_to_implant_lbl_fpaths, augmented_images_results_dir, out_fname, random_seed,
                             num_objects_to_sample_per_image, offset_ctr, gp_gan_blend_offset, dst_img, blended_img_out_path, generate_src_augmentations, verbose=False):
    if generate_src_augmentations:
        src_img_fpath, mask_img_fpath, turbines_used = augment_image(objects_to_implant_img_fpaths, out_shape, objects_to_implant_lbl_fpaths, augmented_images_results_dir, out_fname, random_seed,
                                                         num_objects_to_sample_per_image, offset_ctr, gp_gan_blend_offset)
    else:
        raise NotImplementedError("Currently only generating augmentations for the source domain is supported.")
    
    blend_with_gp_gan(src_img_fpath, dst_img, mask_img_fpath, blended_img_out_path, verbose)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Creates a synthetic image by placing random objects and blending them with background images blending images through the GP-GAN')

    # Augment image arguments
    parser.add_argument(
        "--objects-to-implant-img-fpaths",
        type=str,
        nargs="+",
        required=True,
        help="A list of paths to cropped turbine images."
    )
    parser.add_argument(
        "--out-shape",
        type=int,
        nargs="+",
        required=True,
        help="The desired shape (width, height) of the output image."
    )
    parser.add_argument(
        "--objects-to-implant-lbl-fpaths",
        type=str,
        nargs="+",
        required=True,
        help="A list of paths to files containing relative position and size information for the turbine images."
    )
    parser.add_argument(
        "--augmented-images-results-dir",
        type=str,
        required=True,
        help="The directory where the augmented images will be saved."
    )
    parser.add_argument(
        "--out-fname",
        type=str,
        required=True,
        help="The filename of the output image."
    )
    parser.add_argument(
        "--random-seed",
        type=int,
        default=42,
        help="The random seed for reproducibility."
    )
    parser.add_argument(
        "--num-objects-to-sample-per-image",
        type=int,
        required=True,
        help="The maximum number of turbine images to sample for augmentation."
    )
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
    parser.add_argument(
        "--generate-src-augmentations",
        action="store_true",
        help="Whether to generate the source augmentations."
    )
    parser.add_argument('--verbose', action='store_true', help='Print out progress of augmentation')

    # GP-GAN arguments
    parser.add_argument('--dst-img', type=str, required = True, help='File path for background image')
    parser.add_argument('--blended-img-out-path', type=str, required = True, help='File path to output blended synthetic image')

    args = parser.parse_args()

    # Augment image arguments
    objects_to_implant_img_fpaths = args.objects_to_implant_img_fpaths
    out_shape = tuple(args.out_shape)
    objects_to_implant_lbl_fpaths = args.objects_to_implant_lbl_fpaths
    augmented_images_results_dir = args.augmented_images_results_dir
    out_fname = args.out_fname
    random_seed = args.random_seed
    num_objects_to_sample_per_image = args.num_objects_to_sample_per_image
    offset_ctr = args.offset_ctr
    gp_gan_blend_offset = args.gp_gan_blend_offset
    generate_src_augmentations = args.generate_src_augmentations
    verbose = args.verbose

    # GP-GAN arguments
    # src_dir = args.src_dir
    dst_img = args.dst_img
    blended_img_out_path = args.blended_img_out_path
    
    generate_synthetic_image(objects_to_implant_img_fpaths, out_shape, objects_to_implant_lbl_fpaths, augmented_images_results_dir, out_fname, random_seed, num_objects_to_sample_per_image,
                             offset_ctr, gp_gan_blend_offset, dst_img, blended_img_out_path, generate_src_augmentations, verbose)