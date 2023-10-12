from aiogram import Bot, executor, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

main_kb = ReplyKeyboardMarkup(resize_keyboard=True)
b1 = KeyboardButton('Каталог📗')
b2 = KeyboardButton('Корзина🛒')

first_start = ReplyKeyboardMarkup(resize_keyboard=True)
first_start.add(KeyboardButton('Начать покупки!✨'))

main_kb.add(b1)
main_kb.add(b2)

custom_order_kb = ReplyKeyboardMarkup(resize_keyboard=True)
custom_order_kb.add(KeyboardButton('Назад к каталогу⬅'))

custom_order_first_kb = ReplyKeyboardMarkup(resize_keyboard=True)
custom_order_first_kb.add(KeyboardButton('Да, сделать индивидуальный заказ✅'))
custom_order_first_kb.add(KeyboardButton('Назад к каталогу⬅'))

past_suho_kb = ReplyKeyboardMarkup(resize_keyboard=True)
past_suho_kb.add(KeyboardButton('Пастила🍎'), KeyboardButton('Индивидуальный заказ📦'))
past_suho_kb.add(KeyboardButton('Назад в главное меню⬅'))

to_main_menu_kb = ReplyKeyboardMarkup(resize_keyboard=True)
to_main_menu_kb.add(b2)
to_main_menu_kb.add(KeyboardButton('Назад в главное меню⬅'))


def kb_prod_page(somearg):
    kb = InlineKeyboardMarkup()
    but1 = InlineKeyboardButton(text='Выберите количество', callback_data='empty')
    but2 = InlineKeyboardButton(text='➖', callback_data='butt_minus')
    but3 = InlineKeyboardButton(text=f'{somearg}', callback_data='empty')
    but4 = InlineKeyboardButton(text='➕', callback_data='butt_plus')
    but5 = InlineKeyboardButton(text='Добавить в корзину', callback_data='add_to_cart')
    but6 = InlineKeyboardButton(text='Назад в меню пастилы', callback_data='Пастила🍎')
    kb.add(but1)
    kb.add(but2, but3, but4)
    kb.add(but5)
    kb.add(but6)

    return kb

in_cart_kb = ReplyKeyboardMarkup(resize_keyboard=True)
in_cart_kb.add(KeyboardButton('Очистить корзину🧹'), KeyboardButton('Удалить элементы❌'))
in_cart_kb.add(KeyboardButton('Оформить заказ✅'))
in_cart_kb.add(KeyboardButton('Каталог📗'), KeyboardButton('Назад в главное меню⬅'))

checkout_kb = ReplyKeyboardMarkup(resize_keyboard=True)
checkout_kb.add(KeyboardButton('Оформить✅'))
checkout_kb.add(KeyboardButton('Назад к корзине'))



admin_change = InlineKeyboardMarkup()
admin_change.add(InlineKeyboardButton(text='Изменить наименование', callback_data='Изменить наименование'))
admin_change.add(InlineKeyboardButton(text='Изменить количество', callback_data='Изменить количество'))
admin_change.add(InlineKeyboardButton(text='Изменить цену', callback_data='Изменить цену'))
admin_change.add(InlineKeyboardButton(text='Изменить описание', callback_data='Изменить описание'))
admin_change.add(InlineKeyboardButton(text='Назад', callback_data='Назад к админке'))

final_kb = ReplyKeyboardMarkup(resize_keyboard=True)
final_kb.add(KeyboardButton('Назад в главное меню⬅'))