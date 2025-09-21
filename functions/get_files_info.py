import os

def get_files_info(working_directory, directory="."):
    try:
        full_path = os.path.join(working_directory, directory)
        # print(full_path)
        # Normalize the paths to resolve '..' and make them absolute
        normalized_working_dir = os.path.abspath(working_directory)
        # print(normalized_working_dir)
        normalized_full_path = os.path.abspath(full_path)
        # print(normalized_full_path)
        # Check if the normalized full path starts with the normalized working directory
        is_valid = normalized_full_path.startswith(normalized_working_dir)
        # print(is_valid)
        if not is_valid:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'
        
        directory_contents = []
        for item in os.listdir(full_path):
            item_path = os.path.join(full_path, item)
            item_details = f"{item}: file_size={os.path.getsize(item_path)}, is_dir={os.path.isdir(item_path)}"
            directory_contents.append(item_details)
        
        return f"- {'\n- '.join((directory_contents))}"

    except Exception as e:
        return f"Error: {e}"
    

