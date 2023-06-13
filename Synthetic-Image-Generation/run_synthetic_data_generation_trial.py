import subprocess


# Augment image arguments
implantable_objects_dir = "/scratch/cek28/jitter/wt/turbines/new_cropped_turbines/"
augmented_images_results_dir = "/scratch/cek28/jitter/wt/Synthetic-Images-Test/Augmentations/"
random_seed = 42
# num_objects_to_sample_per_image_percentile = args.num_objects_to_sample_per_image_percentile
# offset_ctr = args.offset_ctr
# gp_gan_blend_offset = args.gp_gan_blend_offset
# real_label_dir = ""


# GP-GAN arguments
background_images_dir = "/scratch/cek28/jitter/wt/images/"
final_results_dir = "/scratch/cek28/jitter/wt/Synthetic-Images-Test/Synthetic-Imagery"
gp_gan_dir = "/scratch/cek28/jitter/wt/Blended-Synthetic-Imagery-for-Climate-Object-Detection/Synthetic-Image-Generation/GP-GAN"
# g_path = "/scratch/cek28/jitter/wt/models/blending_gan.npz"
g_path = "/scratch/cek28/jitter/wt/models/blending_gan.npz"


# Dataset arguments
domains = "EM NW SW"


# generate_unique_src_augmentations = True
# verbose = True


# ============ MAIN HYPERPARAMETERS =================

num_objects_to_sample_per_image_constant = 5
num_synthetic_images_per_domain = 3
objects_augmenter_has_access_to = 1
experiment_name = "first_experiment"

cmd = f"python3 synthetic_dataset_generation.py --g-path {g_path} --implantable-objects-dir {implantable_objects_dir} --objects-augmenter-has-access-to {objects_augmenter_has_access_to} --augmented-images-results-dir {augmented_images_results_dir} --random-seed {random_seed} --num-objects-to-sample-per-image-constant {num_objects_to_sample_per_image_constant} --background-images-dir {background_images_dir} --final-results-dir {final_results_dir} --gp-gan-dir {gp_gan_dir} --domains {domains} --num-synthetic-images-per-domain {num_synthetic_images_per_domain} --experiment-name {experiment_name} --generate-unique-src-augmentations --generate-all-augmentations-first --verbose"

print(cmd)

subprocess.run(cmd, shell=True)