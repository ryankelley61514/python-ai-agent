import os
import sys
import subprocess
from functions.confirm_valid_directory import confirm_valid_directory

def run_python_file(working_directory, file_path, args=[]):
    try:
        is_valid, full_path = confirm_valid_directory(working_directory, file_path)
        if not str(file_path).endswith('.py'):
            return f'Error: "{file_path}" is not a Python file.'
        if not is_valid:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(full_path):
            return f'Error: File "{file_path}" not found.'
        
        command = [sys.executable, file_path] + args

        completed_process = subprocess.run(
            command,
            cwd=working_directory,
            timeout=30,           # Set a timeout of 30 seconds to prevent infinite execution.
            capture_output=True,  # Capture both stdout and stderr.
            text=True,            # Decode stdout and stderr as text.
            check=False           # Do not raise an exception for non-zero exit codes.
        )
        
        output_parts = []
    
        # Add stdout if it exists
        if completed_process.stdout:
            output_parts.append(f"STDOUT:{completed_process.stdout}")
        
        # Add stderr if it exists
        if completed_process.stderr:
            output_parts.append(f"STDERR:{completed_process.stderr}")

        # If both stdout and stderr are empty, return the specific message
        if not completed_process.stdout and not completed_process.stderr:
            return "No output produced."

        # Add the return code message if the process exited with a non-zero code
        if completed_process.returncode != 0:
            output_parts.append(f"Process exited with code {completed_process.returncode}")

        return "\n".join(output_parts)

    except Exception as e:
        return f'Error: executing Python file: {e}'
