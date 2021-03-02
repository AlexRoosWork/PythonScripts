#!/usr/bin/env python3

# given a directory, go through it and its nested dirs to delete all .txt files

import os


def main():
    print(f"Delete all text files in the given directory\n")
    path = input("Input the basedir:\n")
    to_be_deleted = []
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            if filename.endswith(".txt"):
                string = dirpath + os.sep + filename
                to_be_deleted.append(string)
    num_of_files = len(to_be_deleted)
    if input(f"sure you want to delete {num_of_files} .txt files? (y/n)") == "y":
        for file in to_be_deleted:
            os.remove(file)
        print("Done.")
    else:
        print("Abortion.")


if __name__ == "__main__":
    main()
