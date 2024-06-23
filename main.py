import os
from instagrapi import Client
from pathlib import Path
from media_loader import MediaLoader
from dotenv import load_dotenv
from telegram import TelegramNotifier
from instagrapi.exceptions import LoginRequired
import logging

logger = logging.getLogger(__name__)
ConsoleOutputHandler = logging.StreamHandler()
logging.basicConfig(filename='summary.log', encoding='utf-8', level=logging.INFO)
logger.addHandler(ConsoleOutputHandler)
logger.setLevel(logging.INFO)
session_path = Path("session.json")

def login_user(cl: Client, USERNAME: str, PASSWORD: str):
    """
    Attempts to login to Instagram using either the provided session information
    or the provided username and password.
    """

    session = cl.load_settings(session_path) if session_path.exists() else None

    login_via_session = False
    login_via_pw = False

    if session:
        try:
            cl.set_settings(session)
            cl.login(USERNAME, PASSWORD)

            # check if session is valid
            try:
                cl.get_timeline_feed()
            except LoginRequired:
                logger.info("Session is invalid, need to login via username and password")

                old_session = cl.get_settings()

                # use the same device uuids across logins
                cl.set_settings({})
                cl.set_uuids(old_session["uuids"])

                cl.login(USERNAME, PASSWORD)
            login_via_session = True
        except Exception as e:
            logger.info("Couldn't login user using session information: %s" % e)

    if not login_via_session:
        try:
            logger.info("Attempting to login via username and password. username: %s" % USERNAME)
            if cl.login(USERNAME, PASSWORD):
                login_via_pw = True
        except Exception as e:
            logger.info("Couldn't login user using username and password: %s" % e)

    if not login_via_pw and not login_via_session:
        raise Exception("Couldn't login user with either password or session")

if __name__ == "__main__":
    load_dotenv()
    username = os.environ.get("USERNAME", "")
    password = os.environ.get("PASSWORD", "")
    media_loader = MediaLoader("media")
    notifier = TelegramNotifier()
    notifier.notify("Toji Everyday: Upload started")
    try:
        media_loader.load_media()
        client = Client()
        client.delay_range = [1, 3]
        login_user(client, username, password)
        daily_media = media_loader.get_daily_media()
        logger.info(f"Uploading {daily_media.file_path}")
        daily_media.upload(client)
        daily_story = media_loader.get_daily_story()
        if daily_story is not None:
            logger.info(f"Uploading {daily_story.file_path}")
            daily_story.upload(client, to_story=True)
        client.dump_settings(session_path)
    except Exception as e:
        notifier.notify(f"Error: {e}")
    else:
        notifier.notify("Upload finished")

