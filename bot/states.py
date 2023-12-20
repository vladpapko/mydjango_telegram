from aiogram.dispatcher.filters.state import State, StatesGroup

class UserState(StatesGroup):
    dialog_start = State()
    programming = State()
    biology = State()
    hotel_management = State()
    business_analysis = State()
    final = State()