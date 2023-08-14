from utils import fix_stacked_directories, copy_nested_directories
import os
fix_stacked_directories()

source_directory = "outDirectories"
destination_directory = "outDirTest"

# Ensure the destination directory exists
if not os.path.exists(destination_directory):
    os.makedirs(destination_directory)

copy_nested_directories(source_directory, destination_directory)
