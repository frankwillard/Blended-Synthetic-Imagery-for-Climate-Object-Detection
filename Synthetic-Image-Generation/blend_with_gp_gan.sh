#!/bin/bash

# Input arguments
src_img="$1"
dst_img="$2"
mask_img="$3"
verbose="$4"

# Command to execute the blending
cmd="python run_gp_gan.py --src_image \"$src_img\" --dst_image \"$dst_img\" --mask_image \"$mask_img\""

# Print the command if verbose flag is set
if [[ $verbose ]]; then
    echo "Running command:"
    echo $cmd
fi

# Execute the command
eval $cmd