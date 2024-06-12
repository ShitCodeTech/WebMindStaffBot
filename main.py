import os
import sys
import json
import asyncio
import logging
from dotenv import load_dotenv

from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram import Bot, Dispatcher, html, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.client.default import DefaultBotProperties
from aiogram.types import FSInputFile, CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import (
    InlineKeyboardMarkup,InlineKeyboardButton,
    ReplyKeyboardMarkup, ReplyKeyboardRemove,
    KeyboardButton
    )

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
print(os.path.dirname(os.path.abspath(__file__)))
with open(f'{os.path.dirname(os.path.abspath(__file__))}/config/config.json', 'r') as f:
    answers = json.load(f)
dp = Dispatcher()
bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )



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


first_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=button["text"], 
    callback_data=button["callback_data"]) for button in answers["buttons"]]])

main_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=button["text"], 
    callback_data=button["callback_data"]) for button in answers["main_keyboard"]["left_part"]],
    [InlineKeyboardButton(text=button["text"], 
    callback_data=button["callback_data"]) for button in answers["main_keyboard"]["right_part"]]])


@dp.message(CommandStart())
async def command_start_hadler(message: Message) -> None:
    await message.answer_photo(
        photo=FSInputFile(answers["start_photo"]),
        caption=answers["start_text"] + '\n\nIt`s time to choose your side',
        reply_markup=first_keyboard
        )



@dp.callback_query(lambda c: c.data in [button["callback_data"] for button in answers["buttons"]])
async def process_callback(callback_query: CallbackQuery):
    callback_data = callback_query.data
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="Next",
        callback_data="next")
    )
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_caption( 
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        caption=f'{answers["start_text"]}\n\n <b>{callback_data}</b>',
        parse_mode=ParseMode.HTML,
        reply_markup=builder.as_markup()
        )
    




@dp.callback_query(F.data == "next")
async def main_mode(callback_query: CallbackQuery):
    await bot.delete_message( 
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id
        )
    
    await bot.send_animation(
        chat_id=callback_query.message.chat.id,
        animation=FSInputFile('/home/killmilk/WM-dev/WebMindStaffBot/images/1.mp4'),
        reply_markup=main_keyboard
    )
    

async def main() -> None:
    await dp.start_polling(bot)




if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
