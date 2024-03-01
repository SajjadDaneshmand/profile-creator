import string
import json


class NumberFormats(object):
    def __init__(self, phonenumber):
        self.phonenumber = phonenumber.strip()
        self.letters = string.ascii_letters + string.punctuation

    def check_phonenumber_format(self):
        for num in self.phonenumber:
            if num in self.letters:
                return False
        if not self.phonenumber.startswith('09'):
            return False
        if len(self.phonenumber) != 11:
            return False
        return True

    def soroush_format(self):
        number_without_zero = self.phonenumber[1:]
        return '98' + number_without_zero

    def rubika_format(self):
        return self.phonenumber[1:]

    def eitaa_format(self):
        number_without_zero = self.phonenumber[1:]
        return '+98' + number_without_zero


def write_json(path, dictionary):
    with open(path, 'w') as jsonfile:
        json.dump(dictionary, jsonfile)


def load_json(path):
    with open(path, 'r') as json_file:
        return json.load(json_file)
