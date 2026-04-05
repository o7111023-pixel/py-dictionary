class Node:
    def __init__(self, key, value):
        self.key = key
        self.hash = hash(key)
        self.value = value


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.capacity = 8
        self.hash_table = [[] for _ in range(self.capacity)]
        self.load_factor = 0.75

    def _get_index(self, key_hash: int) -> int:
        return key_hash % self.capacity

    def __setitem__(self, key, value) -> None:
        key_hash = hash(key)
        index = self._get_index(key_hash)
        bucket = self.hash_table[index]

        for node in bucket:
            if node.key == key:
                node.value = value
                return

        bucket.append(Node(key, value))
        self.length += 1

        if self.length / self.capacity > self.load_factor:
            self._resize()

    def __getitem__(self, key):
        key_hash = hash(key)
        index = self._get_index(key_hash)
        bucket = self.hash_table[index]

        for node in bucket:
            if node.key == key:
                return node.value

        raise KeyError(f"Key '{key}' not found")

    def __delitem__(self, key) -> None:
        key_hash = hash(key)
        index = self._get_index(key_hash)
        bucket = self.hash_table[index]

        for i, node in enumerate(bucket):
            if node.key == key:
                del bucket[i]
                self.length -= 1
                return

        raise KeyError(f"Key '{key}' not found")

    def __len__(self) -> int:
        return self.length

    def clear(self) -> None:
        self.hash_table = [[] for _ in range(self.capacity)]
        self.length = 0

    def _resize(self) -> None:
        old_table = self.hash_table
        self.capacity *= 2
        self.hash_table = [[] for _ in range(self.capacity)]
        self.length = 0

        for bucket in old_table:
            for node in bucket:
                self[node.key] = node.value
