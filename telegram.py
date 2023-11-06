import os
import logging

import telebot


logger = logging.getLogger(__name__)
ConsoleOutputHandler = logging.StreamHandler()
logger.addHandler(ConsoleOutputHandler)
logger.setLevel(logging.INFO)

class Singleton(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instance

class TelegramNotifier(metaclass=Singleton):
    def __init__(self):
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN', "")
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID', "")
        self.bot = telebot.TeleBot(bot_token)

    def notify(self, message) -> None:
        try:
            self.bot.send_message(self.chat_id, message)
            logger.info(message)
        except Exception:
            logger.info("Could not send Telegram message")
