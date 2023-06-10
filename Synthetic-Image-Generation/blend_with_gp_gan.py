import subprocess
import argparse
import os

def blend_with_gp_gan(src_img, dst_img, mask_img, blended_img_out_path, verbose=False):
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
    #Copies txt file of mask to synthetic output
    cmd = f"python3 run_gp_gan.py --src_image {src_img} --dst_image \"{dst_img}\" --mask_image {mask_img} --blended_image {blended_img_out_path}"
    
    if verbose:
        print("Running command:")
        print(cmd)

    subprocess.run(cmd, shell=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Creates a synthetic image by placing random objects and blending them with background images blending images through the GP-GAN')

    # GP-GAN arguments
    parser.add_argument('--src-img', type=str, required = True, help='File path for source image to blend into destination image')
    parser.add_argument('--dst-img', type=str, required = True, help='File path of destination image to blend source image into')
    parser.add_argument('--mask-img', type=str, required = True, help='File path of mask image with information as to where to blend source image into destination image')
    parser.add_argument('--verbose', action='store_true', help='Print out progress of blending')
    args = parser.parse_args()

    # GP-GAN arguments
    src_dir = args.src_dir
    dst_dir = args.dst_dir
    mask_img = args.mask_img
    verbose = args.verbose

    blend_with_gp_gan(src_dir, dst_dir, mask_img, verbose)