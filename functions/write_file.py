import os
from functions.confirm_valid_directory import confirm_valid_directory
from google.genai import types # pyright: ignore[reportMissingImports]

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes string content to a file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to file to write, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="String content to write to the file.",
            ),
        },
    ),
)

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