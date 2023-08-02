import requests
import hashlib

class Store:
    def __init__(self, nodes, replication_factor=2):
        self.nodes = nodes
        self.replication_factor = replication_factor

    def hash_key(self, key):
        # Use the built-in hash function to get a hash of the key
        hashed = hashlib.md5(key.encode()).hexdigest()
        # Use the modulus to get a consistent node index
        node_index = int(hashed, 16) % len(self.nodes)
        return node_index

    def get_replicas(self, key):
        # Get the index of the node that the key hashes to
        index = self.hash_key(key)
        # Get the next replication_factor nodes
        return self.nodes[index:index+self.replication_factor]

    def add(self, key, value):
        nodes = self.get_replicas(key)
        for node in nodes:
            try:
                requests.post(f'http://{node}/', data={'key': key, 'value': value}, timeout=0.1)
            except requests.exceptions.RequestException:
                pass

    def get(self, key):
        nodes = self.get_replicas(key)
        for node in nodes:
            try:
                response = requests.get(f'http://{node}/?key={key}', timeout=0.1)
                if response.status_code == 200:
                    return response.text
            except requests.exceptions.RequestException:
                pass

    def delete(self, key):
        nodes = self.get_replicas(key)
        for node in nodes:
            try:
                requests.delete(f'http://{node}/?key={key}', timeout=0.1)
            except requests.exceptions.RequestException:
                pass