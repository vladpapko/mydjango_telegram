
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from states import UserState
from api import create_user, create_feedback, create_feedback1, create_feedback2, create_feedback3, create_feedback4
from api import update_subscription_status
API_TOKEN = '6768312843:AAFbscy6xZSBLygMbDoCUR5D8_znDS6Fylw'
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler(Command("start"))
async def start_command(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(text="Да"))
    keyboard.add(KeyboardButton(text="Нет"))

    await message.answer("Привет, я бот помогающий выбрать направление в вузе, ответь на пару вопросов и я помогу тебе, хочешь начать?", reply_markup=keyboard)
    print(create_user(message.from_user.username, message.from_user.first_name, message.from_user.id))
    await UserState.dialog_start.set()

@dp.message_handler(state=UserState.dialog_start)
async def dialog_start(message: types.Message, state: FSMContext):
    if message.text.lower() == "да":
        await message.answer("Ты любишь изучать программирование?")
        await message.answer(create_feedback(message.from_user.id,  message.text))
        await UserState.programming.set()
    else:
        await state.finish()
        await message.answer("Окей, если решиться, напиши /start")

@dp.message_handler(state=UserState.programming)
async def dialog_programming(message: types.Message, state: FSMContext):
    score = 0
    if message.text.lower() == "да":
        score += 1

    await message.answer("Ты любишь изучать биологию?")
    await message.answer(create_feedback1(message.from_user.id,  message.text))
    await UserState.biology.set()
    await state.update_data(score=score)

@dp.message_handler(state=UserState.biology)
async def dialog_biology(message: types.Message, state: FSMContext):
    data = await state.get_data()
    score = data.get("score", 0)

    if message.text.lower() == "нет":
        score += 1

    await message.answer("Ты бы хотел узнать, как обслуживать клиентов в гостинице?")
    await message.answer(create_feedback2(message.from_user.id,  message.text))
    await UserState.hotel_management.set()
    await state.update_data(score=score)

@dp.message_handler(state=UserState.hotel_management)
async def dialog_hotel_management(message: types.Message, state: FSMContext):
    data = await state.get_data()
    score = data.get("score", 0)

    if message.text.lower() == "нет":
        score += 1

    await message.answer("Ты бы хотел погрузиться в бизнес-анализ?")
    await message.answer(create_feedback3(message.from_user.id,  message.text))
    await UserState.business_analysis.set()
    await state.update_data(score=score)

@dp.message_handler(state=UserState.business_analysis)
async def dialog_business_analysis(message: types.Message, state: FSMContext):
    data = await state.get_data()
    score = data.get("score", 0)

    if message.text.lower() == "да":
        score += 1

    direction = "Прикладная информатика" if score >= 2 else "Другое направление"

    await message.answer(f"Я считаю, что тебе подойдет направление \"{direction}\"!\n"
                     "Хотел бы ты получать интересную информацию о поступлении в вуз?",
                     reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[["Да", "Нет"]]))


    await UserState.final.set()
    await state.update_data(direction=direction, score=score)

@dp.message_handler(state=UserState.final)
async def dialog_final(message: types.Message, state: FSMContext):
    data = await state.get_data()
    direction = data.get("direction", "")
    score = data.get("score", 0)

    if message.text.lower() == "да":
        await message.answer("Отлично! Буду стараться радовать тебя информацией")
        update_subscription_status(message.from_user.id, True)  # подписка
    elif message.text.lower() == "нет":
        await message.answer("Спасибо за участие! Если решиться, напиши /start")
        update_subscription_status(message.from_user.id, False)
    else:
        await message.answer("Пожалуйста, ответьте 'Да' или 'Нет'.")
        return

   
    await message.answer(create_feedback4(message.from_user.id, message.text))
    
    

  
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
