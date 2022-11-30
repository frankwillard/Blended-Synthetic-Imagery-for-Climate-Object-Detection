# Blended-Synthetic-Imagery-for-Climate-Object-Detection

General pipeline:
* Collect dataset of images clustered by domain (including both Real Images and Background Images to have objects blended onto)
* Optional: Create set of cropped objects for each domain (./Image-Augmentation/crop_shadows.py)
* Sample said objects and randomly place them on canvases, create corresponding masks and YOLO labels (./Image-Augmentation/csv_augmenter.py)
* Blend said augmented canvases (and their masks) with background images using the GP-GAN (./GP-GAN/gp_gan_one_to_one.py)

## Assumed File Directory Structure

For some of the scripts, there is an assumed file structure including subdirectories of domains in order to not require one to pass a different directory for every domain.

augment_images.py assumes:
* cropped_dir- Directory for cropped images/labels - Has a subdir of images and a subdir of labels (whose subdirs are the domain names)
    * Example: cropped_dir = "/dir1/cropped/", domains = ["NW", "SE"]
        * cropped_dir has subdirs of "images" and "labels"
        * The "images" subdir and "labels" subdir both have subdirs of "NW" and "SE" (the example domains)
* real_label_dir- Directory holding real labels to get distribution from (subdirs are domains)
    * Example: real_label_dir = "/dir1/labels/", domains = ["NW", "SE"]
        * real_label_dir has subdirs of "NW" and "SE"
        * "NW" and "SE" directories have subdir of "Real"

gp_gan_one_to_one.py assumes:
* src_dir- Directory for augmented canvases/masks/labels (will be created by Image-Augmentation so will adhere)
* dst_dir- Directory for background images (subdir of domain, subdir of Background)
    * Example: dst_dir: "/dir1/images/", domains = ["NW", "SE"]
        * dst_dir has subdirs of "NW" and "SE"
        * "NW" and "SE" directories have subdir of "Background"
   
## Image-Augmentation

[Image-Augmentation README](https://github.com/frankwillard/Blended-Synthetic-Imagery-for-Climate-Object-Detection/blob/main/Image-Augmentation/README.md)

## GP-GAN

[GP-GAN README](https://github.com/frankwillard/Blended-Synthetic-Imagery-for-Climate-Object-Detection/blob/main/GP-GAN/README.md)