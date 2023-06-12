#!/bin/bash

# Augment image arguments
implantable_objects_dir="/scratch/cek28/jitter/wt/turbines/new_cropped_turbines/"
augmented_images_results_dir="/home/fcw/Synthetic-Images-Test/Augmentations/"
random_seed=42

# GP-GAN arguments
background_images_dir="/scratch/cek28/jitter/wt/images/"
final_results_dir="/home/fcw/Synthetic-Images-Test/Synthetic-Imagery/"
gp_gan_dir="/home/fcw/Blended-Synthetic-Imagery-for-Climate-Object-Detection/Synthetic-Image-Generation/GP-GAN/"

# Dataset arguments
domains="EM NW SW"

# MAIN HYPERPARAMETERS
num_objects_to_sample_per_image_constant=3
num_synthetic_images_per_domain=5
objects_augmenter_has_access_to=100
experiment_name="first_experiment"

cmd="python3 synthetic_dataset_generation.py --implantable-objects-dir $implantable_objects_dir --augmented-images-results-dir $augmented_images_results_dir --random-seed $random_seed --num-objects-to-sample-per-image-constant $num_objects_to_sample_per_image_constant --background-images-dir $background_images_dir --final-results-dir $final_results_dir --gp_gan_dir $gp_gan_dir --domains \"$domains\" --num-synthetic-images-per-domain $num_synthetic_images_per_domain --experiment_name $experiment_name --generate-unique-src-augmentations --generate_all_augmentations_first --verbose"

echo $cmd

eval $cmd