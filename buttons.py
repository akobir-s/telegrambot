from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from models import get_user, ADMIN




async def geting_home(tg_id):
    user = await get_user(tg_id)

    if not user:
        return   ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text='🍽Menu')],
                [KeyboardButton(text='👤Register')]
            ], resize_keyboard=True
        )
    if user  and tg_id!=ADMIN:
        return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='🍽Menu'),KeyboardButton(text='🛒My Orders') ],
            [KeyboardButton(text='👤Profile')]
        ], resize_keyboard=True
    )
    if user and tg_id==ADMIN:
        return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='🍽Menu'),KeyboardButton(text='🛒My Orders') ],
            [KeyboardButton(text='👤Profile') ,KeyboardButton(text='➕Add Items') ]
        ], resize_keyboard=True
    )






def cancel():

        return   ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text='❌Cancel')],
            ], resize_keyboard=True
        )
   