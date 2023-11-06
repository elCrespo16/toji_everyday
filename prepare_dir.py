import os
import yaml
from media_loader import Config

# Ask for directory
import sys

dir_path = sys.argv[1]

# Change working directory to the specified directory
os.chdir(dir_path)

# Get the name of the only file in the directory
file_name = os.listdir()[0]

# Rename the file to "media"
file_extension = os.path.splitext(file_name)[1]
new_file_name = "media" + file_extension
os.rename(file_name, new_file_name)

# Create a config.yaml file with the configurations from Config class
config = Config()
with open("config.yaml", "w") as f:
    yaml.dump(config.__dict__, f)
