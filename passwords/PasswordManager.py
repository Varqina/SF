from random import randint

from data.DataManager import load_file, save_data
from passwords.password_list import add_passwords


class PasswordManager:
    def __init__(self):
        self.passwords = list(load_file('passwords'))
        add_passwords(self.passwords)
        save_data('passwords', self.passwords)

    def get_password(self):
        key = randint(0, len(self.passwords) - 1)
        self.passwords.append(self.passwords.pop(key))
        return self.passwords[key]
