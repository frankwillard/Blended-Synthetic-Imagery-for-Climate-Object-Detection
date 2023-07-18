# Blended-Synthetic-Imagery-for-Climate-Object-Detection

Official repository for the code from the paper [Closing the Domain Gap -- Blended Synthetic Imagery for Climate Object Detection (Papers Track)](https://www.climatechange.ai/papers/neurips2022/37)

[Link to paper PDF](https://s3.us-east-1.amazonaws.com/climate-change-ai/papers/neurips2022/37/paper.pdf)

In submission for Environmental Data Science Journal

## Environment

The code from the repository was run under the `environment.yml` file. A minimal environment and Dockerfile are being constructed.

## Pre-Trained GP-GAN model

Download the pretrained model `blending_gan.npz` or `unsupervised_blending_gan.npz` from [Google Drive](https://drive.google.com/open?id=0Bybnpq8dvwudVjBHNWNHUmVSV28), and then put them in the folder `models`. Make sure this model path is passed into the GP-GAN script or set as a default path in the arguments.

You may also pre-train the GP-GAN model yourself, following the instructions in the GP-GAN README 

## Generate Single Synthetic Image

To generate an individual synthetic image, you can call run `python generate_synthetic_image.py`. There are various arguments to be used that can be found with the `--help` flag.  

## Generate Synthetic Dataset

To generate a synthetic dataset, you can build a wrapper that calls `python generate_synthetic_image.py`. We developed the `synthetic_dataset_generation.py` wrapper for our dataset creation, which includes some hard-coded information and file paths necessary for our experiments. There are various arguments you can find with the `--help` flag. 

Note: Running a wrapper that generates all image augmentations and then blends all images through the GP-GAN is more computationally efficient than generating each entire image (about 7 times as fast). This is because the GP-GAN must load the pre-trained model every time the run gp gan script is called, which may take 5-6 seconds. If we call it 200 times to generate 200 images, it will have to re-load that model 200 times, whereas if we call the script one time with a list of all of the images and destinations, it will only have to load the model once.
