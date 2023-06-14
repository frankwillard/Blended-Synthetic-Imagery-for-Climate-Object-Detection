import subprocess
import os

# Augment image arguments
implantable_objects_dir = "/scratch/cek28/jitter/wt/turbines/new_cropped_turbines/"
augmented_images_results_dir = "/scratch/cek28/jitter/wt/Synthetic-Images-Test/Augmentations/"
random_seed = 42

# GP-GAN arguments
background_images_dir = "/scratch/cek28/jitter/wt/images/"
final_results_dir = "/scratch/cek28/jitter/wt/Synthetic-Images-Test/Synthetic-Imagery"
gp_gan_dir = "/scratch/cek28/jitter/wt/Blended-Synthetic-Imagery-for-Climate-Object-Detection/Synthetic-Image-Generation/GP-GAN"
g_path = "/scratch/cek28/jitter/wt/models/blending_gan.npz"

# Dataset arguments
domains = "NW SW"
root = "/scratch/cek28/jitter/wt/"
domain_dict_path = "/scratch/cek28/jitter/wt/domain_overview.json"


# ============ MAIN HYPERPARAMETERS =================
num_synthetic_images_per_domain = 100
num_target_background_images = 100

# Sweep over the density of turbines implanted.
for num_objects_to_sample_per_image_constant in [1, 2, 3, 4, 5]:
    objects_augmenter_has_access_to = 100
    experiment_name = f"density_{num_objects_to_sample_per_image_constant}"
    kRoot = f"/scratch/cek28/jitter/wt/synthetic/density_{num_objects_to_sample_per_image_constant}"
    final_results_dir = os.path.join(kRoot, "images")
    augmented_images_results_dir = os.path.join(kRoot)

    cmd = f"python3 synthetic_dataset_generation.py --g-path {g_path} --implantable-objects-dir {implantable_objects_dir} --objects-augmenter-has-access-to {objects_augmenter_has_access_to} --augmented-images-results-dir {augmented_images_results_dir} --random-seed {random_seed} --num-objects-to-sample-per-image-constant {num_objects_to_sample_per_image_constant} --final-results-dir {final_results_dir} --gp-gan-dir {gp_gan_dir} --domains {domains} --root {root} --domain-dict-path {domain_dict_path} --num-target-background-images {num_target_background_images} --num-synthetic-images-per-domain {num_synthetic_images_per_domain} --experiment-name {experiment_name} --generate-unique-src-augmentations --generate-all-augmentations-first --verbose"

    print(cmd)

    subprocess.run(cmd, shell=True)

# Sweep over the number of turbine examples available to the augmenter.
for objects_augmenter_has_access_to in [1, 5, 10, 50, 150]:
    num_objects_to_sample_per_image_constant = 3
    experiment_name = f"unique_objects_{objects_augmenter_has_access_to}"
    kRoot = f"/scratch/cek28/jitter/wt/synthetic/unique_objects_{objects_augmenter_has_access_to}"
    final_results_dir = os.path.join(kRoot, "images")
    augmented_images_results_dir = os.path.join(kRoot, "augmentations")

    cmd = f"python3 synthetic_dataset_generation.py --g-path {g_path} --implantable-objects-dir {implantable_objects_dir} --objects-augmenter-has-access-to {objects_augmenter_has_access_to} --augmented-images-results-dir {augmented_images_results_dir} --random-seed {random_seed} --num-objects-to-sample-per-image-constant {num_objects_to_sample_per_image_constant} --final-results-dir {final_results_dir} --gp-gan-dir {gp_gan_dir} --domains {domains} --root {root} --domain-dict-path {domain_dict_path} --num-target-background-images {num_target_background_images} --num-synthetic-images-per-domain {num_synthetic_images_per_domain} --experiment-name {experiment_name} --generate-unique-src-augmentations --generate-all-augmentations-first --verbose"

    print(cmd)

    subprocess.run(cmd, shell=True)
        
