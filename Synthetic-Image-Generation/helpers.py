import re
import os
import random
import glob
import shutil


def multiple_replace(dict, text):
    """
    Perform multiple replacements in a given text based on a dictionary.

    Args:
        dict (dict): A dictionary where keys represent patterns to be replaced and values are the corresponding replacements.
        text (str): The input text to perform replacements on.

    Returns:
        str: The text with replacements applied based on the provided dictionary.
    """
    # Create a regular expression  from the dictionary keys
    regex = re.compile("(%s)" % "|".join(map(re.escape, dict.keys())))

    # For each match, look-up corresponding value in dictionary
    return regex.sub(lambda mo: dict[mo.string[mo.start() : mo.end()]], text)


def createPath(curr_subdir):
    """
    Create a directory if it doesn't exist.

    Args:
        curr_subdir (str): The path of the directory to be created.
    """
    if not os.path.exists(curr_subdir):
        os.makedirs(curr_subdir, exist_ok=True)
        print(curr_subdir + " directory was made")


def iterative_sample_without_replacement(population, n):
    """
    Sample elements from a population without replacement iteratively.

    If the desired number of samples (n) is smaller than or equal to the size of the population,
    it will sample without replacement directly. Otherwise, it will sample the entire population
    first, and then continue to sample the remaining elements without replacement until reaching
    the desired number of samples.

    Args:
        population (list): The population to sample from.
        n (int): The number of samples to obtain.

    Returns:
        list: A list of sampled elements from the population without replacement.
    """

    print(f"Sampling without replacement {len(population)} {n}")

    sampled_list = []

    # If n <= len(population), sample without replacement
    if n <= len(population):
        sampled_list.extend(random.sample(population, n))
    else:
        # Sample the first 100 elements without replacement
        sampled_list.extend(random.sample(population, len(population)))

        remaining_samples = n - len(population)
        while remaining_samples > 0:
            # Sample the remaining elements without replacement
            sampled_list.extend(
                random.sample(population, min(remaining_samples, len(population)))
            )
            remaining_samples -= len(population)

    return sampled_list


def move_synthetic_files_to_domain_pair_subdirectories(directory, verbose=False):
    """
    Move files in the given directory into corresponding subdirectories based on file names.

    Args:
        directory (str): Path to the directory containing the files.

    Returns:
        None
    """

    file_pattern = os.path.join(directory, "*.jpg")
    file_paths = glob.glob(file_pattern)

    for file_path in file_paths:
        filename = os.path.basename(file_path)
        src_domain = filename.split("_")[1]
        target_domain = filename.split("_")[3]
        subdirectory = f"s_{src_domain}_t_{target_domain}"
        destination_dir = os.path.join(directory, subdirectory)

        shutil.move(file_path, destination_dir)
        if verbose:
            print("Moved " + file_path + " to " + destination_dir)
