import difflib

def generate_patch(original_code, patched_code):
    # Split the original and patched code into lines
    original_lines = original_code.split('\n')
    patched_lines = patched_code.split('\n')

    # Use difflib to generate a unified diff between the two versions of the code
    patch = difflib.unified_diff(original_lines, patched_lines, 'x.diff', 'Patch for global-buffer-overflow vulnerability in func_b()')

    return '\n'.join(patch)

# Original C code (without bounds checking)
original_code = """
#include <stdio.h>
#include <string.h>
#include <unistd.h>

char items[3][10];

void func_a(){
    char* buff;
    int i = 0;
    do{
        printf("input item:");
        buff = &items[i][0];
        i++;
        fgets(buff, 40, stdin);
        buff[strcspn(buff, "\n")] = 0;
    }while(strlen(buff) != 0);
    i--;
}

void func_b(){
    char *buff;
    printf("done adding items\n");
    int j;
    printf("display item #: ");
    scanf("%d", &j);
    buff = &items[j][0];
    printf("item %d: %s\n", j, buff);
}

#ifndef ___TEST___
int main()
{
    func_a();
    func_b();
    return 0;
}
#endif
"""

# Patched C code (with bounds checking)
patched_code = """
#include <stdio.h>
#include <string.h>
#include <unistd.h>

char items[3][10];

void func_a(){
    char* buff;
    int i = 0;
    do{
        printf("input item:");
        buff = &items[i][0];
        i++;
        fgets(buff, 40, stdin);
        buff[strcspn(buff, "\n")] = 0;
    }while(strlen(buff) != 0);
    i--;
}

void func_b(){
    char *buff;
    printf("done adding items\n");
    int j;
    printf("display item #: ");
    scanf("%d", &j);

    // Add bounds checking
    if (j < 0 || j >= 3) {
        printf("Error: Invalid item index. Please enter a value between 0 and 2.\n");
        return;
    }

    buff = &items[j][0];
    printf("item %d: %s\n", j, buff);
}

#ifndef ___TEST___
int main()
{
    func_a();
    func_b();
    return 0;
}
#endif
"""

# Generate the patch file (x.diff)
patch = generate_patch(original_code, patched_code)

with open('x.diff', 'w') as f:
    # Add a header to the patch file with a clear description of the changes
    # f.write("Patch for global-buffer-overflow vulnerability in func_b()\n")
    # f.write("--------------------------------------------------------\n\n")

    # Write the unified diff to the patch file
    f.write(patch + '\n')


    