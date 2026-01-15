from aiogram.fsm.state import State, StatesGroup


class CreateClientState(StatesGroup):
    full_name = State()
    telegram_id = State()
    amount = State()
    due_date = State()
