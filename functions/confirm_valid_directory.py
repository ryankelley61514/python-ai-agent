import os

def confirm_valid_directory(working_directory, directory):
    full_path = os.path.join(working_directory, directory)

    # Normalize the paths to resolve '..' and make them absolute
    normalized_working_dir = os.path.abspath(working_directory)
    normalized_full_path = os.path.abspath(full_path)
    
    # Check if the normalized full path starts with the normalized working directory
    is_valid = normalized_full_path.startswith(normalized_working_dir)

    return is_valid, full_path