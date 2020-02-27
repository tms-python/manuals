from multiprocessing import Lock


class SingletonMeta(type):
    # экземпляр класса, одна единственная сущность!
    __instance = None
    # блокировка при обращении потока к классу
    __lock = Lock()

    def __call__(self, *args, **kwargs):
        # захват блокировки
        with self.__lock:
            # проверяем на наличие экземпляра класса
            if self.__instance is None:
                # если первый первая попытка создать экземпляр класса
                self.__instance = super(SingletonMeta, self).__call__(*args, **kwargs)
        return self.__instance


class Singleton(metaclass=SingletonMeta):
    #  тут может быть любая логика
    pass


first = Singleton()
print(id(first))
second = Singleton()
print(id(second))
third = Singleton()
print(id(third))

