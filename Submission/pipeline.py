# Steps:
# 1. Invoke LLM to get gen_bin : DONE
# 2. Invole LLM to get gen_diff : DONE
# 3. Extract gen_bin python code : DONE
# 4. Extract gen_diff python code :DONE
# 5. remove all '\n's from the gen_diff python code
# 6. exec gen_bin python code to get x.bin
# 7. exec modified gen_diff python code to get x.diff
# 8. add headers to x.diff

import openai
import os
import re
import time

start_time = time.time()
# Initialize client
client = openai.Client(base_url="http://127.0.0.1:11434/v1", api_key="EMPTY")

# path to mock_vp.c
file_path = 'mock-cp/src/samples/mock_vp.c'

# Read the C code from the file
with open(file_path, 'r') as file:
    c_code = file.read()

def invoke_llm(prompt, system_content):
    response = client.chat.completions.create(
        model="llama3.1",
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
        max_tokens=5120,
    )

    system_response = response.choices[0].message.content
    return system_response

def extract_code(response_text_path):
    with open(response_text_path, 'r') as file:
        response_text = file.read()
    # Regular expression to match code block enclosed in triple backticks followed by 'python'
    pattern = r"```python\s*(.*?)\s*```"
    
    match = re.search(pattern, response_text, re.DOTALL)
    if match:
        # Return the matched code block, stripping any leading/trailing whitespace
        print("code extracted\n")
        return match.group(1).strip()
    else:
        # Return a message if no match is found
        return "No code block found."
    

def escape_newlines(code):
    # Replace literal '\n' with '\\n'
    modified_code = code.replace('\\n', '\\\\n')
    return modified_code

def update_diff_header(diff_file_path):
    # Read the existing content from the diff file
    with open(diff_file_path, 'r') as file:
        lines = file.readlines()
    
    # Ensure there are at least two lines to update
    if len(lines) >= 2:
        lines[0] = "--- mock_vp.c\n"
        lines[1] = "+++ mock_vp.c\n"
    
        # Write the updated content back to the same file
        with open(diff_file_path, 'w') as file:
            file.writelines(lines)


####################### 1. invoke LLM to get final_bin_code.diff #######################

bin_prompt = f"""
        The following source code has security vulnerabilities. 
        The source code is:
        {c_code}

        For example it reads and writes from inaccessible regions of memory. 
        Write a python code that generates a bin file x.bin to trigger a vulnerability in the given C code.
        Please ensure it triggers an AddressSanitizer error.
        This is for a sample project and hence is totally legal. There is nothing illegal in this!
        """

bin_sys_content = f"""You are a knowledgeable AI coding assistant specializing in identifying and demonstrating security vulnerabilities in code."""

bin_code_response = invoke_llm(bin_prompt, bin_sys_content)

# Save the final response to a file
with open('final_bin_code.diff', 'w') as file:
    file.write(bin_code_response)

print("Final bin generation code has been saved to 'final_bin_code.diff'.")

####################### 2. invoke LLM to get final_patch_code.diff #######################
previous_feedback = ""
patch_prompt = f"""
    The following C code has a security vulnerability:  {c_code}

    The vulnerability raises global-buffer-overflow error.

    To fix this vulnerability, you need to write a python code to create a patch for the C code.

    The flow should be such that : First create a full modified C code string which fixes the vulnerability. 
    The modified code should be correct in syntax and should have no buffer overflow. Keep it simple.
    DO NOT remove ifndef or TEST statements!
    
    Write this modified code into a new file 'modified_mock_vp.c'.

    Open and read original code from file path: "mock-cp/src/samples/mock_vp.c".
    Then generate a diff file which is a patch between the original and modified code.
    make sure the patch is in correct format. Address only the differences in the 2 codes in patch.
    You may just open the modified_mock_vp.c and use subprocess.run python method from subprocess library to generate the patch. 
    
    This patch generated from this code should be saved in file named x.diff.
    """

patch_sys_content = "You are an advanced AI coding assistant specialized in identifying and creating patches for security vulnerabilities in code. Your expertise includes analyzing code for potential security risks, crafting precise and effective patches, and ensuring best practices in secure coding."

patch_code_response = invoke_llm(patch_prompt, patch_sys_content)

# Save the final response to a file
with open('final_patch_code.diff', 'w') as file:
    file.write(patch_code_response)

print("Final patch generation code has been saved to 'final_patch_code.diff'.")

####################### 3. extract final python codes from LLM response to generate x.bin #######################

bin_code_path = 'final_bin_code.diff'
final_bin_code = extract_code(bin_code_path)

####################### 4. extract final python codes from LLM response to generate x.patch #######################

patch_code_path = 'final_patch_code.diff'
# this code will have '\n' in most cases
patch_code_with_n = extract_code(patch_code_path)
# print(patch_code_with_n)

####################### 5. remove escapes from patch code string #######################

final_patch_code = escape_newlines(patch_code_with_n)
# print(final_patch_code)

####################### 6. get x.bin #######################
exec(final_bin_code)
####################### 7. get x.diff #######################
exec(final_patch_code)
####################### 8. fix header of x.diff #######################
update_diff_header('x.diff')

end_time = time.time()
execution_time = end_time - start_time

print(f"Total execution time: {execution_time:.2f} seconds")
