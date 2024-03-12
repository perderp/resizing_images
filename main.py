import os
import argparse
import shutil
from  resizing_images import resize_image

parser = argparse.ArgumentParser(
    description = "Resizing images yo"
)

parser.add_argument(
    "--path",
    type = str,
    default =".",
    help = "Directory path of the file",
)

#parse the arguments given by the user and extract the path
args = parser.parse_args()
path = args.path

print(f"Resizing Images directory {path}")
print(f"Current working directory: {os.getcwd()}")
print(f"Provided path: {path}")
print(''.center(100, "="))

# check if the directory exists
if not os.path.exists(path):
    print(f"Error: Directory '{path}' does not exist.")
    exit(1)

#get all files from given directory
dir_content = os.listdir(path)

#create a relative path from the path to the file and the document name
path_dir_content = [os.path.join(path, doc) for doc in dir_content]

#filter the directory content into a documents and folders list
docs = [doc for doc in path_dir_content if os.path.isfile(doc)]
folders = [folder for folder in path_dir_content if os.path.isdir(folder)]


moved = 0
created_folders = []
no_folders = len(folders)


def main() :
    if len(folders) > 0 :
        process_folder(folders)

    if len(docs) > 0:
        process_docs(docs, folders, path)

def process_folder(the_folder) :
    if the_folder is None :
        return False

    for folder in the_folder :

        new_path_content = os.listdir(folder)
        new_path_dir_content = [os.path.join(folder, doc) for doc in new_path_content]

        #filter if there's another file or folder
        new_docs = [doc for doc in new_path_dir_content if os.path.isfile(doc)]
        new_folder = [folder for folder in new_path_dir_content if os.path.isdir(folder)]

        if len(new_folder) > 0  and "resized_image" not in new_folder:
            process_folder(new_folder)

        process_docs(new_docs, the_folder, folder)


def process_docs(the_doc, the_folder = folders, the_path = path) :
    subfolder_path = os.path.join(the_path, "resized_image")

    for doc in the_doc :
        full_path_doc, file_type = os.path.splitext(doc)
        doc_path = os.path.dirname(full_path_doc)
        doc_name = os.path.basename(full_path_doc)

        # skip this file if when it's in the directory
        if doc_name == "resized_image" or doc_name.startswith('.'):
            continue

        if subfolder_path not in the_folder and subfolder_path not in created_folders and "resized_image" not in doc_name:
            try :
                os.mkdir(subfolder_path)
                created_folders.append(subfolder_path)
                print(f"Folder {subfolder_path} created")
            except FileExistsError as err:
                print(f"Folder already exists at {subfolder_path}... {err}")

        new_doc_path = os.path.join(subfolder_path, doc_name) + file_type

        if file_type.endswith(('jpg', 'png', 'jpeg')):
            shutil.copyfile(doc, new_doc_path)
            resize_image(new_doc_path, output_filename=new_doc_path)
        else:
            continue

if __name__ == "__main__" :
    main()