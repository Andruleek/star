import os
import shutil
from pathlib import Path
import zipfile

def normalize(file_extension):
    image_extensions = ('.JPEG', '.PNG', '.JPG', '.SVG')
    video_extensions = ('.AVI', '.MP4', '.MOV', '.MKV')
    document_extensions = ('.DOC', '.DOCX', '.TXT', '.PDF', '.XLSX', '.PPTX')
    music_extensions = ('.MP3', '.OGG', '.WAV', '.AMR')
    archive_extensions = ('.ZIP', '.GZ', '.TAR')

    if file_extension.upper() in image_extensions:
        return 'Images'
    elif file_extension.upper() in video_extensions:
        return 'Videos'
    elif file_extension.upper() in document_extensions:
        return 'Documents'
    elif file_extension.upper() in music_extensions:
        return 'Music'
    elif file_extension.upper() in archive_extensions:
        return 'Archives'
    else:
        return 'Unknown'

def sort_files(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        if os.path.isfile(file_path):
            _, file_extension = os.path.splitext(filename)
            destination_folder = normalize(file_extension)
            
            if not os.path.exists(destination_folder):
                os.makedirs(destination_folder)
            
            destination_path = os.path.join(destination_folder, filename)
            shutil.move(file_path, destination_path)

        elif os.path.isdir(file_path):
            if filename.lower() not in ['archives', 'video', 'audio', 'documents', 'images', 'others']:
                sort_files(file_path)
                if not os.listdir(file_path):
                    os.rmdir(file_path)

            elif filename.lower() == 'archives':
                extract_archives(file_path)

def extract_archives(archive_folder):
    for archive_filename in os.listdir(archive_folder):
        archive_path = os.path.join(archive_folder, archive_filename)
        if os.path.isfile(archive_path):
            _, archive_extension = os.path.splitext(archive_filename)
            if archive_extension.upper() in ('.ZIP', '.GZ', '.TAR'):
                extract_folder = os.path.join(archive_folder, normalize(archive_extension))
                with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                    try:
                        zip_ref.extractall(extract_folder)
                    except zipfile.BadZipFile:
                        print(f"Failed to extract {archive_filename}. Removing...")
                        os.remove(archive_path)

if __name__ == "__main__":
    folder_path = input("Enter the folder path: ")
    sort_files(folder_path)
    print("Files sorted successfully.")
