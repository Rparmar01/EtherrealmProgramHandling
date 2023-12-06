import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

class MyHandler(PatternMatchingEventHandler):
    patterns = ["*.txt"]  # Adjust the pattern based on your file type

    def on_modified(self, event):
        super().on_modified(event)
        print(f'File {event.src_path} has been modified.')
        read_and_print_updated_text(event.src_path)

def read_and_print_updated_text(file_path):
    with open(file_path, 'r') as file:
        updated_text = file.read()
        print(f'Updated Text:\n{updated_text}')

if __name__ == "__main__":
    file_path_to_watch = f"C:\\Users\\rparm\\Documents\\GitHub\\Shap-eTextToMeshGit\\EtherrealmProgramHandling\\sample_text_input.txt"
 
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=file_path_to_watch, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()