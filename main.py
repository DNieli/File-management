from os import scandir, rename
from os.path import splitext, exists, join
from shutil import move
from time import sleep

import logging

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Fill in with your directory with an existing directory to observe in the 
# format "C:\\Users\\username\\Downloads" on Windows
source_dir = ""

# Fill in with existing destination directories in the same format
destination_dir_images = ""
destination_dir_videos = ""
destination_dir_documents = ""
destination_dir_other = ""

images_extensions = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp",
        ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw", ".k25", ".bmp", ".dib", ".heif",
        ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2",
        ".svg", ".svgz", ".ai", ".eps", ".ico"]

videos_extensions = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg", ".mp4", ".mp4v",
        ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"]

documents_extensions = [".doc", ".docx", ".odt", ".pdf", ".xls", ".xlsx", ".ppt", ".pptx", "txt", "html"]

def make_unique_name(destination, name):
    counter = 1
    filename, extension = splitext(name)
        
    # adds number if file name already exists
    while exists(f"{destination}\\{name}"):
        name = f"{filename}({counter}){extension}"
        counter += 1
        
    return name
            

class FileMoverHandler(FileSystemEventHandler):
    def move_file(self, entry):
        name = entry.name
        filename, extension = splitext(name)
            
        if extension.lower() in images_extensions:
            destination = destination_dir_images
        elif extension.lower() in videos_extensions:
            destination = destination_dir_videos
        elif extension.lower() in documents_extensions:
            destination = destination_dir_documents
        else:
            destination = destination_dir_other
            
        try:
            # checks if the file provided exists
            if exists(f"{destination}\\{name}"):
                rename(join(destination, name), join(destination, make_unique_name(destination, name)))
            move(entry, destination)
            logging.info(f"Moved {name} to {destination}")
        except Exception as e:
            logging.error(f"Error moving file {name}: {e}") 
       
    # runs every time there is a change in the directory in source_dir
    def on_modified(self, event):
        with scandir(source_dir) as entries:
            for entry in entries:
                self.move_file(entry)
           
#Watchdog API
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    event_handler = FileMoverHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    print("observer started")
    try:
        while True:
            sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()