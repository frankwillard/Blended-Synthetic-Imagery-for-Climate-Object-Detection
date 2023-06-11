## GP-GAN

gp_gan_one_to_one.py
* Takes in general augmented directory (subdirs by domain, holds canvases/masks/labels), destination directory (holds background images to place augmentations on), output_directory name, list of domains, and number of images to produce per domain combination. 
* For every combination of domains, the script pairs n backgrounds with n augmentations, which are passed into run_gp_gan.py. A one to one mapping is used in order to increase the number of new information being passed in.