# Steps:
# 1. Invoke LLM to get gen_bin
# 2. Extract gen_bin python code
# 3. exec gen_bin python code to get x.bin
# 4. Invole LLM to get gen_diff
# 5. Extract gen_diff python code
# 6. remove all '\n's from the gen_diff python code
# 7. exec modified gen_diff python code to get x.diff
# 8. add headers to x.diff

