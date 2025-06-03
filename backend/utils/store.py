import pickle

class Store:
    def __init__(self, file="data/store.pkl"):
        self.file = file
        self.data = {}
        self.load()

    def load(self):
        try:
            with open(self.file, "rb") as f:
                self.data = pickle.load(f)
        except (FileNotFoundError, EOFError):
            self.data = {}

    def save(self):
        with open(self.file, "wb") as f:
            pickle.dump(self.data, f)

    def get(self, key):
        return self.data.get(key)

    def set(self, key, value):
        self.data[key] = value
        self.save()