
import shutil
import os

source_file = "sample.txt"
backup_file = "sample_backup.txt"
copy_file = "sample_copy.txt"

shutil.copy(source_file, copy_file)
print(f"File copied to {copy_file}")

shutil.copy(source_file, backup_file)
print(f"Backup created as {backup_file}")

def safe_delete(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"{file_path} deleted successfully.")
    else:
        print(f"{file_path} does not exist.")

safe_delete(copy_file)