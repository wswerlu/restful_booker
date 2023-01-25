from mimesis import Person


class UserData:

    def __init__(self):
        self.person = Person('ru')

    def firstname(self) -> str:
        """
        Генерация имени.
        """
        return self.person.name()

    def lastname(self) -> str:
        """
        Генерация фамилии.
        """
        return self.person.last_name()
