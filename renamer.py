import os
import shutil
import configparser
import requests # type: ignore

# Load config file
config = configparser.ConfigParser()
config.read('config.ini')
api_key = config.get('Settings', 'api_key')
directory = config.get('Settings', 'directory')
exclusion_list = config.get('Settings', 'exclusion_list').split(',')
unknown_game_folder = os.path.join(directory, "unknown game")

# Create unknown game folder if it doesn't exist
if not os.path.exists(unknown_game_folder):
    os.makedirs(unknown_game_folder)

# Process each folder one at a time
for folder in os.listdir(directory):
    # Check if the folder contains an appid
    if folder.isdigit():
        app_id = folder
        if int(app_id) in exclusion_list:
            continue
        try:
            # Look up the game name using the Steam store API
            url = f"https://store.steampowered.com/api/appdetails?appids={app_id}"
            response = requests.get(url)
            data = response.json()
            if data[app_id]['success'] and 'data' in data[app_id] and 'name' in data[app_id]['data']:
                name = data[app_id]['data']['name']
                new_folder_name = name.replace(':', ' ').replace('/', '_')
                old_folder_path = os.path.join(directory, folder)
                new_folder_path = os.path.join(directory, new_folder_name)
                if os.path.exists(new_folder_path):
                    # Destination folder already exists, move files instead of renaming
                    for filename in os.listdir(old_folder_path):
                        src_file = os.path.join(old_folder_path, filename)
                        dst_file = os.path.join(new_folder_path, filename)
                        shutil.move(src_file, dst_file)
                    shutil.rmtree(old_folder_path)
                    print(f"Moved files from folder {folder} to {new_folder_name}")
                else:
                    os.rename(old_folder_path, new_folder_path)
                    print(f"Renamed folder {folder} to {new_folder_name}")
            else:
                print(f"Failed to retrieve game details for App ID: {app_id}")
                print(data)  # Print API response for troubleshooting
                shutil.move(os.path.join(directory, folder), unknown_game_folder)
                print(f"Moved folder {folder} to unknown game folder")
        except Exception as e:
            print(f"Error getting game name for App ID {app_id}: {e}")