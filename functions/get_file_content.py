import os
from functions.config import MAX_CHARS

def get_file_content(working_directory, file_path):
    try:
        full_path = os.path.join(working_directory, file_path)
        # Normalize the paths to resolve '..' and make them absolute
        normalized_working_dir = os.path.abspath(working_directory)
        normalized_full_path = os.path.abspath(full_path)
        # Check if the normalized full path starts with the normalized working directory
        is_valid = normalized_full_path.startswith(normalized_working_dir)
        if not is_valid:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(full_path, 'r') as f:
            file_content_string = f.read(MAX_CHARS)
            if len(file_content_string) == MAX_CHARS:
                file_content_string += f'\n[...File "{file_path}" truncated at 10000 characters]'
        
        return file_content_string
    
    except Exception as e:
        return f'Error: {e}'