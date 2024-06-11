import os
import sys
import json
import asyncio
import logging
from dotenv import load_dotenv

from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode
from aiogram.types import FSInputFile, CallbackQuery
from aiogram.filters import CommandStart
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties



load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
with open('config/config.json', 'r') as f:
    answers = json.load(f)
bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
dp = Dispatcher()


def useradd(uid, login, direction, passcode):
    data = {
        {uid}: {
            "uid": {uid},
            "login": {login},
            "direction": {direction},
            "pass": {passcode}
            }
    }
    with open('config/users.json','w') as users:
        json.dump(data, users)


def get_data(uid):
    with open('config/users.json','r') as ulist:
        users_data = json.load(ulist)
    return users_data.get(uid)


keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=button["text"], 
    callback_data=button["callback_data"]) for button in answers["buttons"]]
])


@dp.message(CommandStart())
async def command_start_hadler(message: Message) -> None:
    await message.answer_photo(
        photo=FSInputFile(answers["start_photo"]),
        caption=answers["start_text"],
        reply_markup=keyboard
        )



@dp.callback_query(lambda c: c.data in [button["callback_data"] for button in answers["buttons"]])
async def process_callback(callback_query: CallbackQuery):
    callback_data = callback_query.data
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f'You choose: {callback_data}')
    await bot.send_message(callback_query.from_user.id, "Time to set up your credentials\n\n How can i call you?")
    await YourStateName.password.set()

@dp.message_handler(state=YourStateName.password)
async def auth(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    password = message.text.strip()
    print(user_id,password)



async def main() -> None:
    await dp.start_polling(bot)




if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
