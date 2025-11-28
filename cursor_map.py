#!/usr/bin/env python3

import os
import shutil
import argparse

def no_file_extension(str):
    return os.path.splitext(str)[0]

def get_file_list(folder_path):
    #return [no_file_extension(f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    return [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

def load_mappings(mappings_file):
    mappings = {}
    if not os.path.exists(mappings_file):
        print(f"Error: Mappings file '{mappings_file}' not found.")
        exit(1)

    with open(mappings_file, "r") as file:
        for line in file:

            try:
                [key, value] = line.split(sep="=")
            except ValueError:  # empty line
                continue

            key = key.strip()
            value = value.replace(" ", "").replace("\n","").split(sep=",")

            mappings[key] = value

    return mappings

def build_main_dictionary(file_list, template_mappings):
    dictionary = {}
    for file in file_list:
        try:
            dictionary[file] = template_mappings[file]
        except KeyError:
            pass

    return dictionary

def main():
    parser = argparse.ArgumentParser(description="Convert Windows cursor files to a Linux Icon Theme.")

    parser.add_argument("-i", "--input", required=True, help="Input folder containing Windows cursor files")
    parser.add_argument("-o", "--output", required=True, help="Output folder for the converted theme")
    parser.add_argument("-n", "--name", required=True, help="Name of the cursor pack (internal theme name)")
    parser.add_argument("-m", "--mappings",
                    default=os.getenv("CURSOR_WIN2LIN_MAPPINGS", "mappings.txt"),
                    help="Path to the mappings file (default: mappings.txt)")

    args = parser.parse_args()

    input_folder = os.path.abspath(args.input)
    output_folder = os.path.abspath(args.output)
    mappings_file = os.path.abspath(args.mappings)
    cursor_name = args.name

    if not os.path.exists(input_folder):
        print(f"Error: Input directory '{input_folder}' does not exist.")
        exit(1)

    input_files = get_file_list(input_folder)
    template_mappings = load_mappings(mappings_file)
    current_mappings = build_main_dictionary(input_files, template_mappings)

    cursor_dest_folder = os.path.join(output_folder, "cursors")

    if not os.path.exists(cursor_dest_folder):
        try:
            os.makedirs(cursor_dest_folder)
        except OSError as e:
            print(f"Error: Failed to create directory {cursor_dest_folder}. {e.strerror}")
            exit(1)

    for key, value in current_mappings.items():
        if value != "-" and value[0] != "-":

            win_name = key

            for xcur_name in value:
                src = os.path.join(input_folder, win_name)
                dst = os.path.join(cursor_dest_folder, xcur_name)
                shutil.copy2(src, dst)

            if input_folder == output_folder:
                os.remove(os.path.join(input_folder, win_name))

    with open(os.path.join(output_folder, "index.theme"), "w") as index:
        index.writelines(["[Icon Theme]\n", f"Name={cursor_name}\n"])

    with open(os.path.join(output_folder, "cursor.theme"), "w") as index:
        index.writelines(["[Icon Theme]\n", f"Inherits={cursor_name}\n"])

if __name__ == "__main__":
    main()