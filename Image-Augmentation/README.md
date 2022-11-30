# Image-Augmentation

## Shadow Parsing

### shadow_parser- 

plot_shadows and plot_unmatched uses the functions of bounding_boxs to plot the regular and shadow labels of an image.

In order to complete our image augmentation, we wanted to crop real wind turbines and then put them onto a white canvas and blend them into a background. In doing so, we created YOLO labels that included just the turbine for feeding into YOLO, as well as labels of the wind turbine and the shadow for the image augmentation. This is because the shadow provides useful context for the turbine and when taking the time to label- this does not greatly increase
the time cost. 

crop_shadows goes through the real and shadow labels uses the shadow labels to crop out turbines, with additional checks to ensure the object is not too close to the image border and ensures that it geometrically contains a turbine label within it. This is because in order to create labels for synthetic imagery, we need the information as to where a turbine is relative to the entire crop with the shadow. By ensuring a one to one match, the relevant calculations are made to determine relative label. 

## Image Augmentation

sample_txts.py- From a directory containing txt files (in YOLOv3 format- contain location/size information), it samples 100 of these txt files and saves into an output file

experiment2txts.txt- Sample output file from sample_txts.py

csv_augmenter.py- Accepts txt file containing YOLOv3 files, cropped wind turbines (and coinciding bounding box information in YOLOv3 format), then samples txt files and runs augment_images.py

augment_images.py- Samples wind turbines and places them in specified location/size (based on sampled txt file) with random rotation (while preventing overlap with border/each other), performs same transformations to make coinciding binary mask, calculates relative size/positioning data for YOLOv3 bounding box txt file

results9 folder- Contains output of running csv_augmenter.py- Several augmented images with coinciding binary masks and YOLOv3 bounding box txt files
