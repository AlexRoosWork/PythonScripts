#!/usr/bin/env python3
# scan a directory and all nested directories. Move all files in new directories named after their suffix

import os
import PyInquirer


def set_start_directory():
    """Ask userinput for path to scan. Return path as string"""
    dir_question = [
        {
            "type": "input",
            "name": "scan_dir",
            "message": "Enter directory to sort all files from: ",
        }
    ]

    answers = PyInquirer.prompt(dir_question)
    answer = answers["scan_dir"].strip()
    return answer


def get_all_files(target_dir):
    """Run through directory. Return list of all extension. Return list of all filepaths."""
    filepaths = []
    for root, dirs, files in os.walk(target_dir):
        for f in files:
            if not f.startswith("."):
                filepaths.append(os.path.join(root, f))

    extensions = []
    for f in filepaths:
        _, ext = os.path.splitext(f)
        if not ext in extensions:
            extensions.append(ext)

    return filepaths, extensions


def create_ext_dirs(scan_dir, extensions):
    """Create a folder in scanned directory for each unique extension"""
    for ext in extensions:
        print(f"Creating {os.path.join(scan_dir, ext[1:])}")
        os.makedirs(os.path.join(scan_dir, ext[1:]), exist_ok=True)
    print(f"Created {len(extensions)} directories")


def move_files(scan_dir, filepaths):
    """Move files to appropriate directory"""
    for f in filepaths:
        _, ext = os.path.splitext(f)
        name = os.path.basename(f)
        new_path = os.path.join(scan_dir, ext[1:], name)
        os.rename(f, new_path)


def main():
    scan_dir = set_start_directory()
    filepaths, extensions = get_all_files(scan_dir)
    create_ext_dirs(scan_dir, extensions)
    move_files(scan_dir, filepaths)
    print("All done")


if __name__ == "__main__":
    main()
