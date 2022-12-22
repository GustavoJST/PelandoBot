from telebot.asyncio_handler_backends import State, StatesGroup

class UserStates(StatesGroup):
    """
    Group of states for registering
    """
    tags_button = State()
    tags_between = State()
    tags_add = State()
    tags_remove = State()