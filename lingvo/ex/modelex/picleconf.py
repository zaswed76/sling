import pickle


class PConfig:
    def __init__(self, path):
        self.path = path
        self.__data = {}

    def load(self):
        with open(self.path, 'rb') as f:
            self.__data = pickle.load(f)
        return self.__data

    def save(self, data):
        self.__data = data
        with open(self.path, 'wb') as f:
            pickle.dump(self.__data, f)

    @property
    def data(self):
        return self.__data