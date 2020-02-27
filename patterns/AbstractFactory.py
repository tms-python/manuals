import json
from abc import ABC, abstractmethod


class AbstractDoor(ABC):

    @abstractmethod
    def get_description(self):
        pass

    @abstractmethod
    def create_door(self, width: int, height: int):
        pass


class WoodenDoor(AbstractDoor):
    __width = None
    __height = None

    def __init__(self, width: int, height: int):
        self.create_door(width=width, height=height)

    def create_door(self, width: int, height: int):
        self.__width = width
        self.__height = height

    def get_description(self):
        return f'Wooden door. width = {self.__width}mm and height = {self.__height}mm'


class IronDoor(AbstractDoor):
    __width = None
    __height = None

    def __init__(self, width: int, height: int):
        self.create_door(width=width, height=height)

    def create_door(self, width: int, height: int):
        self.__width = width / 25.4
        self.__height = height / 25.4

    def get_description(self):
        return f'Iron door. width = {self.__width}inch and height = {self.__height}inch'


class DoorMaster(ABC):

    @abstractmethod
    def install_door(self):
        pass

    @abstractmethod
    def check_door_type(self):
        pass


class WoodenDoorMaster(DoorMaster):
    __door = None

    def __init__(self, door: WoodenDoor):
        self.__door = door
        self.check_door_type()

    def install_door(self):
        return f'{self.__door.get_description()} was installed'

    def check_door_type(self):
        if type(self.__door) != WoodenDoor:
            raise TypeError('Door type is wrong')


class IronDoorMaster(DoorMaster):
    __door = None

    def __init__(self, door: IronDoor):
        self.__door = door
        self.check_door_type()

    def install_door(self):
        return f'{self.__door.get_description()} was installed'

    def check_door_type(self):
        if type(self.__door) != IronDoor:
            raise TypeError('Door type is wrong')


class AbstractDoorFactory(ABC):
    @abstractmethod
    def make_door(self, width: int, height: int):
        pass

    @abstractmethod
    def make_door_master(self, door: AbstractDoor):
        pass

    @abstractmethod
    def get_door(self):
        pass

    @abstractmethod
    def get_door_master(self):
        pass


class WoodenDoorFactory(AbstractDoorFactory):
    __door = None
    __door_master = None

    def __init__(self, width: int, height: int):
        self.__door = self.make_door(width, height)
        self.__door_master = self.make_door_master(self.__door)

    def make_door(self, width: int, height: int):
        return WoodenDoor(width=width, height=height)

    def make_door_master(self, door: WoodenDoor):
        return WoodenDoorMaster(door=door)

    def get_door(self):
        return self.__door

    def get_door_master(self):
        return self.__door_master


class IronDoorFactory(AbstractDoorFactory):
    __door = None
    __door_master = None

    def __init__(self, width: int, height: int):
        self.__door = self.make_door(width, height)
        self.__door_master = self.make_door_master(self.__door)

    def make_door(self, width: int, height: int):
        return IronDoor(width=width, height=height)

    def make_door_master(self, door: IronDoor):
        return IronDoorMaster(door=door)

    def get_door(self):
        return self.__door

    def get_door_master(self):
        return self.__door_master

# door = IronDoor(100, 1000)

# print(door.get_description())


iron_door_factory = IronDoorFactory(900, 2005)
print(iron_door_factory.get_door().get_description())
print(iron_door_factory.get_door_master().install_door())


wooden_door_factory = WoodenDoorFactory(900, 2005)
print(wooden_door_factory.get_door().get_description())
print(wooden_door_factory.get_door_master().install_door())