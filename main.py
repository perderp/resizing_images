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

#print(f"DOCUMENTS : {docs}")
#print(f"FOLDERS : {folders}")
#print(path_dir_content)

# go through all files and move them into according folders
if len(folders) > 0 :
    for folder in folders :
        #connecting the filepath in order to create the new folder
        subfolder_path = os.path.join(folder, 'resized_image')


        folder_content = os.listdir(folder)
        new_docs = [os.path.join(folder, doc) for doc in folder_content if os.path.isfile(os.path.join(folder, doc))]

        for new_doc in new_docs :
            full_path_doc, file_type = os.path.splitext(new_doc)
            doc_path = os.path.dirname(full_path_doc)
            doc_name = os.path.basename(full_path_doc)

            if doc_name == "resized_image" or doc_name.startswith('.'):
                continue

            if subfolder_path not in folder and subfolder_path not in created_folders:
                #create the folder here
                try :
                    os.mkdir(subfolder_path)
                    created_folders.append(subfolder_path)
                    print(f"Folder {subfolder_path} created")
                except FileExistsError as err:
                    print(f"Folder already exists at {subfolder_path}... {err}")

            # get the new folder and copy the file
            new_doc_path = os.path.join(subfolder_path, doc_name) + file_type

            if file_type.endswith(('jpg', 'png', 'jpeg')):
                shutil.copyfile(new_doc, new_doc_path)
                resize_image(new_doc_path, output_filename=new_doc_path)
            else:
                continue

if len(docs) > 0:
    for doc in docs:
        full_path_doc, file_type = os.path.splitext(doc)
        doc_path = os.path.dirname(full_path_doc)
        doc_name = os.path.basename(full_path_doc)

        # skip this file when its in the directory
        if doc_name == "resized_image" or doc_name.startswith('.'):
            continue

        # get the subfolder name and create folder if not exist
        subfolder_path = os.path.join(path, 'resized_image')

        if subfolder_path not in folders and subfolder_path not in created_folders:
            #create the folder
            try:
                os.mkdir(subfolder_path)
                created_folders.append(subfolder_path)
                print(f"Folder {subfolder_path} created")
            except FileExistsError as err:
                print(f"Folder already exists at {subfolder_path}... {err}")
        #get the new folder and copy the file
        new_doc_path = os.path.join(subfolder_path, doc_name) + file_type

        #print(file_type)

        if file_type.endswith(('jpg', 'png', 'jpeg')):
            shutil.copyfile(doc, new_doc_path)
            resize_image(new_doc_path, output_filename=new_doc_path)

        else:
            continue