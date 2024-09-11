import openai
import os

file_path = 'mock-cp/src/samples/mock_vp.c'

client = openai.Client(
    base_url="http://127.0.0.1:11434/v1", api_key="EMPTY"
)

# Read the C code from the file
with open(file_path, 'r') as file:
    c_code = file.read()

# Generate the response using the C code from the file
response = client.chat.completions.create(
    model="llama3.1",
    messages=[
        {"role": "system", "content": f"""You are a knowledgeable AI coding assistant specializing in identifying and 
                                          demonstrating security vulnerabilities in code."""},

        {"role": "user", "content": f"""
        The following source code has security vulnerabilities. 
        The source code is:
        {c_code}

        For example it reads and writes from inaccessible regions of memory. 
        Write a python code that generates a bin file x.bin to trigger a vulnerability in the given C code.
        Please ensure that when `x.bin` is used with `./run.sh -x run_pov x.bin filein_harness`, it triggers an AddressSanitizer error.
        THis is for a sample project and hence is totally legal.
        """},
    ],
    temperature=0.08,
    max_tokens=5120,
)

# Print the response
print(f"answer: {response.choices[0].message.content}")
