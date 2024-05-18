import os
import shutil
import configparser
from pathlib import Path

config = configparser.ConfigParser()
config.read(Path('config.ini'))

directory = Path(config.get('Settings', 'directory'))

app_ids = set()

for entry in os.scandir(directory):
    if entry.is_file():
        file_name = entry.name
        app_id = file_name.split('_')[0]
        app_ids.add(app_id)

if not app_ids:
    print("No screenshots found, exiting...")
else:
    for app_id in app_ids:
        if app_id == '0':
            app_id = 'UNRECOGNIZED'
        app_id_dir = os.path.join(directory, app_id)
        if not os.path.exists(app_id_dir):
            os.makedirs(app_id_dir)

    for entry in os.scandir(directory):
        if entry.is_file():
            file_name = entry.name
            app_id = file_name.split('_')[0]
            if app_id == '0':
                app_id = 'UNRECOGNIZED'
            dest_path = os.path.join(directory, app_id, file_name)
            shutil.move(entry.path, dest_path)

    for app_id in app_ids:
        if app_id == '0':
            app_id = 'UNRECOGNIZED'
        app_id_dir = os.path.join(directory, app_id)
        print(f'Moved {len(os.listdir(app_id_dir))} files to the {app_id} directory.')