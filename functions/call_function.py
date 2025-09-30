from google.genai import types # pyright: ignore[reportMissingImports]
from functions.schema_functions import available_functions
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file

working_directory = './calculator'

def call_function(function_call_part, verbose=False):
    function_call_part.args["working_directory"] = working_directory

    function_dict = {
        'get_files_info': get_files_info,
        'get_file_content': get_file_content,
        'run_python_file': run_python_file,
        'write_file': write_file,
    }

    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    if function_call_part.name not in function_dict:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )

    function_result = function_dict[function_call_part.name](**function_call_part.args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": function_result},
            )
        ],
    )