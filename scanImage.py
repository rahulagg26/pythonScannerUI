import os
import subprocess

def scanImage(scanner_path, saved_images_path):
    # os.system(scanner_path)
    process = subprocess.Popen([scanner_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # print(process)
    stdout, stderr = process.communicate()
    if stderr:
        print(f"Error: {stderr.decode()}")
    # Wait until the subprocess (application) is closed
    process.wait() 

    folder_path = saved_images_path

    files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    # debug
    # print(files)
    # If there are no files, handle this case
    if not files:
        print("No files found in the directory.")
    else:
        # Sort the files by their last modified time in descending order
        files.sort(key=lambda x: os.path.getmtime(x), reverse=True)

        # Get the most recent file
        most_recent_file = files[0]

        print(f"Opening the most recent file: {most_recent_file}")
        return most_recent_file
    
