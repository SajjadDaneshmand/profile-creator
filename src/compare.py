import settings
import os


class Compare(object):
    def __init__(self, base_path, path2):
        self.base_path = base_path
        self.path2 = path2
        self._diff = []
        self._dirs = []
        self._files = []

    @property
    def exists(self):
        return self._logic()

    def _logic(self):
        for root, directories, files in os.walk(self.base_path):
            correct_path = self.path_correction(root, 'User Data')
            create_path2 = os.path.join(self.path2, correct_path)

            if os.path.exists(create_path2):
                self._diff.append(root)

            for file in files:
                file_path = os.path.join(root, file)
                create_filepath2 = os.path.join(self.path2, correct_path, file)

                if os.path.exists(create_filepath2):
                    self._diff.append(file_path)

        for things in self._diff:
            if os.path.isdir(things):
                self._dirs.append(things)

            elif os.path.isfile(things):
                self._files.append(things)

        return self._dirs, self._files

    @classmethod
    def path_correction(cls, path, word):
        path_components = path.split(os.path.sep)
        try:
            word_index = path_components.index(word)
            word_index += 1
            return os.path.sep.join(path_components[word_index:])

        except ValueError:
            return False

