from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
import requests
from aiogram.utils.markdown import hbold, hlink
from krysha import main as m
import json
from envparse import Env

env = Env()
TOKEN = env.str("TOKEN")

bot = Bot(TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_buttons = ["Квартиры"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer("Квартиры", reply_markup=keyboard)

@dp.message_handler(Text(equals="Квартиры"))
async def get_discount_sneakers(message: types.Message):
    await message.answer("Please waiting...")

    m()

    with open("result.json", encoding='utf-8') as file:
        data = json.load(file)

    for i in data:
        for item in i:
            card = f"{hlink(item.get('title'), item.get('price'))}\n" \
                   f"{hbold('Этаж: ')} {item.get('etaj')}\n" \
                   f"{hbold('Прайс: ')} {item.get('price')}\n" \
                   f"{hbold('Описание: ')} -{item.get('description')}%: {item.get('url')}🔥"

            await message.answer(card)

def main():
    executor.start_polling(dp)


if __name__ == '__main__':
    main()