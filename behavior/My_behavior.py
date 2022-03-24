from abc import ABC, abstractmethod
import config

class My_behavior(ABC):
    state = None
    behavior_names = None
    button_options = config.default_keyboard_options

    def __init__(self, message):
        pass

    @abstractmethod
    async def get_response(self, message):
        pass


