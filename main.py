import os
from instagrapi import Client
from media_loader import MediaLoader
from dotenv import load_dotenv
from telegram import TelegramNotifier

if __name__ == "__main__":
    load_dotenv()
    username = os.environ.get("USERNAME")
    password = os.environ.get("PASSWORD")
    media_loader = MediaLoader("media")
    notifier = TelegramNotifier()
    notifier.notify("Toji Everyday: Upload started")
    try:
        media_loader.load_media()
        client = Client()
        client.login(username, password)
        daily_media = media_loader.get_daily_media()
        daily_media.upload(client)
        daily_story = media_loader.get_daily_story()
        if daily_story is not None:
            daily_story.upload(client, to_story=True)
    except Exception as e:
        notifier.notify(f"Error: {e}")
    else:
        notifier.notify("Upload finished")

