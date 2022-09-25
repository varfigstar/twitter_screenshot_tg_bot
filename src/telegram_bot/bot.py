import logging
import asyncio
import functools
import io
from concurrent.futures.thread import ThreadPoolExecutor
from typing import List

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import settings
from . import texts
from src.twitter_parser.parser import ParsersPool

pool_executor = ThreadPoolExecutor(max_workers=settings.MAX_WORKERS)
bot = Bot(settings.API_TOKEN)
URL_REGEXP = "http(?:s)?:\/\/(?:www\.)?twitter\.com"
twitter_parsers = ParsersPool(parsers_num=settings.MAX_WORKERS)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
    url = State()
    twit_depth = State()


@dp.message_handler(commands=["start", "help"])
async def send_welcome_message(message: types.Message):
    await Form.url.set()
    await message.reply(texts.WELCOME_MESSAGE)


@dp.message_handler(regexp=URL_REGEXP, state="*")
async def take_url(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        data["url"] = message.text

    await Form.twit_depth.set()

    await message.reply(text=texts.ASK_DEPTH_MESSAGE)


@dp.message_handler(lambda message: message.text.isdigit() and int(message.text) <= 10, state=Form.twit_depth)
async def send_screenshot(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        url = data.get("url")
    twit_depth = int(message.text)

    await message.reply(texts.START_TASK_MESSAGE)

    func = functools.partial(twitter_parsers.take_screenshots, url, twit_depth)
    screenshots: List[bytes] = await asyncio.get_running_loop().run_in_executor(pool_executor, func)

    if screenshots:
        media_group = types.MediaGroup()
        [media_group.attach_photo(io.BytesIO(photo)) for photo in screenshots]
        await bot.send_media_group(
            chat_id=message.chat.id, reply_to_message_id=message.message_id, media=media_group
        )
    else:
        await message.reply(texts.ERROR_MESSAGE)

    await state.finish()
    await Form.url.set()


def main():
    executor.start_polling(dp, skip_updates=False)


if __name__ == "__main__":
    main()
