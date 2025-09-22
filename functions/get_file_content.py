import os
from functions.config import MAX_CHARS
from functions.confirm_valid_directory import confirm_valid_directory

def get_file_content(working_directory, file_path):
    try:
        is_valid, full_path = confirm_valid_directory(working_directory, file_path)
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