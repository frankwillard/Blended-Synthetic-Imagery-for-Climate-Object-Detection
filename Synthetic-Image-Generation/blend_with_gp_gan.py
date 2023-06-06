import subprocess
import argparse

def blend_with_gp_gan(src_img, dst_img, mask_img, verbose=False):
    """

    """
    #Copies txt file of mask to synthetic output
    cmd = f"python run_gp_gan.py --src_image {src_img} --dst_image \"{dst_img}\" --mask_image {mask_img} --blended_image {mask_img}"
    if verbose:
        print("Running command:")
        print(cmd)

    subprocess.run(cmd, shell=True)

    return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Creates a synthetic image by placing random objects and blending them with background images blending images through the GP-GAN')

    # GP-GAN arguments
    parser.add_argument('--src-dir', type=str, required = True, help='Directory (do not include the final slash) for augmented canvases/masks/labels')
    parser.add_argument('--dst-dir', type=str, required = True, help='Directory (do not include the final slash) for backgrounds (subdir of domain, subdir of Background)')
    parser.add_argument('--mask_img', type=str, required = True, help='Directory (do not include the final slash) for output_images (subdir of s_src_t_target per domain combination)')
    parser.add_argument('--verbose', action='store_true', help='Print out progress of blending')
    args = parser.parse_args()

    # GP-GAN arguments
    src_dir = args.src_dir
    dst_dir = args.dst_dir
    mask_img = args.mask_img
    verbose = args.verbose

    blend_with_gp_gan(src_dir, dst_dir, mask_img, verbose)