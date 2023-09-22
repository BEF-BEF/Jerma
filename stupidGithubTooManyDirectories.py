import os
import shutil

def split_directories():
    script_directory = os.path.dirname(os.path.abspath(__file__))  # Gets the directory of the script

    # Handle outDirectories and subtitleDirectories
    for directory_name in ["outDirectories", "subtitleDirectories"]:
        source_directory = os.path.join(script_directory, directory_name)
        folder_count = sum([1 for item in os.listdir(source_directory) if os.path.isdir(os.path.join(source_directory, item))])
        
        if folder_count > 999:
            handle_directory_split(script_directory, directory_name)

def handle_directory_split(script_directory, directory_name):
    source_directory = os.path.join(script_directory, directory_name)

    # List all directories under the source directory excluding ones like directory_name1, directory_name2, etc.
    all_dirs = [d for d in os.listdir(source_directory) if os.path.isdir(os.path.join(source_directory, d)) and not d.startswith(directory_name)]
    all_dirs.sort()

    counter = 0
    parent_counter = 1
    current_parent_directory = os.path.join(source_directory, f"{directory_name}{parent_counter}")

    for d in all_dirs:
        # If counter reaches 999, reset it and create a new parent directory
        if counter >= 999:
            counter = 0
            parent_counter += 1
            current_parent_directory = os.path.join(source_directory, f"{directory_name}{parent_counter}")

            # Create new parent directory if it doesn't exist
            if not os.path.exists(current_parent_directory):
                os.makedirs(current_parent_directory)

        # Move the directory
        shutil.move(os.path.join(source_directory, d), os.path.join(current_parent_directory, d))
        counter += 1

def combine_directories(source_directory="outDirectories", parent_directory_prefix="outDirectories"):
    # List all directories with prefix under the source directory
    parent_dirs = [d for d in os.listdir(source_directory) if os.path.isdir(os.path.join(source_directory, d)) and d.startswith(parent_directory_prefix)]

    for parent_dir in parent_dirs:
        parent_path = os.path.join(source_directory, parent_dir)
        for sub_dir in os.listdir(parent_path):
            shutil.move(os.path.join(parent_path, sub_dir), os.path.join(source_directory, sub_dir))
        os.rmdir(parent_path)  # remove the empty parent directory
