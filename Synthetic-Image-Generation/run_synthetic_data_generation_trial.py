import subprocess


# Augment image arguments
implantable_objects_dir = "/scratch/cek28/jitter/wt/turbines/new_cropped_turbines/"
augmented_images_results_dir = "/scratch/cek28/jitter/wt/Synthetic-Images-Test/Augmentations/"
num_target_background_images = 100
random_seed = 42

# GP-GAN arguments
background_images_dir = "/scratch/cek28/jitter/wt/images/"
final_results_dir = "/scratch/cek28/jitter/wt/Synthetic-Images-Test/Synthetic-Imagery"
gp_gan_dir = "/scratch/cek28/jitter/wt/Blended-Synthetic-Imagery-for-Climate-Object-Detection/Synthetic-Image-Generation/GP-GAN"
g_path = "/scratch/cek28/jitter/wt/models/blending_gan.npz"

# Dataset arguments
domains = "EM NW SW"
root = "/scratch/cek28/jitter/wt/"
domain_dict_path = "/scratch/cek28/jitter/wt/domain_overview.json"

# ============ MAIN HYPERPARAMETERS =================

num_objects_to_sample_per_image_constant = 4
num_synthetic_images_per_domain = 5
objects_augmenter_has_access_to = 90
experiment_name = "first_experiment"

cmd = f"python3 synthetic_dataset_generation.py --g-path {g_path} --implantable-objects-dir {implantable_objects_dir} --objects-augmenter-has-access-to {objects_augmenter_has_access_to} --augmented-images-results-dir {augmented_images_results_dir} --random-seed {random_seed} --num-objects-to-sample-per-image-constant {num_objects_to_sample_per_image_constant} --final-results-dir {final_results_dir} --gp-gan-dir {gp_gan_dir} --domains {domains} --root {root} --domain-dict-path {domain_dict_path} --num-target-background-images {num_target_background_images} --num-synthetic-images-per-domain {num_synthetic_images_per_domain} --experiment-name {experiment_name} --generate-unique-src-augmentations --generate-all-augmentations-first --verbose"

print(cmd)

subprocess.run(cmd, shell=True)
