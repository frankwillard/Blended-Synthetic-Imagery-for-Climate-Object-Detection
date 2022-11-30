# Blended-Synthetic-Imagery-for-Climate-Object-Detection

## Image-Augmentation

augment_images.py: 
* Called by csv_augmenter- performs the augmentations. Outputs a user-defined quantity of canvases and their corresponding masks and labels (YOLO format)

csv_augmenter.py: 
* For every domain, it samples cropped images and places them onto a canvas in random locations/rotations. 
* User defines variables including buffer from image border, number of crops to place, how much to buffer the object in the mask going into GP-GAN (decreases chance of edges being blended away but increases surrounding context blended in)
* Outputs metadata of matchings (output image) to JSON.

get_distribution.py
* Helper script that gets the distribution for a given domain using the directory- unnormalizes the YOLO labels and grabs the data. Has potential use case in csv_augmenter if you want to choose the number of objects placed on the canvas by percentile of the distribution for a given domains
