import subprocess

# Augment image arguments
implantable_objects_dir = "/scratch/cek28/jitter/wt/turbines/new_cropped_turbines/"
augmented_images_results_dir = "/home/fcw/Synthetic-Images-Test/Augmentations/"
random_seed = 42
# num_objects_to_sample_per_image_percentile = args.num_objects_to_sample_per_image_percentile
num_objects_to_sample_per_image_constant = 3
# offset_ctr = args.offset_ctr
# gp_gan_blend_offset = args.gp_gan_blend_offset
# real_label_dir = ""

# GP-GAN arguments
background_images_dir = "/scratch/cek28/jitter/wt/images/"
final_results_dir = "/home/fcw/Synthetic-Images-Test/Synthetic-Imagery/"
gp_gan_dir = "/home/fcw/Blended-Synthetic-Imagery-for-Climate-Object-Detection/GP-GAN/"

# Dataset arguments
domains = "EM NW SW"
num_synthetic_images_per_domain = 5
objects_to_have_access_to = 100
# generate_unique_src_augmentations = True
# verbose = True

#cmd = f"python run_gp_gan.py --src_image {src_img} --dst_image \"{dst_img}\" --mask_image {mask_img} --blended_image {blended_img_out_path}"

cmd = f"python3 synthetic_dataset_generation.py --implantable-objects-dir {implantable_objects_dir} --augmented-images-results-dir {augmented_images_results_dir} --random-seed {random_seed} --num-objects-to-sample-per-image-constant {num_objects_to_sample_per_image_constant} --background-images-dir {background_images_dir} --final-results-dir {final_results_dir} --gp_gan_dir {gp_gan_dir} --domains {domains} --num-synthetic-images-per-domain {num_synthetic_images_per_domain} --generate-unique-src-augmentations --verbose"

print(cmd)

subprocess.run(cmd, shell=True)