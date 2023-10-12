from aiogram import Bot, executor, Dispatcher, types
from aiogram.dispatcher.filters import Text
# from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, CallbackQuery, ReplyKeyboardRemove, InputFile, \
#     InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters.state import StatesGroup, State
# from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from aiogram.utils.callback_data import CallbackData
# from price import update_price_past_dict, update_price_past_list
from config import TOKEN


storage = MemoryStorage()

class MainStates(StatesGroup):
    origin = State()
    prod_page = State()


@dp.message_handler(text=['Слово'], state=MainStates)
async def word(msg: types.Message):
    await msg.answer('LIDAAAA')