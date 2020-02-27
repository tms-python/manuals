from abc import ABC, abstractmethod

# Представим, что у вас есть сайт с разными страницами,
# и вам надо разрешить пользователям менять их тему.
# Что вы будете делать? Создавать множественные копии каждой
#  страницы для каждой темы или просто отдельную тему,
# которую пользователь сможет выбрать сам?
# Шаблон мост позволяет вам сделать второе.


class AbstractWebPage(ABC):

    @abstractmethod
    def get_content(self):
        pass


class About(AbstractWebPage):
    __theme = None

    def __init__(self, theme: 'AbstractTheme'):
        self.__theme = theme

    def get_content(self):
        return f'Страница с информацией в {self.__theme.get_color()}'


class Vacancy(AbstractWebPage):
    __theme = None

    def __init__(self, theme: 'AbstractTheme'):
        self.__theme = theme

    def get_content(self):
        return f'Страница вакансий в {self.__theme.get_color()}'


class AbstractTheme(ABC):
    @abstractmethod
    def get_color(self):
        pass


class DarkTheme(AbstractTheme):

    def get_color(self):
        return 'Dark Theme'


class LightTheme(AbstractTheme):

    def get_color(self):
        return 'Light Theme'


dark_theme = DarkTheme()
light_theme = LightTheme()


about = About(dark_theme)
vacancy = Vacancy(dark_theme)

print(about.get_content())
print(vacancy.get_content())

about = About(light_theme)
vacancy = Vacancy(light_theme)

print(about.get_content())
print(vacancy.get_content())