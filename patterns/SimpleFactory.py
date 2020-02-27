from abc import ABC, abstractmethod

# Simple Factory
class AbstractDoor(ABC):
    @abstractmethod
    def get_width(self):
        pass

    @abstractmethod
    def get_height(self):
        pass

    @abstractmethod
    def create_door(self, width: int, height: int):
        pass


class WoodenDoor(AbstractDoor):
    __width = None
    __height = None

    def create_door(self, width: int, height: int):
        # тут может быть какаято логика по вычислению данных
        # например нужно перевести длину и ширину в дюймы
        self.__width = width / 25.4
        self.__height = height / 25.4

    def get_width(self):
        return self.__width

    def get_height(self):
        return self.__height

    def __init__(self, width: int, height: int):
        self.create_door(width=width, height=height)


class DoorFactory(object):
    def make_door(self, width: int, height: int):
        return WoodenDoor(width=width, height=height)


door = DoorFactory().make_door(900, 2005)

print(door.get_width(), door.get_height())


# Когда создание объекта — это не просто несколько присвоений,
# а какая-то логика, тогда имеет смысл создать отдельную фабрику вместо повторения одного и того же кода повсюду.
