from abc import ABC, abstractmethod
import os
import datetime
import random
import logging
from pathlib import Path
from re import I
from tkinter.tix import IMAGE
from typing import Optional
from pydantic import BaseModel
import yaml
from instagrapi import Client


logger = logging.getLogger(__name__)
ConsoleOutputHandler = logging.StreamHandler()
logger.addHandler(ConsoleOutputHandler)
logger.setLevel(logging.INFO)

DEFAULT_CAPTION = """We all want to be like Toji. \n GO FOR IT. \n
    Feel free to send me a message if you have any clip of Toji Fushiguro. I'll be happy to post it here.
    \n\n #jujutsu #JujutsuKaisen #TojiFushiguro #Fushiguro #Toji #TojiFushiguroShorts #TojiFushiguroShortsCompilation
    #jjk #anime #manga #gojo #geto #sukuna #itadori #nobara #megumi #satoru #yuta #yujisatoru #yujikaisen #satorugojo
    """

START_DAY = datetime.datetime(2023, 11, 5)

class Config(BaseModel):
    """
    Config file for media
    """
    is_story: bool = False
    is_feed: bool = True
    is_easter_egg: bool = False
    caption: str = ""

    @classmethod
    def load(cls, config_file) -> 'Config':
        """
        Load config from file
        """
        with open(config_file) as f:
            config = yaml.load(f.read(), Loader=yaml.FullLoader)
        new_config =  cls.parse_obj(config)
        new_config.caption = new_config.set_publication_day(new_config.caption)
        return new_config

    def set_publication_day(self, caption: str) -> str:
        """
        Set the publication day in the caption
        """
        publication_day = datetime.datetime.today() - START_DAY
        caption =  f"DAY {publication_day.days} \n\n {caption}  \n\n  {DEFAULT_CAPTION}"
        return caption

    def save(self, config_file):
        """
        Save config to file
        """
        with open(config_file, "w") as f:
            yaml.dump(self.dict(), f, default_flow_style=False)

class Media(ABC):

    def __init__(self, file_path: Path,
                 config: Config,
                 thumbnail_path: Optional[Path] = None):
        """
        Media object
        """
        self.file_path = file_path
        self.thumbnail_path = thumbnail_path if thumbnail_path is not None else file_path.parent / "thumbnail.jpg"
        self.config = config
        self.thumbnail_exists = thumbnail_path is not None and thumbnail_path.exists()

    @abstractmethod
    def upload(self, client: Client, to_story: bool = False):
        """
        Upload media to instagram
        """
        pass

    def default_thumbnail(self):
        """
        Create a default thumbnail
        """
        default_thumbnail_path = str(self.file_path) + ".jpg"
        os.rename(default_thumbnail_path, self.thumbnail_path)


class Image(Media):
    def upload(self, client: Client, to_story: bool = False):
        """
        Upload image to instagram
        """
        if to_story and self.config.is_story or self.config.is_easter_egg:
            client.photo_upload_to_story(
                self.file_path,
                self.config.caption,
            )
        else:
            client.photo_upload(
                self.file_path,
                self.config.caption,
            )


class Video(Media):

    def __init__(self, file_path: Path, config: Config, thumbnail_path: Path | None = None):
        super().__init__(file_path, config, thumbnail_path)
        self.story_path = file_path.parent / "story.mp4"

    def upload(self, client: Client, to_story: bool = False):
        """
        Upload video to instagram
        """
        kwargs = {}
        if self.thumbnail_exists:
            kwargs = {
                "thumbnail": self.thumbnail_path,
            }
        if to_story and self.config.is_story or self.config.is_easter_egg:
            tarjet_path = self.file_path
            if self.story_path.exists():
                tarjet_path = self.story_path
            client.video_upload_to_story(
                tarjet_path,
                self.config.caption,
                **kwargs # type: ignore
            )
        else:
            client.video_upload(
                self.file_path,
                self.config.caption,
                **kwargs # type: ignore
            )
        if not self.thumbnail_exists:
            self.default_thumbnail()
            self.thumbnail_exists = True


MEDIA_FILE_EXTENSIONS = (".mp4", ".jpg", ".jpeg", ".png")
IMAGE_FILE_EXTENSIONS = (".jpg", ".jpeg", ".png")

class MediaFactory:

    @staticmethod
    def create_media(file_path: Path,
                     thumbnail_path: Optional[Path] = None,
                     config_path: Optional[Path] = None) -> Media:
        """
        Create media object
        """
        MediaFactory.validate(file_path, thumbnail_path)
        if config_path is None or not config_path.exists():
                config = Config()
                config.save(config_path)
        else:
            config = Config.load(config_path)
        if file_path.suffix in IMAGE_FILE_EXTENSIONS:
            return Image(file_path, config, thumbnail_path)
        else:
            return Video(file_path, config, thumbnail_path)

    @staticmethod
    def validate(file_path: Path, thumbnail_path: Optional[Path] = None):
        """
        Validate media file
        """
        if file_path.suffix not in MEDIA_FILE_EXTENSIONS:
            raise ValueError(f"Invalid file extension {file_path.suffix} {file_path}")
        if thumbnail_path is not None and not thumbnail_path.exists():
            logger.info(f"Thumbnail {thumbnail_path} does not exist")
        if thumbnail_path is not None and thumbnail_path.suffix != ".jpg":
            raise ValueError(f"Invalid thumbnail extension {thumbnail_path.suffix}")
        if file_path.suffix == ".jpg" and thumbnail_path is not None:
            logger.info(f"Thumbnail cannot be set for image {file_path}")

class MediaLoader:
    MEDIA_FILENAME = "media"
    THUMBNAIL_FILENAME = "thumbnail.jpg"
    CONFIG_FILENAME = "config.yaml"
    def __init__(self, directory):
        self.directory = directory
        self.media = []
        self.stories = []
        self.easter_eggs = []

    def load_media(self):
        """
        Load media from directory
        """
        for directories in os.listdir(self.directory):
            directory_path = Path(self.directory, directories)
            if directory_path.is_dir():
                media_path = None
                for file in os.listdir(directory_path):
                    if self.MEDIA_FILENAME in file:
                        media_path = directory_path / file
                        break
                thumbnail_path = directory_path / self.THUMBNAIL_FILENAME
                config_path = directory_path / self.CONFIG_FILENAME
                if media_path:
                    media = MediaFactory.create_media(media_path, thumbnail_path, config_path)
                    if media.config.is_story:
                        self.stories.append(media)
                    if media.config.is_easter_egg:
                        self.easter_eggs.append(media)
                    if media.config.is_feed:
                        self.media.append(media)
        if not self.media:
            raise ValueError("No media found in directory")
        if not self.stories:
            logger.info("No stories found in directory")
        if not self.easter_eggs:
            logger.info("No easter eggs found in directory")

    def get_daily_media(self) -> Media:
        """
        Get daily media
        """
        if self.media:
            return self.media[random.randint(0, len(self.media) - 1)]
        else:
            raise ValueError("No media found")

    def get_daily_story(self) -> Optional[Media]:
        """
        Get daily story
        """
        random_number = random.randint(1, 365)
        today = datetime.datetime.today()
        if self.easter_eggs and random_number == today.timetuple().tm_yday:
            return self.easter_eggs[random.randint(0, len(self.easter_eggs) - 1)]
        elif self.stories:
            return self.stories[random.randint(0, len(self.stories) - 1)]
        else:
            return None
