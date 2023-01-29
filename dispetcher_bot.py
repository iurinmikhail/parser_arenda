from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hlink
from krysha import main as m
import json
from config import TOKEN


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
    try:
        m()
        with open("result.json", encoding='utf-8') as file:
            data = json.load(file)
        for i in data:
            for item in i:
                card = f"{hlink(item.get('title'), item.get('price'))}\n\n" \
                       f"{hbold('Стоимость: ')}{item.get('price')}\n\n" \
                       f"{hbold('Адрес: ')}{item.get('address')}\n\n" \
                       f"{hbold('Этаж: ')}{item.get('etaj')}\n\n" \
                       f"{hbold('Описание: ')}{item.get('description')}\n\n"\
                       f"🔥{item.get('url')}"
                await message.answer(card)
    except:
        return await message.answer("Новых квартир нет")


def main():
    while True:
        try:
            executor.start_polling(dp)
        except:
            print('Что-то сломалось. Перезагрузка')

if __name__ == '__main__':
    main()