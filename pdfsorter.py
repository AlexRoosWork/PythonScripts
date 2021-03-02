#!/usr/bin/env python3

import os, random, subprocess, threading
import PyInquirer


# list program to open pdfs with
PDF_READER = "/usr/bin/okular"

# destination basedir
BASE_DIR = "/home/alex/Documents/"


def walk_flag():
    """Ask the user if nested dirs should be scanned as well. Return bool"""
    question = [
        {
            "type": "confirm",
            "name": "walk_flag",
            "message": "Scan nested directories: ",
            "default": False,
        }
    ]
    answers = PyInquirer.prompt(question)
    answer = answers["walk_flag"]
    return answer


def choose_directory():
    """Choose a directory to go through all pdfs. Returns dirpath"""

    questions = [
        {
            "type": "input",
            "name": "origin_dir",
            "message": "enter directory to sift through: ",
        }
    ]

    answers = PyInquirer.prompt(questions)
    answer = answers["origin_dir"].strip()
    if answer.startswith("/"):
        return answer
    else:
        return f"/home/alex/{answer}"


def get_pdf_files(directory, walk_flag):
    # create list of all pdfs
    pdfs = []
    candidates = []
    if walk_flag:
        for root, dirs, files in os.walk(directory):
            for name in files:
                if not name.startswith("."):
                    candidates.append(os.path.join(root, name))
    else:
        candidates = os.listdir(directory)  # get all files from dr
    for f in candidates:
        _, ext = os.path.splitext(f)
        if ext.lower() == ".pdf":
            if not f.startswith("."):
                pdfs.append(os.path.join(directory, f))
    return pdfs


def open_pdf(f):
    """Open a given pdf file"""
    # command = f"{PDF_READER} {f}"
    command = [PDF_READER, f]
    return subprocess.Popen(command)


def close_pdf(process):
    process.terminate()


def give_filename():
    name = input("Enter a new name for the pdf: ")
    return name


def dir_menu():
    """Display menu of possible destinations. Return new path."""
    years = [
        "2021",
        "2020",
        "2019",
        "2018",
        "2017",
        "2016",
        "2015",
        "2014",
        "2013",
        "2012",
        "2011",
        "2010",
        "2009",
        "2008",
    ]

    questions = [
        {
            "type": "list",
            "name": "target_dir",
            "message": "Choose document year",
            "choices": years,
            "default": years[1],
        }
    ]

    answers = PyInquirer.prompt(questions)
    return answers["target_dir"]


def main():
    """Run the programm"""

    # choose directory to search
    origin_dir = choose_directory()
    flag = walk_flag()
    pdfs = get_pdf_files(origin_dir, flag)

    # loop through all files in directory
    for pdf in pdfs:
        # open the pdf in reader
        process = open_pdf(pdf)

        # Prepare dir + rename the file
        name = f"{give_filename()}.pdf"
        chosen_year = dir_menu()  # already a string
        destination = os.path.join(BASE_DIR, chosen_year, name)

        os.rename(pdf, destination)

        # close pdf
        close_pdf(process)

    input("All done! See you soon.")


if __name__ == "__main__":
    main()
