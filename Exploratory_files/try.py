def generate_code():
    # This function returns a string containing Python code
    code = """
def hello():
    print("Hello, world!")

hello()
"""
    return code

# Get the code from the function
code_to_run = generate_code()

# Execute the code
exec(code_to_run)


import openai
import os

file_path = 'mock-cp/src/samples/mock_vp.c'
prev_run_path = 'x.diff'
prev_err_path = 'prev_err.txt'
prev_code_path = 'gen_diff.py'
# Initialize client
client = openai.Client(base_url="http://127.0.0.1:11434/v1", api_key="EMPTY")

# Read the C code from the file
with open(file_path, 'r') as file:
    c_code = file.read()

with open(prev_run_path, 'r') as file:
    prev_patch = file.read()

with open(prev_err_path, 'r') as file:
    prev_err = file.read()

with open(prev_code_path, 'r') as file:
    prev_code = file.read()

num_iter = 1
previous_feedback = prev_code

for i in range(1, num_iter + 1):
    print("Currently in iteration: ", i)
    prompt = f"""
    The following C code has a security vulnerability:  {c_code}

    The vulnerability is that `func_b()` does not validate the index `j`, allowing access outside the bounds of the `items` array.
    This raises global-buffer-overflow error.

    To fix this vulnerability, you need to  write a python code to create a patch for the C code.

    The code flow shold be such that it first creates a full modified C code  as a string which address the vulnerability. 
    Get original code from file path: 'mock-cp/src/samples/mock_vp.c'
    Then generate a diff file which is a patch between the original and modified code.
    Make sure the patch is in correct format - you may use subprocess.run python method from subprocess library. 
    
    This patch generated from this code should be saved in file named x.diff.
    Keep the code simple and just do the needful.
    Improve on your previously generated code : {previous_feedback}

    """

    response = client.chat.completions.create(
        model="llama3.1",
        messages=[
            {"role": "system", "content": "You are an advanced AI coding assistant specialized in identifying and creating patches for security vulnerabilities in code. Your expertise includes analyzing code for potential security risks, crafting precise and effective patches, and ensuring best practices in secure coding."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.075,
        max_tokens=5120,
    )

    previous_feedback = response.choices[0].message.content
    if i == num_iter:
        answer = previous_feedback



# Optionally, save the final response to a file
with open('final_patch_code.diff', 'w') as file:
    file.write(answer)

print("Final patch has been saved to 'final_patch_code.diff'.")
