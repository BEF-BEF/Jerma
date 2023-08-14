import os
import shutil


def split_directories():
    # Assuming the script is in the same directory as outDirectories
    script_directory = os.path.dirname(os.path.abspath(__file__))  # Gets the directory of the script
    source_directory = os.path.join(script_directory, "outDirectories")

    # List all directories under the source directory
    all_dirs = [d for d in os.listdir(source_directory) if os.path.isdir(os.path.join(source_directory, d))]

    # Sort the directories (optional, but can be useful)
    all_dirs.sort()

    counter = 0
    parent_counter = 1
    current_parent_directory = os.path.join(source_directory, f"outDirectories{parent_counter}")

    for d in all_dirs:
        # If counter reaches 999, reset it and create a new parent directory
        if counter >= 999:
            counter = 0
            parent_counter += 1
            current_parent_directory = os.path.join(source_directory, f"outDirectories{parent_counter}")

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
