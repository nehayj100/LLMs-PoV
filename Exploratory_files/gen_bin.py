# import struct

# # Create a binary file with a long string
# with open("x.bin", "wb") as f:
#     # Write a string longer than 10 characters (the size of each item array)
#     s = b"A" * 20 + b"B"
#     f.write(s)

# print("Binary file x.bin generated")

import struct

# Define the structure of the binary data
data = b"Hello, World!" * 10  # More than 3 characters!

# Write the binary data to a file called x.bin
with open("x.bin", "wb") as f:
    f.write(data)