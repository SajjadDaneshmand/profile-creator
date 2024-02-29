import shutil

import settings
from compare import Compare
import re
import os


class Folders(object):
    def __init__(self, path):
        self.path = path

        self.compare = Compare(settings.CHROME_PATH, settings.INSTANCE_PATH)

        self.pattern = r'^پروفایل شماره (.+)$'
        self.nums_dict = {
            '۱': '1',
            '۲': '2',
            '۳': '3',
            '۴': '4',
            '۵': '5',
            '۶': '6',
            '۷': '7',
            '۸': '8',
            '۹': '9',
            '۰': '0'
        }

        self.base_folder = os.path.join(self.path, self.get_name(), 'Chrome')

    def raw_profile(self):
        self.create_base_folder()
        self.create_folders()
        self.copy_files()

    def create_folders(self):
        for directory in self.compare.exists[0]:
            correct_dir = self.compare.path_correction(directory, settings.BASE_CHROME_NAME)
            dir_creation = os.path.join(self.base_folder, correct_dir)
            if not os.path.exists(dir_creation):
                try:
                    os.makedirs(dir_creation)
                except FileNotFoundError:
                    pass
        return True

    def copy_files(self):
        for files in self.compare.exists[1]:
            correct_file = self.compare.path_correction(files, settings.BASE_CHROME_NAME)
            try:
                shutil.copy(files, os.path.join(self.base_folder, correct_file))
            except PermissionError:
                pass

    def create_base_folder(self):
        os.makedirs(self.base_folder, exist_ok=True)
        return True

    def get_name(self):
        return 'پروفایل شماره' + ' ' + self.correct_folder_number(self.path)

    def correct_folder_number(self, path):
        pattern = r'^پروفایل شماره (.+)$'
        files = os.listdir(path)
        folder_nums = []
        for file in files:
            match = re.search(pattern, file)
            if match is not None:
                persian_num = match.group(1)
                eng_num = self.convert_num(self.nums_dict, persian_num)
                folder_nums.append(eng_num)

        folder_nums = [int(num) for num in folder_nums]
        folder_nums.sort()
        final_num = str(folder_nums[-1] + 1)
        return self.convert_num(self.revert_dict(self.nums_dict), final_num)

    @staticmethod
    def convert_num(dictionary: dict, persian_num: str):
        str_num = ''
        for char in persian_num:
            str_num += dictionary[char]
        return str_num

    @staticmethod
    def revert_dict(dictionary):
        reverted_dict = dict()
        for key, value in dictionary.items():
            reverted_dict[value] = key
        return reverted_dict
