# from aiogram import *
import os
import sys
import json
import asyncio
import logging
from dotenv import load_dotenv

from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode
from aiogram.types import FSInputFile
from aiogram.filters import CommandStart
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties





dp = Dispatcher()
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
with open('config/config.json', 'r') as f:
    answers = json.load(f)


keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=button["text"], callback_data=button["callback_data"]) for button in answers["buttons"]]
])


@dp.message(CommandStart())
async def command_start_hadler(message: Message) -> None:
    await message.answer_photo(
        photo=FSInputFile(answers["start_photo"]),
        caption=answers["start_text"],
        reply_markup=keyboard
        )


async def main() -> None:
    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)




if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
