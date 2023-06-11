import subprocess
import argparse
import os

def blend_with_gp_gan(gp_gan_dir, src_img, dst_img, mask_img, blended_img_out_path = None, results_folder = None, list_path = None, verbose=False):
    """
    Blend the source image with the destination image using the mask image
    and save the blended image to the specified output path using GP-GAN.

    Parameters:
    ----------
        src_img (str): Path to the source image file.
        dst_img (str): Path to the destination image file.
        mask_img (str): Path to the mask image file.
        blended_img_out_path (str): Output path to save the blended image.
        verbose (bool, optional): If True, print the command being executed. 
                                  Defaults to False.

    Returns:
    -------
        None

    Raises:
    -------
        subprocess.CalledProcessError: If the command execution fails.

    Note:
    -----
        This function requires the 'run_gp_gan.py' script to be available.

    Example:
    -------
        blend_with_gp_gan('source.jpg', 'destination.jpg', 'mask.png', 'blended.jpg', verbose=True)
    """

    assert list_path or (src_img and dst_img and mask_img), "Either list_path or src_img, dst_img, and mask_img must be specified"

    #Copies txt file of mask to synthetic output
    cmd = f"python3 {gp_gan_dir}/run_gp_gan.py"

    if list_path is not None:
        cmd += f" --list_path {list_path}"
    else:
        cmd += f" --src_image {src_img} --dst_image \"{dst_img}\" --mask_image {mask_img}"
    
    if blended_img_out_path is not None:
        cmd += f" --blended_image {blended_img_out_path}"
    elif results_folder is not None:
        cmd += f" --results_folder {results_folder}"

    if verbose:
        print("Running command:")
        print(cmd)

    subprocess.run(cmd, shell=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Creates a synthetic image by placing random objects and blending them with background images blending images through the GP-GAN')

    # GP-GAN arguments
    parser.add_argument('--gp-gan-dir', type=str, required=True, help='Directory including the GP-GAN code')
    parser.add_argument('--src-img', type=str, required = True, help='File path for source image to blend into destination image')
    parser.add_argument('--dst-img', type=str, required = True, help='File path of destination image to blend source image into')
    parser.add_argument('--mask-img', type=str, required = True, help='File path of mask image with information as to where to blend source image into destination image')
    parser.add_argument('--blended-img-out-path', type=str, default = None, help='File path of mask image with information as to where to blend source image into destination image')
    parser.add_argument('--results-folder', type=str, default = None, help='File path of mask image with information as to where to blend source image into destination image')
    parser.add_argument('--list_path', default='',
                        help='File for input list of all images to blend in csv format: obj_path;bg_path;mask_path in each line')
    parser.add_argument('--verbose', action='store_true', help='Print out progress of blending')
    args = parser.parse_args()

    assert not (args.list_path and (args.src_img or args.dst_img or args.mask_img)), "Either list_path or src_img, dst_img, and mask_img must be specified, not both. Otherise list_path will just be used"

    # GP-GAN arguments
    gp_gan_dir = args.gp_gan_dir
    src_dir = args.src_dir
    dst_dir = args.dst_dir
    mask_img = args.mask_img
    verbose = args.verbose
    blended_img_out_path = args.blended_img_out_path
    list_path = args.list_path
    results_folder = args.results_folder

    blend_with_gp_gan(src_dir, dst_dir, mask_img, blended_img_out_path, results_folder, list_path, verbose)