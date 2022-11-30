# Blended-Synthetic-Imagery-for-Climate-Object-Detection

General pipeline:
* Create set of cropped objects for each domain (./Image-Augmentation/crop_shadows.py)
* Sample said objects and randomly place them on canvases, create corresponding masks and YOLO labels (./Image-Augmentation/csv_augmenter.py)


## Assumed File Directory Structure


## Image-Augmentation

[Image-Augmentation README](https://github.com/frankwillard/Blended-Synthetic-Imagery-for-Climate-Object-Detection/blob/main/Image-Augmentation/README.md)

## GP-GAN

gp_gan_one_to_one.py- Takes in general augmented directory (subdirs by domain, holds canvases/masks/labels), destination directory (holds background images to place augmentations on), output_directory name, list of domains, and number of images to produce per domain combination. 

For every combination of domains, the script creates a unique 

src_dir = "/scratch/public/augmented_images/"
dst_dir = "/scratch/public/jitter/wt/images/"
#REPLACE/Background/
results_dir = "/scratch/public/jitter/wt/images/Synthetic/"

domains = ["EM", "NW", "SW"]

n = 182

run_one_to_one(src_dir, dst_dir, results_dir, domains, n)