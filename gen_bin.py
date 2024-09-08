# Generate a file x.bin containing the malicious payload
with open("x.bin", "wb") as f:
    # Write the string "exploited" to the file, followed by a null terminator
    f.write(b"exploited\0")
    
print("Generated x.bin file for demonstration purposes.")