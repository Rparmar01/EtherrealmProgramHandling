import os
import time
import traceback

class FileModified():
    def __init__(self, file_path, callback):
        self.file_path = file_path
        self.callback = callback
        self.modifiedOn = os.path.getmtime(file_path)
    
    def start(self):
        try:
            while (True):
                time.sleep(0.5)
                modified = os.path.getmtime(self.file_path)
                if modified != self.modifiedOn:
                    self.modifiedOn = modified
                    if self.callback():
                        break
        except Exception as e:
            print(f'Error reading the file: {e}')
        except KeyboardInterrupt:
            print("Stopping observer...")


def file_modified():
    with open('sample_text_input.txt', 'r'  ) as f:
        lines = f.read()
        print("File Modified!", lines)
    return False

fileModifiedHandler = FileModified(r"sample_text_input.txt",file_modified)
fileModifiedHandler.start()