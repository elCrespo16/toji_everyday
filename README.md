# Instagram Media Uploader Project

This project automates the daily uploading of media to Instagram using the `instagrapi` library. The project consists of multiple scripts to handle media files, configurations, and the automation of uploads.

## Prerequisites

Before running the scripts, make sure you have the required dependencies installed. You can install them using the following command:

pip install instagrapi pydantic python-dotenv

## Directory Preparation Script

The following script prepares a directory for use with the Instagram media uploading project. It assumes the directory contains a single media file, renames that file to "media," and creates a `config.yaml` file with default configurations.

### Usage

Run the script using the following command:

python prepare_dir.py /path/to/directory

Replace `/path/to/directory` with the path to the directory you want to prepare.

### Steps Performed by the Script

1. **Change Working Directory:** The script changes the working directory to the specified directory.

2. **Get File Name:** It identifies the name of the only file in the directory.

3. **Rename the File:** The script renames the file to "media" to ensure consistency with the media loader script.

4. **Create `config.yaml`:** It creates a `config.yaml` file in the directory with default configurations generated from the `Config` class in the `media_loader.py` script.

## Media Loader

The `media_loader.py` script handles media files and their configurations. It supports both images and videos, with optional features like daily stories and easter eggs.

### Prerequisites

Before using the script, make sure you have the required dependencies installed. You can install them using the following command:

pip install instagrapi pydantic

### Configuration

Refer to the provided `media_loader.py` README section for details on how to organize your media files, configure media settings, and use the media loader script.

### Usage

To use the script, follow the steps outlined in the `media_loader.py` README section.

## Main Uploading Script (main.py)

The `main.py` script automates the daily uploading of media to Instagram. It uses the `instagrapi` library for Instagram interactions and sends notifications via Telegram.

### Usage

1. Create a `.env` file in the project root directory with the following content:

USERNAME=your_instagram_username
PASSWORD=your_instagram_password
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id

Replace the placeholders with your Instagram credentials, Telegram bot token, and chat ID.

2. Organize your media files into directories within the `media` directory.

3. Customize the `DEFAULT_CAPTION` in `media_loader.py` to fit your preferences.

4. Run the `main.py` script using the following command:

python main.py

### Notes

- The script uses the `instagrapi` library for Instagram interactions.
- Session information is stored in `session.json` for persistent login.
- Notifications are sent via Telegram to the specified chat ID using a Telegram bot.



Feel free to reach out if you have any questions or encounter issues. Happy uploading!

# Automating Daily Uploads with Cron Job

To automate the daily uploading of media to Instagram, set up a cron job as follows:

1. Open the crontab configuration file for editing:
```bash
crontab -e
```
2. Add the following line to run the upload script every day at 11:00 AM:
```cron
0 11 * * * cd $HOME/toji_everyday && ./upload.sh
```
This cron job changes to the project directory and executes the upload.sh script.
# Upload Script (upload.sh)
To facilitate the daily uploads, a Bash script (upload.sh) has been provided. Follow these steps to use the script:

1. Create a new file named upload.sh in your project directory.

2. Copy and paste the following content into upload.sh:
```bash
#!/bin/bash

set -e

# Source your bashrc or any necessary environment setup
source /path_to/.bashrc

# Change to the project directory
cd /path_to/toji_everyday

# Activate the virtual environment using pyenv
pyenv activate toji_everyday

# Execute the main.py script and log the output to toji_logs.log
pyenv exec python main.py >> toji_logs.log
```

3. Save and close the file.

4. Make the script executable:
```bash
chmod +x upload.sh
```

Now, you can rely on the cron job to automatically upload media to Instagram every day at the specified time.

## Notes
- Make sure to customize the paths and filenames in the scripts based on your project setup.
- Adjust the cron schedule (0 11 * * *) according to your desired daily upload time.