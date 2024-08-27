from aiogram.fsm.state import StatesGroup, State


class TaskStages(StatesGroup):
    adding_task = State()
    completing_task = State()
