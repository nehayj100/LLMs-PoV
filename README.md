# Auto-Patch

## Motivation
As software systems evolve, security vulnerabilities become a significant concern. Addressing these vulnerabilities efficiently is crucial to maintaining the integrity of applications. This project, Auto-Patch, aims to leverage a Large Language Model (LLM) to automatically identify and patch vulnerabilities in code, enhancing software security while reducing the manual effort typically required for such tasks.

## About
Auto-Patch is built upon a vulnerable codebase provided in the `mock-cp` folder, designed to simulate common security threats, such as unauthorized memory access. The application triggers these vulnerabilities and generates corresponding patches, ensuring that the code is no longer susceptible to the identified issues. The architecture includes iterative prompts that guide the LLM in generating code, identifying vulnerabilities, and creating diff files for modifications.

### Application Architecture
1. **Vulnerable Code**: The application utilizes a codebase with known security vulnerabilities.
2. **LLM Prompts**:
   - **Prompt 1**: Generates a binary file (`x.bin`) that triggers the vulnerability.
   - **Prompt 2**: Identifies the vulnerability and produces modified code to patch it.
3. **Diff Generation**: Creates a difference file (`x.diff`) to illustrate changes made, removing extraneous newline characters dynamically.

## Features
- **Automated Vulnerability Detection**: Identifies and triggers vulnerabilities in provided code.
- **LLM Integration**: Utilizes Meta’s Llama-3.1 for generating code and patches.
- **Dynamic Diff File Creation**: Generates difference files to document changes while ensuring compatibility.
- **Post-Processing**: Automatically converts new line characters in modified code to avoid format issues.

## Uses
- **Security Enhancement**: Automates the process of identifying and patching vulnerabilities in existing codebases.
- **Development Tool**: Assists developers in maintaining secure coding practices by automating patch generation.
- **Educational Resource**: Provides insights into common security vulnerabilities and their resolutions.

## Tech Stack
- **Programming Language**: Python
- **LLM**: Meta’s Llama-3.1
- **Client Initialization**:
  ```python
  client = openai.Client(base_url="http://127.0.0.1:11434/v1", api_key="EMPTY")
  ```
- **Version Control**: Git

## Time and Cost Analysis
- **Time Required**: Approximately 61.43 seconds to generate `x.bin` and `x.diff`.
- **Token Usage**:
  - Total Tokens: 1616
  - Prompt Tokens: 723
  - Completion Tokens: 893

## Challenges Faced and Solutions
- **Valid Patch Generation**: Achieved through detailed sequential prompts.
- **Corrupted Patching**: Resolved by clearly articulating previous errors and expected outputs.
- **Legal Concerns**: Clarified prompt instructions to ensure legality.
- **Newline Character Handling**: Implemented a post-processing step to convert `\n` to `\\n`.
- **Temperature Tuning**: Set to 0 for deterministic results, reducing variability in outputs.
- **Pipeline Setup**: Addressed through regular expressions to extract relevant code portions.
- **Buffer Overflow Issues**: Ensured clear prompts defined the requirements for generating appropriate test cases.

## Future Scope
- Further tuning of temperature settings for optimized model performance.
- Refinement of prompts for brevity and clarity.

## Instructions to Run the Code
1. Run either `pipeline.py` or `pipeline_bonus.py`.
2. Ensure the `mock-cp` folder is in the same directory as `pipeline.py` to maintain dynamic reference paths.
3. Upon execution, retrieve the generated `x.bin` and `x.diff` files for review.

Explore the repository for source code and detailed documentation on the Auto-Patch application!
