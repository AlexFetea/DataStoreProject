from store import Store

class Client:
    def __init__(self, nodes):
        self.store = Store(nodes)

    def add(self, key, value):
        self.store.add(key, value)

    def get(self, key):
        return self.store.get(key)

    def delete(self, key):
        self.store.delete(key)
