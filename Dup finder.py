import os
import hashlib
from collections import defaultdict

def get_file_hash(file_path, first_chunk_only=False, chunk_size=1024):
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        if first_chunk_only:
            hasher.update(f.read(chunk_size))
        else:
            for chunk in iter(lambda: f.read(4096), b''):
                hasher.update(chunk)
    return hasher.hexdigest()

def find_duplicates(root_folder, file_types=None):
    files_by_size = defaultdict(list)
    files_by_hash = defaultdict(list)

    # Step 1: Group by size
    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames:
            if file_types and not filename.lower().endswith(tuple(file_types)):
                continue
            file_path = os.path.join(dirpath, filename)
            try:
                size = os.path.getsize(file_path)
                files_by_size[size].append(file_path)
            except Exception as e:
                print(f"Error reading {file_path}: {e}")

    # Step 2: Group by partial hash (first 1KB)
    for size, files in files_by_size.items():
        if len(files) < 2:
            continue
        for file in files:
            try:
                partial_hash = get_file_hash(file, first_chunk_only=True)
                files_by_hash[(size, partial_hash)].append(file)
            except Exception as e:
                print(f"Hashing error: {file} – {e}")

    # Step 3: Verify full content hash
    duplicates = defaultdict(list)
    for group, files in files_by_hash.items():
        if len(files) < 2:
            continue
        full_hashes = defaultdict(list)
        for file in files:
            try:
                full_hash = get_file_hash(file, first_chunk_only=False)
                full_hashes[full_hash].append(file)
            except Exception as e:
                print(f"Full hash error: {file} – {e}")
        for dup_files in full_hashes.values():
            if len(dup_files) > 1:
                duplicates[group] += dup_files

    return duplicates

# Example usage
if __name__ == "__main__":
    root_dir = input("Enter the folder path to scan: ")
    types = input("Enter file types to scan (comma-separated, e.g. .pdf,.docx) or leave blank: ")
    ext_filter = [t.strip() for t in types.split(",")] if types else None
    result = find_duplicates(root_dir, ext_filter)

    print("\n🔍 Duplicate Files Found:\n")
    for group, files in result.items():
        print(f"\n[Group: {group}]")
        for file in files:
            print(f"  - {file}")
