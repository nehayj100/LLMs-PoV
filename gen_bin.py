import struct

# Create a binary file with a long string
with open("x.bin", "wb") as f:
    # Write a string longer than 10 characters (the size of each item array)
    s = b"A" * 20 + b"B"
    f.write(s)

print("Binary file x.bin generated")