
import os
import shutil

source_dir = os.path.join("project", "data", "files")
destination_dir = os.path.join("project", "backup")

os.makedirs(destination_dir, exist_ok=True)


files = os.listdir(source_dir)

for file in files:
    source_path = os.path.join(source_dir, file)

    copy_path = os.path.join(destination_dir, f"copy_{file}")
    shutil.copy(source_path, copy_path)
    print(f"Copied: {file} → {copy_path}")

    move_path = os.path.join(destination_dir, f"moved_{file}")
    shutil.move(source_path, move_path)
    print(f"Moved: {file} → {move_path}")
