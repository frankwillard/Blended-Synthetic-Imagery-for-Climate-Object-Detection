from augment_image import augment_image
from blend_with_gp_gan import blend_with_gp_gan
import argparse

def generate_synthetic_image(objects_to_implant_img_fpaths, out_shape, objects_to_implant_lbl_fpaths, results_dir, out_fname, random_seed, num_to_sample, offset_ctr, gp_gan_blend_offset, src_dir, dst_dir, final_results_dir, generate_src_augmentations, verbose=False):
    if generate_src_augmentations:
        augment_image(objects_to_implant_img_fpaths, out_shape, objects_to_implant_lbl_fpaths, results_dir, out_fname, random_seed, num_to_sample, offset_ctr, gp_gan_blend_offset)
    
    src_dir = results_dir
    blend_with_gp_gan(src_dir, dst_dir, final_results_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Creates a synthetic image by placing random objects and blending them with background images blending images through the GP-GAN')

    # Augment image arguments
    parser.add_argument(
        "objects_to_implant_img_fpaths",
        type=str,
        nargs="+",
        required=True,
        help="A list of paths to cropped turbine images."
    )
    parser.add_argument(
        "out_shape",
        type=int,
        nargs="+",
        required=True,
        help="The desired shape (width, height) of the output image."
    )
    parser.add_argument(
        "objects_to_implant_lbl_fpaths",
        type=str,
        nargs="+",
        required=True,
        help="A list of paths to files containing relative position and size information for the turbine images."
    )
    parser.add_argument(
        "results_dir",
        type=str,
        required=True,
        help="The directory where the augmented images will be saved."
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
    parser.add_argument(
        "num_to_sample",
        type=int,
        required=True,
        help="The maximum number of turbine images to sample for augmentation."
    )
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
    parser.add_argument(
        "generate_src_augmentations",
        type=int,
        default=20,
        help="The blend offset used for masking."
    )
    parser.add_argument('--verbose', action='store_true', help='Print out progress of augmentation')


    # GP-GAN arguments
    # parser.add_argument('--src-dir', type=str, required = True, help='Directory (do not include the final slash) for augmented canvases/masks/labels')
    parser.add_argument('--dst-dir', type=str, required = True, help='Directory (do not include the final slash) for backgrounds (subdir of domain, subdir of Background)')
    parser.add_argument('--final_results_dir', type=str, required = True, help='Directory (do not include the final slash) for output_images (subdir of s_src_t_target per domain combination)')

    args = parser.parse_args()

    # Augment image arguments
    objects_to_implant_img_fpaths = args.objects_to_implant_img_fpaths
    out_shape = tuple(args.out_shape)
    objects_to_implant_lbl_fpaths = args.objects_to_implant_lbl_fpaths
    results_dir = args.results_dir
    out_fname = args.out_fname
    random_seed = args.random_seed
    num_to_sample = args.num_to_sample
    offset_ctr = args.offset_ctr
    gp_gan_blend_offset = args.gp_gan_blend_offset
    generate_src_augmentations = args.generate_src_augmentations
    verbose = args.verbose

    # GP-GAN arguments
    # src_dir = args.src_dir
    dst_dir = args.dst_dir
    final_results_dir = args.final_results_dir
    
    generate_synthetic_image(objects_to_implant_img_fpaths, out_shape, objects_to_implant_lbl_fpaths, results_dir, out_fname, random_seed, num_to_sample, offset_ctr, gp_gan_blend_offset, src_dir, dst_dir, final_results_dir)