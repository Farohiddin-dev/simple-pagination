"""
This is a Pagination bot.
"""
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
from aiogram.dispatcher import FSMContext
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = 'TOKEN'

# Configure logging
logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)


def getleng(subcat):
    # leng = db.select_all_product(subcat)
    return 20


# State
class Paginate(StatesGroup):
    index = State()


# Keyboard
nextprev = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="⬅️", callback_data="prev"),
            InlineKeyboardButton(text="➡️", callback_data="next")
        ],
    ]
)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message, state: FSMContext):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    async with state.proxy() as data:
        data['index'] = 0
        data['maxind'] = 4
        data['messages'] = ['Assalomu Alaykum', 'Ahvollaringiz qalay?', 'Ishlaringiz yaxshimi?',
                            'Lorem Ipsum dolor', 'Hello World!']
    await message.reply("Salom !", reply_markup=nextprev)
    await Paginate.index.set()


@dp.callback_query_handler(text_contains='next', state=Paginate.index)
async def next_ms(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        messages = data['messages']
        maxin = data['maxind']
        # await call.answer()
        if data['index'] == maxin:
            # data['index'] = 0
            try:
                await call.answer(text="Bu oxirgi sahifa ⚠️", show_alert=True)
                # Yoki foydalanuvchini birinchi habarga otkazb qoyishingiz mumkin 👇🏻 # data['index'] = 0 bolishi kerak
                # return await call.message.edit_text(messages[0], reply_markup=nextprev)
            except:
                await call.answer("Nimadur xato ketdi")
        else:
            data['index'] += 1
            try:
                return await call.message.edit_text(text=f"{messages[data['index']]}\n\n{data['index']} / "
                                                         f"{maxin}", reply_markup=nextprev)
            except:
                await call.answer("Nimadur xato ketdi")


@dp.callback_query_handler(text_contains='prev', state=Paginate.index)
async def prev_ms(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        messages = data['messages']
        maxin = data['maxind']
        await call.answer()  # bosh sahifada ekanligini aytishingiz uchun buni kommentga oling
        if data['index'] == 0:
            data['index'] = maxin  # bosh sahifada ekanligini aytishingiz uchun buni kommentga oling
            try:
                return await call.message.edit_text(messages[4], reply_markup=nextprev)
                # Yoki obunachiga bosh sahifada ekanligini aytishingiz mumkin 👇🏻
                # await call.answer(text="Siz allaqachon bosh sahifadasiz ⚠️", show_alert=True)
            except:
                await call.answer("Nimadur xato ketdi")
        else:
            data['index'] -= 1
            try:
                return await call.message.edit_text(text=f"{messages[data['index']]}\n\n"
                                                         f"{data['index']} / "
                                                         f"{maxin}", reply_markup=nextprev)
            except:
                await call.answer("Nimadur xato ketdi")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
