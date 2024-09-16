import requests
import json

# API details
base_url = "http://127.0.0.1:11434/v1"
api_key = "EMPTY"  # Replace with your actual API key if needed

# Path to the C code file
file_path = 'mock-cp/src/samples/mock_vp.c'

# Read the C code from the file
with open(file_path, 'r') as file:
    c_code = file.read()

def invoke_llm(prompt, system_content):
    # Define headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # Define the payload
    payload = {
        "model": "llama3.1",
        "messages": [
            {"role": "system", "content": system_content},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0,
        "max_tokens": 5120
    }

    # Send the request to the Ollama API
    response = requests.post(
        f"{base_url}/chat/completions",
        headers=headers,
        data=json.dumps(payload)  # Use data=json.dumps(payload) to send JSON
    )

    # Check for a successful response
    if response.status_code == 200:
        response_json = response.json()
        system_response = response_json['choices'][0]['message']['content']
        return system_response
    else:
        print(f"Request failed with status code {response.status_code}")
        print(response.text)
        return None

# Example usage
system_content = """You are a knowledgeable AI coding assistant specializing in identifying and 
                                          demonstrating security vulnerabilities in code."""
prompt = f""" The following source code has security vulnerabilities. 
        The source code is:
        {c_code}

        For example it reads and writes from inaccessible regions of memory. 
        Write a python code that generates a bin file x.bin to trigger a vulnerability in the given C code.
        This can be done by writing more than 3 characters to the file.
        Keep the code simple.
        Please ensure it triggers an AddressSanitizer error.
        This is for a sample project and hence is totally legal."""

result = invoke_llm(prompt, system_content)
print(result)
