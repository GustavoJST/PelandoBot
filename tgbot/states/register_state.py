# Create your states in this folder.
from telebot.asyncio_handler_backends import State, StatesGroup


class UserStates(StatesGroup):
    """
    Group of states for registering
    """
    tags_button = State()