import os
import yaml
from media_loader import Config

# Specify the directory you want to start from
rootDir = os.path.join(os.path.dirname(__file__), 'media')

print(f'Root directory: {rootDir}')
for dirName, subdirList, fileList in os.walk(rootDir):
    if len(fileList) == 1:
        file_name = fileList[0]
        file_extension = os.path.splitext(file_name)[1]
        if file_extension in ['.mp4', '.jpg', '.jpeg', '.png']:
            # Change working directory to the specified directory
            print(f'Found directory: {dirName}')
            os.chdir(dirName)

            # Rename the file to "media"
            new_file_name = "media" + file_extension
            os.rename(file_name, new_file_name)

            # Create a config.yaml file with the configurations from Config class
            config = Config()
            with open("config.yaml", "w") as f:
                yaml.dump(config.__dict__, f)

            # Change working directory back to the root directory
            os.chdir(rootDir)
