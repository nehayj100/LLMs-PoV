import openai
import os

file_path = 'mock-cp/src/samples/mock_vp.c'

# Initialize client
client = openai.Client(base_url="http://127.0.0.1:11434/v1", api_key="EMPTY")

# Read the C code from the file
with open(file_path, 'r') as file:
    c_code = file.read()

prompt = f"""
The following C code has a security vulnerability:  {c_code}

The vulnerability is that `func_b()` does not validate the index `j`, allowing access outside the bounds of the `items` array.
This raises global-buffer-overflow error.

To fix this vulnerability, you need to  write a python code to create a patch for the C code.

The code flow shold be such that it first creates a modified C code and then generates a diff file which is a patch between the original and modified code.
Get original code from file path: 'mock-cp/src/samples/mock_vp.c'
Both the source and destination in patch header should be mock_vp.c
Make sure the patch is in unified diff format. Do not skip any line of character from original code.
Do not take extra spaces or new lin characters!
This patch that will be generated from this code should be named x.diff.
"""


response = client.chat.completions.create(
    model="llama3.1",
    messages=[
        {"role": "system", "content": "You are a skilled AI coding assistant with expertise creating patches for security vulnerabilities in code."},
        {"role": "user", "content": prompt},
    ],
    temperature=0,
    max_tokens=5120,
)

answer = response.choices[0].message.content



# Optionally, save the final response to a file
with open('final_patch_code.diff', 'w') as file:
    file.write(answer)

print("Final patch has been saved to 'final_patch.diff'.")
