from aiogram.fsm.state import StatesGroup, State


class TaskStages(StatesGroup):
    add_task = State()
    complete_task = State()
