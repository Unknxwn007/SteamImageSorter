import os
import shutil
import configparser
from pathlib import Path
import tkinter as tk
from tkinter import filedialog

# Create a config parser object and read the config file
config = configparser.ConfigParser()
config.read('config.ini')

# Check if API key and directory are present in the config file
if not config.get('Settings', 'api_key') or not config.get('Settings', 'directory'):
    # Prompt the user for the API key and directory
    api_key = input('Enter your API key: ') if not config.get('Settings', 'api_key') else config.get('Settings', 'api_key')
    directory = Path(input('Enter the directory of the external screenshots folder: ')) if not config.get('Settings', 'directory') else Path(config.get('Settings', 'directory'))

    # Use a pop-up window to select the directory if it was not provided
    if not directory.exists():
        root = tk.Tk()
        root.withdraw()
        directory = Path(filedialog.askdirectory())
        root.destroy()

    # Update the config file with the new values
    config['Settings'] = {'api_key': api_key, 'directory': str(directory)}
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

# Get the directory path from the config file
directory = Path(config.get('Settings', 'directory'))

# Find all the unique app IDs in the directory
app_ids = set()
for entry in os.scandir(directory):
    if entry.is_file():
        file_name = entry.name
        app_id = file_name.split('_')[0]
        app_ids.add(app_id)

if not app_ids:
    print("No screenshots found, exiting...")
else:
    # Create directories for each app ID
    for app_id in app_ids:
        if app_id == '0':
            app_id = 'Unrecognized game'
        app_id_dir = os.path.join(directory, app_id)
        if not os.path.exists(app_id_dir):
            os.makedirs(app_id_dir)

    # Move the screenshots to their respective directories
    for entry in os.scandir(directory):
        if entry.is_file():
            file_name = entry.name
            app_id = file_name.split('_')[0]
            if app_id == '0':
                app_id = 'Unrecognized game'
            dest_path = os.path.join(directory, app_id, file_name)
            shutil.move(entry.path, dest_path)

    # Print the number of screenshots moved for each app ID
    for app_id in app_ids:
        if app_id == '0':
            app_id = 'Unrecognized game'
        app_id_dir = os.path.join(directory, app_id)
        print(f'Moved {len(os.listdir(app_id_dir))} files to the {app_id} directory.')