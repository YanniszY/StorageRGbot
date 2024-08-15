from aiogram.fsm.state import State, StatesGroup

class User(StatesGroup):
    user_file_id = State()
