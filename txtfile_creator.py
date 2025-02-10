def create_large_text_file(size_in_mb=3, filename="large_file.txt"):
    size_in_bytes = size_in_mb * 1024 * 1024  # Convert MB to bytes
    text = "ABCD" * 512 #Each line is 1KB (1024 bytes)

    with open(filename, "w") as file:
        for _ in range(size_in_bytes // 2048):  # Write enough lines to reach 3MB
            file.write(text + "\n")

    print(f"{filename} created successfully with size {size_in_mb}MB.")
