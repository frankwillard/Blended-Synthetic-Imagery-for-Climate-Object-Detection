# Image-Augmentation

## Shadow Parsing

### shadow_parser- 

plot_shadows and plot_unmatched uses the functions of bounding_boxs to plot the regular and shadow labels of an image.

In order to complete our image augmentation, we wanted to crop real wind turbines and then put them onto a white canvas and blend them into a background. In doing so, we created YOLO labels that included just the turbine for feeding into YOLO, as well as labels of the wind turbine and the shadow for the image augmentation. This is because the shadow provides useful context for the turbine and when taking the time to label- this does not greatly increase
the time cost. 

crop_shadows goes through the real and shadow labels uses the shadow labels to crop out turbines, with additional checks to ensure the object is not too close to the image border and ensures that it geometrically contains a turbine label within it. This is because in order to create labels for synthetic imagery, we need the information as to where a turbine is relative to the entire crop with the shadow. By ensuring a one to one match, the relevant calculations are made to determine relative label. 

## Image Augmentation

augment_images.py: 
* Called by csv_augmenter- performs the augmentations. Outputs a user-defined quantity of canvases and their corresponding masks and labels (YOLO format)

csv_augmenter.py: 
* For every domain, it samples cropped images and places them onto a canvas in random locations/rotations. 
* User defines variables including buffer from image border, number of crops to place, how much to buffer the object in the mask going into GP-GAN (decreases chance of edges being blended away but increases surrounding context blended in)
* Outputs metadata of matchings (output image) to JSON.

get_distribution.py
* Helper script that gets the distribution for a given domain using the directory- unnormalizes the YOLO labels and grabs the data. Has potential use case in csv_augmenter if you want to choose the number of objects placed on the canvas by percentile of the distribution for a given domains

