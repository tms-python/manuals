from abc import ABC, abstractmethod

# структурный шаблон проектирования, предназначенный для организации
# использования функций объекта,
# недоступного для модификации, через специально созданный интерфейс.
# Шаблон позволяет обернуть несовместимые объекты в адаптер, чтобы сделать их совместимыми с другим классом.
# Обратимся к коду. Представим игру, в которой охотник охотится на львов.


class AbstractLion(ABC):

    @abstractmethod
    def roar(self):
        pass


class AsianLion(AbstractLion):

    def roar(self):
        pass

    def __str__(self):
        return 'Asian Lion'


class AfricanLion(AbstractLion):

    def roar(self):
        pass

    def __str__(self):
        return 'African Lion'


class Hunter:
    def hunt(self, lion: AbstractLion):
        if isinstance(lion, AbstractLion):
            print(f'Hunt to {lion}')
        else:
            raise TypeError('lion is not inherit AbstractLion')


# Теперь представим, что нам надо добавить WildDog в нашу игру,
# на которую наш Hunter также мог бы охотиться

class WildDog:
    def bark(self):
        pass

    def __str__(self):
        return 'Wild Dog'


class WildDogAdapter(AbstractLion):
    __dog = None

    def __init__(self, dog: WildDog):
        self.__dog = dog

    def roar(self):
        self.__dog.bark()

    def __str__(self):
        return self.__dog.__str__()



# class

asian_lion = AsianLion()
african_lion = AfricanLion()

wild_dog = WildDog()

hunter = Hunter()
hunter.hunt(asian_lion)
hunter.hunt(african_lion)
try:
    hunter.hunt(wild_dog)
except TypeError as e:
    print(f'Exception: {TypeError} {e}')


wild_dog = WildDogAdapter(wild_dog)
hunter.hunt(wild_dog)