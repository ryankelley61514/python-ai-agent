import os
from functions.confirm_valid_directory import confirm_valid_directory

def get_files_info(working_directory, directory="."):
    try:
        is_valid, full_path = confirm_valid_directory(working_directory, directory)
        if not is_valid:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'
        
        directory_contents = []
        for item in os.listdir(full_path):
            item_path = os.path.join(full_path, item)
            item_details = f'{item}: file_size={os.path.getsize(item_path)}, is_dir={os.path.isdir(item_path)}'
            directory_contents.append(item_details)
        
        return f'- {"\n- ".join((directory_contents))}'

    except Exception as e:
        return f'Error: {e}'