from random import randint, choices, choice, shuffle
from string import ascii_lowercase, ascii_uppercase, digits


class Password:
    @staticmethod
    def get_password() -> str:
        """
        Generates a 6-20 character password.

        :return: Ready password.
        """

        password_length = randint(6, 20)
        special_symbols = ['@', '!', '№', '#', '%', '^', ',', '.', ';', ':', ')', '(', '?', '/', ']', '[']
        all_symbols = ascii_lowercase + ascii_uppercase + digits + ''.join(special_symbols)

        password = choices(all_symbols, k=password_length-4)
        password.append(choice(ascii_uppercase))
        password.append(choice(ascii_lowercase))
        password.append(choice(digits))
        password.append(choice(special_symbols))
        shuffle(password)

        return ''.join(password)
