from aiogram import Dispatcher, Bot, F
from aiogram.types import (Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardButton, InlineKeyboardMarkup)
from dotenv import load_dotenv
from aiogram.fsm.context import FSMContext   # fininte state machine 
from aiogram.fsm.state import State, StatesGroup
import os
from models import (connection, create_table, register, conn, add_order, get_my_orders,
                    get_user, add_item, get_item_by_id, get_items, ADMIN)
import asyncio
from buttons import geting_home, cancel



class Register(StatesGroup):
    full_name = State()    
    age = State()    
    address = State()    
    contact = State()    

class AddItems(StatesGroup):
    title = State()    
    description = State()    
    price = State()    
    photo_url = State()    


dp = Dispatcher()
bot = Bot(token=os.getenv("BOT_TOKEN"))



@dp.message(F.text =='/start')
async def start(message: Message):
    button = await geting_home(message.from_user.id)  
    await message.answer('Welcome to ur bot ', reply_markup=button)
    

@dp.message(F.text =='❌Cancel')
async def start(message: Message, state: FSMContext):
    button = await geting_home(message.from_user.id)  
    await state.clear()
    await message.answer('Welcome to ur bot ', reply_markup=button)
    








@dp.message(F.text =='👤Register')
async def start(message: Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    if user:
        await message.answer(
            f"Mr(s) {user['full_name']}\n"
            f"we have a news for u \n"
            f"U already register its enough"
        )
        return
    await message.answer('Enter ur full_name plz', reply_markup=cancel())
    await state.set_state(Register.full_name)


@dp.message(F.text =='👤Profile')
async def start(message: Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    if user:
        await message.answer(
            f"Mr(s) {user['full_name']}\n"
            f"Ur contact {user['contact']}\n"
            f"Ur age: {user['age']}"
        )
        return
    await message.answer('U havent register yet so u dont have any profile go and register',)




@dp.message(Register.full_name)
async def start(message: Message, state: FSMContext):
    if len(message.text) < 4 or   message.text.isdigit():
        await message.answer('Name shoudl be more then 4 letter')
        return
    await state.update_data(full_name = message.text)
    await message.answer('Enter ur age plz')
    await state.set_state(Register.age)
    


@dp.message(Register.age)
async def start(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Age shold be a number')
        return
    await state.update_data(age = message.text)
    await message.answer('Enter ur address plz')
    await state.set_state(Register.address)
    


@dp.message(Register.address)
async def start(message: Message, state: FSMContext):
    await state.update_data(address = message.text)
    contact = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Share ur contact harry up', request_contact=True)]
        ], resize_keyboard=True
    )
    await message.answer('Enter ur contact plz', reply_markup=contact)
    await state.set_state(Register.contact)




@dp.message(Register.contact, F.contact)
async def start(message: Message, state: FSMContext):
    await state.update_data(contact= message.contact.phone_number)
    data = await state.get_data()
    user= message.from_user
    try:
        await register(username=user.username, full_name=data['full_name'],
                    age=int(data['age']), address=data['address'], contact=data['contact'], tg_id=user.id)
        print('REgister')
        buttons = await geting_home(message.from_user.id)
        await message.answer('U registered successfully', reply_markup=buttons)
        await state.clear()
    except Exception as e:
        print(e)



#  ADD ITEMES PART 

@dp.message(F.text =='➕Add Items', F.from_user.id==ADMIN)
async def add_items(message: Message, state: FSMContext):
    
    await message.answer('Enter ur item title plz', reply_markup=cancel())
    await state.set_state(AddItems.title)




@dp.message(AddItems.title)
async def start(message: Message, state: FSMContext):
    if len(message.text) < 2 or   message.text.isdigit():
        await message.answer('Title shoudl be more then 2 letters and not number')
        return
    await state.update_data(title = message.text)
    await message.answer('Enter ur item description  plz')
    await state.set_state(AddItems.description)
    


@dp.message(AddItems.description)
async def start(message: Message, state: FSMContext):
    if len(message.text) < 2 or   message.text.isdigit():
        await message.answer('Description shoudl be more then 2 letters and not number')
        return
    await state.update_data(description = message.text)
    await message.answer('Enter ur item price  plz')
    await state.set_state(AddItems.price)
    


@dp.message(AddItems.price)
async def start(message: Message, state: FSMContext):
    if not  message.text.isdigit():
        await message.answer('Price shoudl be a number')
        return
    await state.update_data(price = float(message.text))
    await message.answer('Enter ur item photo  plz')
    await state.set_state(AddItems.photo_url)




@dp.message(AddItems.photo_url, F.photo)
async def start(message: Message, state: FSMContext):
    photo_url = message.photo[-1].file_id
    print(photo_url, 'photo_url id ')
    data = await state.get_data()

    try:
        r = await add_item(title=data['title'],
                    description=data['description'], price=data['price'], photo_url=photo_url)
        if r:
            await message.answer('Ur items has been added successfully')
        else:
            await message.answer('Ur items was not  added ', reply_markup=await geting_home(message.from_user.id))
        await state.clear()
        
    except Exception as e:
        print(e)
        await message.answer('Ur items was not  added ', reply_markup=await geting_home(message.from_user.id))



@dp.message(F.text == '🍽Menu')
async def show_items(message: Message, state: FSMContext):
    items = await get_items()
    if not items:
        await message.answer('We dont have any items yet')
        return
    
    buttons = []
    for item in items:
        button = InlineKeyboardButton(text=f'{item["title"]} - {item["price"]} c',
                                      callback_data=f'item:{item["id"]}') # item:3
        buttons.append([button])

    markup = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer('Here u are ', reply_markup=markup)

@dp.callback_query(F.data.startswith('item:'))
async def get_item_into(call: CallbackQuery):
    id = call.data.split(':')[-1]
    item = await get_item_by_id(int(id))
    print(item)
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Order Now', callback_data=f'order:{item["id"]}')]
        ]
    )
    await call.message.delete()
    await call.message.answer_photo(photo=item['photo_url'],
                                    caption=f'<b>{item["title"]}</b>\n{item["price"]}c\n{item["description"]}',
                                    parse_mode='HTML', reply_markup=markup)


@dp.callback_query(F.data.startswith('order:'))
async def get_item_into(call: CallbackQuery):
    id = int(call.data.split(':')[-1])
    user = call.from_user
    order = await add_order(user.id, id)
    buttons = await geting_home(user.id)
    if order:
            await call.message.answer('u ORDER WAS ADDED', reply_markup=buttons)
    else:
            await call.message.answer('u ORDER WAS not ADDED', reply_markup=buttons)
        



@dp.message(F.text == '🛒My Orders')
async def get_item_into(message: Message):
    orders = await get_my_orders(message.from_user.id)
    if not orders:
        await message.answer(
            f'U dont have any order go and order smth'
        )
        return
    answer = ''
    for order in orders:
        answer += f'Title: {order['i_title']}\nPrice: {order['i_price']}\n'
    
    await message.answer(answer)
     








        
    
    




async def main():
    print('Bot started')
    await connection()
    await create_table()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())