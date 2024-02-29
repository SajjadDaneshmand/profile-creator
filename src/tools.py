import string


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

