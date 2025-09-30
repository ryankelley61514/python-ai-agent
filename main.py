import os
import sys
import argparse
from dotenv import load_dotenv # pyright: ignore[reportMissingImports]

from google import genai
from google.genai import types # pyright: ignore[reportMissingImports]

from functions.schema_functions import available_functions
from functions.call_function import call_function
from functions.config import MAX_ITERS

from prompts import system_prompt

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser()
    parser.add_argument("user_prompt", type=str, help="The user's prompt")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    
    user_prompt = args.user_prompt

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    verbose = args.verbose
    iters = 0
    while True:
        iters += 1
        if iters > MAX_ITERS:
            print(f"Maximum iterations ({MAX_ITERS}) reached.")
            sys.exit(1)

        try:
            final_response = generate_content(client, messages, verbose)
            if final_response:
                print("Final response:")
                print(final_response)
                break
        except Exception as e:
            print(f"Error in generate_content: {e}")

def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model = "gemini-2.0-flash-001",
        contents = messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],system_instruction=system_prompt
        )
    )

    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

    if verbose:
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")

    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)
    
    if not response.function_calls:
        return response.text

    function_responses = []
    for call in response.function_calls:
        function_call_result = call_function(call, verbose)
        if not function_call_result.parts or not function_call_result.parts[0].function_response.response:
            raise Exception("Error: Fatal error of some sort.")
        
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
            
        function_responses.append(function_call_result.parts[0])

    if not function_responses:
        raise Exception("no function responses generated, exiting.")
        
    messages.append(
        types.Content(
            role="user",
            parts=function_responses,
        )
    )

if __name__ == "__main__":
    main()
