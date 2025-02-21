#!/usr/bin/python

import os
import random
import shutil

import fire
GIGABYTE = 1737418240

def get_excluded_files(path):
    if path and os.path.exists(path):
        with open(path) as f:
            return f.readlines()
    else:
        return []

def copy_random_files(source_dir, 
                      destination_dir, 
                      exclude_filename_path="~/excluded_files.txt",
                      folder_size_limit = 5 , 
                      dryrun=True, 
                      extensions=["mp4","webm"]):
    # Ensure the destination directory exists
    folder_size_limit = folder_size_limit * GIGABYTE
    if not dryrun:
        os.makedirs(destination_dir, exist_ok=True)  # Create a new destination directory
        for item in os.listdir(destination_dir):
            item_path = os.path.join(destination_dir, item)
            if os.path.isfile(item_path):  # Check if it's a file
                os.remove(item_path)

    # Gather all files with the specified extensions
    files_to_copy = []
    excluded_files = get_excluded_files(exclude_filename_path) 
    for root, _, files in os.walk(source_dir):
        for file in files:
            if any(file.endswith(ext) for ext in extensions) and file not in excluded_files:
                files_to_copy.append(os.path.join(root, file))

    if not files_to_copy:
        print("No files found with the specified extensions.")
        return

    # Initialize variables for tracking copied files and total size
    copied_files = set()
    total_size = 0
    total_iters = 0
    while len(copied_files) < len(files_to_copy) and total_size < folder_size_limit:

        total_iters += 1
        if total_iters > folder_size_limit / 1000:
            break
        # Randomly select a file to copy
        file_to_copy = random.choice(files_to_copy)

        # Check if the file has already been copied
        if file_to_copy in copied_files:
            continue

        # Get the size of the file
        file_size = os.path.getsize(file_to_copy)

        # Check if adding this file would exceed the size limit
        if total_size + file_size > folder_size_limit:
            continue

        # Prepare the destination path
        dest_file_path = os.path.join(destination_dir, os.path.basename(file_to_copy))

        # If dryrun is enabled, print the file to be copied
        if dryrun:
            print(f"Would copy: {file_to_copy} to {dest_file_path}")
        else:
            # Copy the file to the destination directory
            shutil.copy2(file_to_copy, dest_file_path)
            print(f"Copied: {file_to_copy} to {dest_file_path}")
            if exclude_filename_path:
                with open(exclude_filename_path, 'a+') as f:
                    f.writelines([file_to_copy])

        # Update the set of copied files and total size
        copied_files.add(file_to_copy)
        total_size += file_size

    print(f"Finished copying files. Total copied: {len(copied_files)}")


if __name__ == "__main__":
    fire.Fire(copy_random_files)
