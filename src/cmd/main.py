import logging

from src.telegram_bot import bot
import settings


if __name__ == "__main__":
    logging.basicConfig(level=settings.LOG_LEVEL)
    bot.main()
