import emoji
from aiogram import Bot, executor, Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, CallbackQuery, InputFile, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from price import update_price_past_dict, update_price_past_list
from models import *
from kbs import main_kb, past_suho_kb, kb_prod_page, to_main_menu_kb, in_cart_kb,\
    admin_change, first_start, checkout_kb, custom_order_first_kb, final_kb

from config import TOKEN, ADMINS, MANAGER

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)

ADMINS = ADMINS
MANAGER = MANAGER

# Bot in TG: @fryts_bot

with db:
    db.create_tables([User, Catalog, Cart, Order])
    print('DONE')

def upd_pp(somearg=None):
    price_past = update_price_past_list()
    return price_past
def upd_pd(somearg=None):
    price_past_dict = update_price_past_dict()
    return price_past_dict

def upd_pinl(somearg=None):
    price_past = upd_pp()
    past_inl_kb = InlineKeyboardMarkup()

    past_inl_kb.add(InlineKeyboardButton(text=price_past[0], callback_data=price_past[0]),
                    InlineKeyboardButton(text=price_past[1], callback_data=price_past[1]))
    past_inl_kb.add(InlineKeyboardButton(text=price_past[2], callback_data=price_past[2]),
                    InlineKeyboardButton(text=price_past[3], callback_data=price_past[3]))
    past_inl_kb.add(InlineKeyboardButton(text=price_past[4], callback_data=price_past[4]),
                    InlineKeyboardButton(text=price_past[5], callback_data=price_past[5]))
    past_inl_kb.add(InlineKeyboardButton(text='Назад', callback_data='Каталог📗'))

    return past_inl_kb


class MainStates(StatesGroup):
    origin = State()
    prod_page = State()
    checkout = State()
    admin_origin = State()
    admin_prod_page = State()
    admin_change_name = State()
    admin_change_quantity = State()
    admin_change_price = State()
    admin_change_description = State()


@dp.message_handler(commands=['start'])
async def first_cmd_start(msg: types.Message, state: FSMContext):
    await msg.answer('Привет!\n'
                     'Компания "FRYTS" - это про пользу в каждом кусочке.\n'
                     'В последнее время мы всё больше следим за здоровьем и фигурой, но как же сложно отказаться от любимых сладостей.'
                     ' Отличная замена - это натуральная пастила без добавления сахара и крахмала.'
                     ' В каталоге можете ознакомиться с нашим ассортиментом.\n\nБудем рады видеть вас в качестве наших клиентов!',
                     reply_markup=first_start)
    username = msg.from_user.username
    print(username)
    if username is None:
        username = 'None'

    print(f'id: {msg.from_user.id} | username: {username} | full_name: {msg.from_user.full_name}' + '\n')
    User.get_or_create(user_id=msg.from_user.id, username=username, name=msg.from_user.full_name)

    await state.set_state(MainStates.origin)


@dp.message_handler(text=['Начать покупки!✨'], state=MainStates)
async def cmd_start(msg: types.Message, state: FSMContext) -> None:
    await msg.answer('Выберите направление↔', reply_markup=main_kb)


@dp.message_handler(text=['Назад в главное меню⬅'], state=MainStates)
async def in_main_menu(msg: types.Message, state: FSMContext) -> None:
    await cmd_start(msg, state)


@dp.message_handler(text=['Каталог📗', 'Назад к каталогу⬅'], state=MainStates)
async def cmd_catalog(msg: types.Message, state: FSMContext) -> None:
    await bot.send_photo(chat_id=msg.from_user.id, photo="https://chudo-prirody.com/uploads/posts/2021-08/1628909188_6-p-khitrii-kot-foto-6.jpg",
                         reply_markup=past_suho_kb,
                         caption='📗Мы долго тестировали различные сочетания вкусов в пастиле и самые удачные добавили в каталог.\n\n'
                                 '📦Если же у вас есть желание попробовать что-то необычное, то для вас мы готовы сделать индивидуальное сочетание.')


@dp.callback_query_handler(text=['Каталог📗'], state=MainStates)
async def catalog_dup(msg: types.Message, state: FSMContext):
    await cmd_catalog(msg, state)


@dp.message_handler(text=['Пастила🍎'], state=MainStates)
async def catalog_past(msg: types.Message, state: FSMContext):
    await bot.send_message(chat_id=msg.from_user.id, text='Каталог: Пастила🍎',
                           reply_markup=to_main_menu_kb)
    await bot.send_photo(chat_id=msg.from_user.id,
                         photo="https://chudo-prirody.com/uploads/posts/2021-08/1628909188_6-p-khitrii-kot-foto-6.jpg",
                         reply_markup= upd_pinl(), caption='🍎Актуальные позиции фруктовой пастилы:')
    await state.set_state(MainStates.origin)


@dp.callback_query_handler(text=['Пастила🍎'], state=MainStates)
async def catalog_past_dup(callback: CallbackQuery, state: FSMContext):
    await catalog_past(msg=callback, state=state)


@dp.message_handler(text=['Индивидуальный заказ📦'], state=MainStates)
async def custom_order(msg: types.Message):
    await msg.answer('Уверены что хотите сделать индивидуальный заказ?', reply_markup=custom_order_first_kb)


@dp.message_handler(text=['Да, сделать индивидуальный заказ✅'], state=MainStates)
async def custom_order(msg: types.Message):
    await msg.answer('Информация отправлена менеджеру!\nДля индивидуального заказа в ближайшее время личный менеджер свяжется с вами!\n\nМенеджер: @Arinocka_g')
    username = msg.from_user.username
    if username is None:
        username = 'None'
    await bot.send_message(chat_id=MANAGER,
                           text=f'Этот пользователь магазина решил сделать индивидуальный заказ!\n\n'
                                f'Имя пользователя: @{username}\nПолное имя: {msg.from_user.full_name}\nid: {msg.from_user.id}')

# Cтраница продукта


@dp.callback_query_handler(state=MainStates.origin)
async def prod_page(callback: CallbackQuery, state=FSMContext):
    price_past_dict = upd_pd()
    cb = callback.data
    if cb in price_past_dict:
        await state.set_state(MainStates.prod_page)
        #обработка ошибки ненайаденного фото
        try:
            photo = InputFile("media/{}.jpg".format(''.join(i for i in cb if i not in emoji.EMOJI_DATA)))
        except FileNotFoundError:
            photo=None
        await state.update_data(product=cb)
        async with state.proxy() as data:
            data['button_value'] = 1
        #также обработка ошибки ненайденного фото
        try:
            await bot.send_photo(
                             chat_id=callback.from_user.id,
                             caption='{0}\n\n🍏{1}\n\n🍏Количество на складе: {2}\n🍏Цена: {3}р.'.format(data['product'],
                                                                            price_past_dict[data['product']]['Описание'],
                                                                            price_past_dict[data['product']]['Количество'],
                                                                            price_past_dict[data['product']]['Цена']),
                             photo=photo,
                             reply_markup=kb_prod_page(data['button_value'])
            )
        except Exception:
            await bot.send_message(
                                 chat_id=callback.from_user.id,
                                 text='{0}\n\n🍏{1}\n\n🍏Количество на складе: {2}\n🍏Цена: {3}р.'.format(data['product'],
                                                                            price_past_dict[data['product']]['Описание'],
                                                                            price_past_dict[data['product']]['Количество'],
                                                                            price_past_dict[data['product']]['Цена']),
                                 reply_markup=kb_prod_page(data['button_value']))


@dp.callback_query_handler(Text(startswith='butt_'), state=MainStates.prod_page)
async def somefunc(callback, state: FSMContext):
    button_value = callback.data.split('_')[1]
    price_past_dict = upd_pd()
    async with state.proxy() as data:
        if button_value == 'minus' and data['button_value'] > 1:
            data['button_value'] -= 1
        if button_value == 'plus' and data['button_value'] < int(price_past_dict[data['product']]['Количество']):
            data['button_value'] += 1

    await callback.message.edit_reply_markup(reply_markup=kb_prod_page(data['button_value']))


@dp.callback_query_handler(text=['add_to_cart'], state=MainStates)
async def add_to_cart(callback: CallbackQuery, state: FSMContext):

    price_past_dict = upd_pd()
    data = await state.get_data()
    print(price_past_dict[data['product']])
    global quantity_prod
    quantity_prod = int(data['button_value'])

    cartik = Cart.select().where(Cart.user_id == callback.from_user.id)

    cartik_prod_list = [i.product for i in cartik]
    print(cartik_prod_list)
    if quantity_prod > price_past_dict[data['product']]['Количество']:
        await bot.send_message(chat_id=callback.from_user.id, text='Продукта нет в наличии')
    else:
        if data['product'] in cartik_prod_list:
            cart = Cart.get(Cart.product == data['product'])
            if cart.quantity + quantity_prod <= Catalog.get(Catalog.name == data['product']).quantity:
                cart.quantity += quantity_prod
                cart.save()
        else:
            if callback.from_user.username is None:
                Cart.create(user_id=callback.from_user.id, username='None', product=data['product'],
                    quantity=quantity_prod, price=price_past_dict[data['product']]['Цена']*quantity_prod)
            else:
                Cart.create(user_id=callback.from_user.id, username=callback.from_user.username, product=data['product'],
                            quantity=quantity_prod, price=price_past_dict[data['product']]['Цена'] * quantity_prod)

        await bot.send_message(chat_id=callback.from_user.id, text='Продукт добавлен в корзину')
        await catalog_past(msg=callback, state=state)


@dp.message_handler(text=['Корзина🛒', 'Назад к корзине'], state=MainStates)
async def cart(msg: types.Message):
    await msg.answer('🛒Ваша корзина:')

    cartik = Cart.select().where(Cart.user_id == msg.from_user.id)
    sum_price = [i.price for i in cartik]
    if not cartik:
        await msg.answer('Пусто', reply_markup=in_cart_kb)

    for cart in cartik:
        if cart.quantity > 1:
            await msg.answer('🍏({0}) {1}: {2}р.'.format(cart.quantity, cart.product, cart.price))
        else:
            await msg.answer('🍏{0}: {1}р.'.format(cart.product, cart.price))

    await msg.answer(f"🍎Итого: {sum(sum_price)}р.", reply_markup=in_cart_kb)


@dp.message_handler(text=['Очистить корзину🧹'], state=MainStates)
async def clean_cart(msg:types.Message):
    del_list = Cart.select(Cart.user_id).where(Cart.user_id == msg.from_user.id)
    Cart.delete().where(Cart.user_id.in_(del_list)).execute()
    await msg.answer('Коризна очищена✅')


async def remove_prods_kb(msg):
    remove_prods = ReplyKeyboardMarkup()
    cartt = Cart.select().where(Cart.user_id == msg.from_user.id)
    for key in cartt:
        remove_prods.add(KeyboardButton(text=f"❌Удалить {key.product}"))
    remove_prods.add(KeyboardButton(text='Назад к корзине'))
    print(remove_prods)
    return remove_prods


@dp.message_handler(text=['Удалить элементы❌'], state=MainStates)
async def delete_elems_in_cart(msg: types.Message):
    await msg.answer('Какие элементы вы хотите удалить из корзины?', reply_markup= await remove_prods_kb(msg))


@dp.message_handler(Text(startswith='❌Удалить'), state=MainStates)
async def deleting_elem(msg: types.Message):
    print(msg.text.split(' ')[1])
    user_cart = Cart.select().where(Cart.user_id == msg.from_user.id)
    Cart.delete().where(Cart.user_id.in_(user_cart) and Cart.product == msg.text.split(' ')[1]).execute()
    await msg.answer('Товар успешно удалён из корзины!')
    await msg.answer('Какие ещё элементы вы хотите удалить из корзины?', reply_markup=await remove_prods_kb(msg))


@dp.message_handler(text=['Оформить заказ✅'], state=MainStates)
async def checkout_one(msg: types.Message, state:FSMContext):
    actual_catalog = upd_pp()
    cartik = Cart.select().where(Cart.user_id == msg.from_user.id)
    cart = [i.product for i in cartik]

    if not cart:
        await msg.answer('Корзина пуста')
    else:
        if set(cart).issubset(actual_catalog):
            await msg.answer(
                'Вы уверены что хотите оформить заказ?\n'
                'При оформлении заказа, информация о нём уйдёт менеджеру, который позднее свяжется с вами',
                reply_markup=checkout_kb
            )
            await state.set_state(MainStates.checkout)
        else:
            await msg.answer('Кажется некоторые товары в вашей корзине потеряли свою актуальность.\n'
                             'Пожалуйста очистите корзину и выберите товары для покупки ещё раз')


@dp.message_handler(text=['Оформить✅'], state=MainStates.checkout)
async def checkout_two(msg: types.Message):
    #приходит админу
    await bot.send_message(chat_id=MANAGER, text='Новый заказ❗')

    cartik = Cart.select().where(Cart.user_id == msg.from_user.id)
    sum_price = [i.price for i in cartik]

    for i in cartik:
        Catalog.update({Catalog.quantity: Catalog.quantity-i.quantity}).where(Catalog.name == i.product).execute()

    for cart in cartik:
        if cart.quantity > 1:
            await bot.send_message(chat_id=MANAGER, text='🍏({0}) {1}: {2}р.'.format(cart.quantity, cart.product, cart.price))
        else:
            await bot.send_message(chat_id=MANAGER,
                                   text='🍏{0}: {1}р.'.format(cart.product, cart.price))
    Order.create(user_id=msg.from_user.id)
    data = Order.select(fn.MAX(Order.id))
    for row in data:
        numb = row.id

    minimum = Order.select(fn.MIN(Order.id))
    for r in minimum:
        min = r.id
    Order.delete().where(Order.id == min).execute()

    username = '@'+str(msg.from_user.username)
    if msg.from_user.username is None:
        username = msg.from_user.url

    await bot.send_message(chat_id=MANAGER, text=f"🍎Итого: {sum(sum_price)}р.\n\n"
                                                   f"❗Номер заказа:№{numb}\nИмя пользователя: {username}\n"
                                                   f"Полное имя: {msg.from_user.full_name}\nid: {msg.from_user.id}")
    Cart.delete().where(Cart.user_id == msg.from_user.id).execute()

    await msg.answer('Отлично! Ваш заказ оформлен, в ближайшее время ваш личный менджер свяжется с вами для оплаты заказа!\n\n'
                     'Менеджер: @Arinocka_g', reply_markup=final_kb)


# Администрирование


@dp.message_handler(text=['Админка', 'админка'], state=MainStates)
async def admin_panel(msg:types.Message, state: FSMContext):
    if str(msg.from_user.id) in ADMINS:
        await bot.send_photo(
                             chat_id=msg.from_user.id,
                             photo="https://chudo-prirody.com/uploads/posts/2021-08/1628909188_6-p-khitrii-kot-foto-6.jpg",
                             reply_markup=upd_pinl(), caption='Какую позицию вы хотите изменить?'
        )
        await state.set_state(MainStates.admin_origin)
    else:
        await msg.answer('Нет доступа')


@dp.callback_query_handler(text=['Назад к админке'], state=MainStates)
async def admin_panel_dup(callback: None, state: FSMContext):
    if str(callback.from_user.id) in ADMINS:
        await admin_panel(callback, state)
        await state.set_state(MainStates.admin_origin)
    else:
        pass


@dp.callback_query_handler(state=MainStates.admin_origin)
async def admin_prod_page(callback: CallbackQuery, state=FSMContext):
    price_past_dict = upd_pd()
    cb = callback.data
    if cb in price_past_dict:
        await state.set_state(MainStates.prod_page)
        try:
            photo = InputFile("media/{}.jpg".format(''.join(i for i in cb if i not in emoji.EMOJI_DATA)))
        except FileNotFoundError:
            photo = None
        async with state.proxy() as data:
            data['product'] = cb
            data['position'] = price_past_dict[data['product']]['Позиция']
        print(data['position'])
        try:
            await bot.send_photo(
                             chat_id=callback.from_user.id,
                             caption='Наименование: {0}\n\n🍏{1}\n\n🍏Количество на складе: {2}\n🍏Цена: {3}р.'.format(data['product'],
                                                                            price_past_dict[data['product']]['Описание'],
                                                                            price_past_dict[data['product']]['Количество'],
                                                                            price_past_dict[data['product']]['Цена']),
                             photo=photo, reply_markup=admin_change
            )
        except Exception:
            await bot.send_message(
                                 chat_id=callback.from_user.id,
                                 text='Наименование:{0}\n\n🍏{1}\n\n🍏Количество на складе: {2}\n🍏Цена: {3}р.'.format(data['product'],
                                                                            price_past_dict[data['product']]['Описание'],
                                                                            price_past_dict[data['product']]['Количество'],
                                                                            price_past_dict[data['product']]['Цена']),
                                 reply_markup=admin_change)


@dp.callback_query_handler(text=['Изменить наименование'], state=MainStates.prod_page)
async def admin_change_name_short(callback: CallbackQuery, state=FSMContext):
    await bot.send_message(chat_id=callback.from_user.id, text='Введите новое название для этой позиции')
    await state.set_state(MainStates.admin_change_name)


@dp.message_handler(state=MainStates.admin_change_name)
async def admin_change_name(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    catalog = Catalog.get(Catalog.id == data['position'])
    catalog.name = msg.text
    catalog.save()
    upd_pinl()
    upd_pd()
    upd_pp()
    await state.set_state(MainStates.admin_origin)
    await admin_panel(msg, state)


@dp.callback_query_handler(text=['Изменить количество'], state=MainStates.prod_page)
async def admin_change_quantity_short(callback: CallbackQuery, state=FSMContext):
    await bot.send_message(chat_id=callback.from_user.id, text='Введите новое количество для этой позиции')
    await state.set_state(MainStates.admin_change_quantity)


@dp.message_handler(state=MainStates.admin_change_quantity)
async def admin_change_quantity(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    catalog = Catalog.get(Catalog.id == data['position'])
    catalog.quantity = msg.text
    catalog.save()
    upd_pinl()
    upd_pd()
    upd_pp()
    await state.set_state(MainStates.admin_origin)
    await admin_panel(msg, state)


@dp.callback_query_handler(text=['Изменить цену'], state=MainStates.prod_page)
async def admin_change_name(callback: CallbackQuery, state=FSMContext):
    await bot.send_message(chat_id=callback.from_user.id, text='Введите новую цену для этой позиции')
    await state.set_state(MainStates.admin_change_price)


@dp.message_handler(state=MainStates.admin_change_price)
async def admin_change_name(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    catalog = Catalog.get(Catalog.id == data['position'])
    catalog.price = msg.text
    catalog.save()
    upd_pinl()
    upd_pd()
    upd_pp()
    await state.set_state(MainStates.admin_origin)
    await admin_panel(msg, state)


@dp.callback_query_handler(text=['Изменить описание'], state=MainStates.prod_page)
async def admin_change_name(callback: CallbackQuery, state=FSMContext):
    await bot.send_message(chat_id=callback.from_user.id, text='Введите новое описание для этой позиции')
    await state.set_state(MainStates.admin_change_description)


@dp.message_handler(state=MainStates.admin_change_description)
async def admin_change_name(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    catalog = Catalog.get(Catalog.id == data['position'])
    catalog.description = msg.text
    catalog.save()
    upd_pinl()
    upd_pd()
    upd_pp()
    await state.set_state(MainStates.admin_origin)
    await admin_panel(msg, state)

async def on_startup(dp):
    print('Сервер запущен!')

if __name__ == "__main__":
    executor.start_polling(dispatcher=dp,
                           skip_updates=True, on_startup=on_startup)