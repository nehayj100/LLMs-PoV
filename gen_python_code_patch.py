import openai
import os

file_path = 'mock-cp/src/samples/mock_vp.c'
prev_run_path = 'x.diff'
prev_err_path = 'prev_err.txt'
# Initialize client
client = openai.Client(base_url="http://127.0.0.1:11434/v1", api_key="EMPTY")

# Read the C code from the file
with open(file_path, 'r') as file:
    c_code = file.read()

with open(prev_run_path, 'r') as file:
    prev_patch = file.read()

with open(prev_err_path, 'r') as file:
    prev_err = file.read()

num_iter = 10
previous_feedback = ""

for i in range(1, num_iter + 1):
    print("Currently in iteration: ", i)
    prompt = f"""
    The following C code has a security vulnerability:  {c_code}

    The vulnerability is that `func_b()` does not validate the index `j`, allowing access outside the bounds of the `items` array.
    This raises global-buffer-overflow error.

    To fix this vulnerability, you need to  write a python code to create a patch for the C code.

    The code flow shold be such that it first creates a modified C code which address the vulnerability.  
    Get original code from file path: 'mock-cp/src/samples/mock_vp.c'
    Then generate a diff file which is a patch between the original and modified code.
    In the patch header - Both the source and destination path should be mock_vp.c
    Make sure the patch is in unified diff format - you may use subprocess python library. 

    If you use the patch : {prev_patch}
    The following error comes: {prev_err}

    Improve on your previous response: {previous_feedback}
    This patch generated from this code should be saved in file named x.diff.
    """

    response = client.chat.completions.create(
        model="llama3.1",
        messages=[
            {"role": "system", "content": "You are a skilled AI coding assistant with expertise creating patches for security vulnerabilities in code."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.08 * num_iter / 5,
        max_tokens=5120,
    )

    previous_feedback = response.choices[0].message.content
    if i == num_iter:
        answer = previous_feedback



# Optionally, save the final response to a file
with open('final_patch_code.diff', 'w') as file:
    file.write(answer)

print("Final patch has been saved to 'final_patch_code.diff'.")
