import openai

# Initialize client
client = openai.Client(base_url="http://127.0.0.1:11434/v1", api_key="EMPTY")

def generate_prompt(iteration, previous_response=None):
    # Escape curly braces and other special characters
    escaped_code = """
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
        buff[strcspn(buff, "\\n")] = 0;
    }while(strlen(buff) != 0);
    i--;
}

void func_b(){
    char *buff;
    printf("done adding items\\n");
    int j;
    printf("display item #: ");
    scanf("%d", &j);
    buff = &items[j][0];
    printf("item %d: %s\\n", j, buff);
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

    if previous_response:
        feedback = f"\nFeedback on previous iteration: {previous_response}\n"
    else:
        feedback = ""
    
    return f"""
    You are a skilled AI coding assistant with expertise in identifying and patching security vulnerabilities in code. 

    The following C code has a security vulnerability that leads to a global-buffer-overflow error. We have created a file `x.bin` that triggers this overflow, detectable by tools like AddressSanitizer. The vulnerability is that `func_b()` does not validate the index `j`, allowing access outside the bounds of the `items` array.

    The C code is:

    {escaped_code}

    To fix this vulnerability and prevent the global-buffer-overflow error, you need to create a Python script that generates a patch for the C code. The patch should:

    1. **Do Bounds Checking**: Ensure that `func_b()` does not attempt to access memory outside the bounds of the `items` array.

    Please write a Python script that:
    - Generates a patch file named `x.diff` that modifies the C code to include the necessary input validation and bounds checking.
    - Includes clear comments in the script explaining how the patch fixes the global-buffer-overflow vulnerability and ensures that the code is safe from such issues.
    - Do not have any patch segments without a header
    Please address the above issues improving on previous feedback:
    {feedback}

    Make sure `x.diff` is in a valid unified diff format and can be applied to the original C code to address the vulnerability effectively.
    
    Iteration: {iteration}
    """

def generate_patch(iteration, previous_response=None):
    prompt = generate_prompt(iteration, previous_response)
    
    response = client.chat.completions.create(
        model="llama3.1",
        messages=[
            {"role": "system", "content": "You are a skilled AI coding assistant with expertise in identifying and patching security vulnerabilities in code."},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
        max_tokens=5120,
    )
    
    answer = response.choices[0].message.content
    print(f"Iteration {iteration}\n")
    return answer

# Perform iterations
previous_response = None
final_response = None
for i in range(1, 2):
    final_response = generate_patch(i, previous_response)
    previous_response = final_response  # Pass the latest response as feedback for the next iteration

print(f"Final Response from Iteration 10:\n{final_response}\n")

# Optionally, save the final response to a file
with open('final_patch.diff', 'w') as file:
    file.write(final_response)

print("Final patch has been saved to 'final_patch.diff'.")
