

import os


base_dir = "project"
nested_dir = os.path.join(base_dir, "data", "files")

os.makedirs(nested_dir, exist_ok=True)
print(f"Nested directories created: {nested_dir}")


sample_files = ["file1.txt", "file2.txt", "image.png", "doc.pdf"]

for file in sample_files:
    file_path = os.path.join(nested_dir, file)
    with open(file_path, "w") as f:
        f.write(f"Sample content for {file}")

print("Sample files created.")


print("\nListing all directories and files:")
for root, dirs, files in os.walk(base_dir):
    print(f"\nDirectory: {root}")
    print(" Subdirectories:", dirs)
    print(" Files:", files)


def find_files_by_extension(directory, extension):
    matches = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                matches.append(os.path.join(root, file))
    return matches

txt_files = find_files_by_extension(base_dir, ".txt")

print("\nFound .txt files:")
for file in txt_files:
    print(file)