import os
import sys
import argparse
from dotenv import load_dotenv # pyright: ignore[reportMissingImports]

from google import genai
from google.genai import types # pyright: ignore[reportMissingImports]

from functions.get_files_info import available_functions

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser()
parser.add_argument("user_prompt", type=str, help="The user's prompt")
parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

def main():
    try:
        user_prompt = args.user_prompt

        messages = [
            types.Content(role="user", parts=[types.Part(text=user_prompt)])
        ]
    except Exception as e:
        print(e)
        sys.exit(1)

    system_prompt = """
        You are a helpful AI coding agent.

        When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

        - List files and directories

        All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    response = client.models.generate_content(
        model = "gemini-2.0-flash-001",
        contents = messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],system_instruction=system_prompt
        )
    )

    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

    if args.verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")
    
    if response.function_calls:
        for call in response.function_calls:
            print(f"Calling function: {call.name}({call.args})")
    else:
        print(response.text)
    


if __name__ == "__main__":
    main()
