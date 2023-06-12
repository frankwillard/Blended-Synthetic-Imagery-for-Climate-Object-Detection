#!/bin/bash

blend_with_gp_gan() {
    local gp_gan_dir="$1"
    local src_img="$2"
    local dst_img="$3"
    local mask_img="$4"
    local blended_img_out_path="$5"
    local results_folder="$6"
    local list_path="$7"
    local verbose="$8"

    #Copies txt file of mask to synthetic output
    local cmd="python3 ${gp_gan_dir}/run_gp_gan.py"

    if [[ -n "$list_path" ]]; then
        cmd+=" --list_path ${list_path}"
    else
        cmd+=" --src_image ${src_img} --dst_image \"${dst_img}\" --mask_image ${mask_img}"
    fi

    if [[ -n "$blended_img_out_path" ]]; then
        cmd+=" --blended_image ${blended_img_out_path}"
    elif [[ -n "$results_folder" ]]; then
        cmd+=" --results_folder ${results_folder}"
    fi

    if [[ "$verbose" == "true" ]]; then
        echo "Running command:"
        echo "$cmd"
    fi

    eval "$cmd"
}

# Call the blend_with_gp_gan function with command-line arguments
blend_with_gp_gan "$@"