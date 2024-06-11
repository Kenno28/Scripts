import os
import time
import shutil

download_folder = os.path.expanduser('~/Downloads')
pdf_folder = os.path.expanduser('~/Downloads/PDFs')
image_folder = os.path.expanduser('~/Downloads/Images')
archive_folder = os.path.expanduser('~/Downloads/Archives')


if not os.path.exists(pdf_folder):
    os.makedirs(pdf_folder)

if not os.path.exists(image_folder):
    os.makedirs(image_folder)

if not os.path.exists(archive_folder):
    os.makedirs(archive_folder)

def move_files():
    for filename in os.listdir(download_folder):
        if filename.endswith('.pdf'):
            source = os.path.join(download_folder, filename)
            destination = os.path.join(pdf_folder, filename)
            shutil.move(source, destination)
            print(f"Verschoben: {filename}")
        elif filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.jpeg'):
            source = os.path.join(download_folder, filename)
            destination = os.path.join(image_folder, filename)
            shutil.move(source, destination)
            print(f"Verschoben: {filename}")
        elif filename.endswith('.zip'):
            source = os.path.join(download_folder, filename)
            destination = os.path.join(archive_folder, filename)
            shutil.move(source, destination)
            print(f"Verschoben: {filename}")

if __name__ == "__main__":
    print("Überwachung des Download-Ordners gestartet...")
    while True:
        move_files()
        time.sleep(10) 