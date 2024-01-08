from pathlib import Path
import shutil

# Визначення категорій файлів і шляху до папки
file_categories = {
    'images': ('JPEG', 'PNG', 'JPG', 'SVG'),
    'videos': ('AVI', 'MP4', 'MOV', 'MKV'),
    'documents': ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'),
    'music': ('MP3', 'OGG', 'WAV', 'AMR'),
    'archives': ('ZIP', 'GZ', 'TAR'),
    'unknown': ()
}

# Введіть назву папки яку потрібно посортувати
folder_path = Path('')

# Функція для сортування файлів
def sort(path, root_folder):
    folder_path = Path(path)
    for file_path in folder_path.iterdir():
        if file_path.is_file():
            extension = file_path.suffix[1:].upper()
            moved = False
            for category, extensions in file_categories.items():
                if extension in extensions:
                    shutil.move(str(file_path), str(root_folder / category / file_path.name))
                    moved = True
                    break
            if not moved:
                shutil.move(str(file_path), str(root_folder / 'unknown' / file_path.name))
        else:
            sort(file_path, root_folder)

# Створення папок для кожної категорії, якщо вони ще не існують
for category in file_categories.keys():
    (folder_path / category).mkdir(exist_ok=True)

# Виклик функції сортування
sort(folder_path, folder_path)

print("Сортування завершено!")
