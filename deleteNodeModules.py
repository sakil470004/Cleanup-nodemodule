#!/usr/bin/env python3
import os
import shutil
from pathlib import Path

# Safety: set to True to do a dry run (only log what would be deleted).
# Set to False to actually remove files/directories.
DRY_RUN = True

# Names of folders we want to remove when found at/after minDepth
TARGET_NAMES = ['node_modules', '.next', 'dist']


def delete_folder_recursive(folder_path):
    """Recursively delete a folder and all its contents."""
    if not os.path.exists(folder_path):
        return
    
    try:
        if DRY_RUN:
            # Count items in dry run mode
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    print(f'Would delete file: {file_path}')
                for dir_name in dirs:
                    dir_path = os.path.join(root, dir_name)
                    print(f'Would remove directory: {dir_path}')
            print(f'Would remove directory: {folder_path}')
        else:
            shutil.rmtree(folder_path)
    except Exception as e:
        print(f'Error deleting {folder_path}: {e}')


def find_and_delete_targets(start_path, min_depth, current_depth=0):
    """Recursively find and delete target directories at or below minDepth."""
    if not os.path.exists(start_path):
        return
    
    try:
        entries = os.listdir(start_path)
    except PermissionError:
        return
    
    for entry in entries:
        cur_path = os.path.join(start_path, entry)
        
        if os.path.isdir(cur_path):
            # Check if we're at the right depth and this is a target directory
            if current_depth >= min_depth and entry in TARGET_NAMES:
                action = 'Would delete:' if DRY_RUN else 'Deleting:'
                print(f'{action} {cur_path}')
                delete_folder_recursive(cur_path)
            else:
                # Recurse deeper
                find_and_delete_targets(cur_path, min_depth, current_depth + 1)


if __name__ == '__main__':
    target_directory = './'  # Replace with your root folder path
    min_depth = 0  # Minimum depth to start deleting (0 = all levels)
    
    find_and_delete_targets(target_directory, min_depth)
