# Blended-Synthetic-Imagery-for-Climate-Object-Detection

General pipeline:
* Create set of cropped objects for each domain (./Image-Augmentation/crop_shadows.py)
* Sample said objects and randomly place them on canvases, create corresponding masks and YOLO labels (./Image-Augmentation/csv_augmenter.py)


## Assumed File Directory Structure


## Image-Augmentation

[Image-Augmentation README](https://github.com/frankwillard/Blended-Synthetic-Imagery-for-Climate-Object-Detection/blob/main/Image-Augmentation/README.md)

## GP-GAN

[GP-GAN README](https://github.com/frankwillard/Blended-Synthetic-Imagery-for-Climate-Object-Detection/blob/main/GP-GAN/README.md)