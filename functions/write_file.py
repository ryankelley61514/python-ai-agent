import os
from functions.confirm_valid_directory import confirm_valid_directory

def write_file(working_directory, file_path, content):
    try:
        is_valid, full_path = confirm_valid_directory(working_directory, file_path)
        if not is_valid:
            return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'

        if not os.path.exists(full_path):
            os.makedirs(os.path.dirname(full_path), exist_ok=True)

        with open(full_path, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f'Error: {e}'