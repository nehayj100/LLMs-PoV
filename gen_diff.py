import subprocess

# Original and modified file paths
original_file = 'mock-cp/src/samples/mock_vp.c'
modified_file = 'mock-cp/src/samples/mock_vp_modified.c'

# Function to generate modified C code
def modify_code(original_file):
    with open(original_file, 'r') as f:
        lines = f.readlines()

    # Add validation for index j in func_b()
    modified_lines = []
    for i, line in enumerate(lines):
        if "func_b()" in line and not any("if" in modified_lines[-1] for modified_lines[-1] in modified_lines):
            modified_lines.append('    if (j >= 0 && j < 3) {\n')
        elif "buff = &items[j][0];" in line:
            modified_lines.append('        } else {\n')
            modified_lines.append('            printf("Invalid item number\\n");\n')
            modified_lines.append('            return;\n')
            modified_lines.append('        }\n')
        modified_lines.append(line)

    with open(modified_file, 'w') as f:
        f.writelines(modified_lines)


# Generate modified C code
modify_code(original_file)

# Create a diff file (patch) between the original and modified code
subprocess.run(['diff', '-u', original_file, modified_file], stdout=open('x.diff', 'w'))