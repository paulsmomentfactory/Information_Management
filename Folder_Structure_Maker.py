import os
import tempfile
#This script can be used to copy the folder structures of everything under a file path...
"""
source_dir = input("Enter the source directory path: ")
> C:\Users\savlu\Desktop\old stuff
target_dir = input("Enter the target directory path: ")
C:\Users\savlu\Desktop\old stuff_file_structure_copy
"""
#^^^ this will copu everything under the folder "old stuff" and will put the folder structure (basically it creates the folders it needs to replicate the folder structure for everything under old stuff in the new path... "old stuff_file_structure_copy")
def has_write_permissions(directory):
    try:
        tempfile.TemporaryFile(dir=directory).close()
    except OSError:
        return False
    return True

def get_all_paths(directory):
    paths = []
    for dirpath, _, _ in os.walk(directory):
        paths.append(dirpath)
    return paths

def recreate_directory_structure(source_dir, target_dir):
    if not has_write_permissions(target_dir):
        print(f"Write permissions are required for the directory {target_dir}.")
        print("Please change the permissions and try again.")
        print("This can be done by right-clicking the folder, selecting Properties, going to the Security tab, and modifying the permissions.")
        return
    paths = get_all_paths(source_dir)
    for path in paths:
        relative_path = os.path.relpath(path, source_dir)
        new_path = os.path.join(target_dir, relative_path)
        os.makedirs(new_path, exist_ok=True)

source_dir = input("Enter the source directory path: ")
target_dir = input("Enter the target directory path: ")

recreate_directory_structure(source_dir, target_dir)
