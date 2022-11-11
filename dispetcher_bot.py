from aiogram import Bot, Dispatcher, executor, types


from envparse import Env

env = Env()
TOKEN = env.str("TOKEN")

bot = Bot(TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer('hey')

def main():
    executor.start_polling(dp)


if __name__ == '__main__':
    main()