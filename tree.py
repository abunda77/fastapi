import os

def print_directory_structure(root_dir, prefix=""):
    # List all files and directories in the root directory
    items = os.listdir(root_dir)
    
    # Sort items so that directories come before files
    items.sort(key=lambda x: (not os.path.isdir(os.path.join(root_dir, x)), x))
    
    # Iterate over all items in the directory
    for index, item in enumerate(items):
        # Determine if the current item is the last one in the directory
        is_last = index == len(items) - 1
        
        # Create the appropriate prefix
        new_prefix = prefix + ("└── " if is_last else "├── ")
        
        # Print the current item
        print(prefix + new_prefix + item)
        
        # If the current item is a directory, recursively print its structure
        if os.path.isdir(os.path.join(root_dir, item)):
            new_subprefix = prefix + ("    " if is_last else "│   ")
            print_directory_structure(os.path.join(root_dir, item), new_subprefix)

# Set the root directory
root_directory = "app"

# Print the directory structure
print_directory_structure(root_directory)
