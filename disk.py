import json
import os.path


class Disk:
    data = {}
    
    def __init__(self, name):
        self.name = name
        self.load()

    def __iter__(self):
        with open(f"{self.name}.json", "r") as file:
            data = json.load(file)
            for key in data:
                yield key

    def add_item(self, key, value):
        self.data[key] = value
        self.save()
        return f"{value} added"

    def delete_item(self, key):
        self.data.pop(key)
        self.save()
        return f"{key} deleted"

    def get_item(self, key):
        return self.data[key]

    def save(self):
        with open(f"{self.name}.json", "w") as file:
            json.dump(self.data, file)

    def load(self):
        if not os.path.exists(f"{self.name}.json"):
            self.save()
        self.save()
        with open(f"{self.name}.json", "r+") as file:
            self.data = json.load(file)

    def exit(self):
        self.data = {}
        os.remove(f"{self.name}.json")
        self.name = None

    def items(self):
        return str(self.data)

    def keys(self):
        if not self.data.keys():
            return "[]"
        return " ".join(map(str, list(self.data.keys())))

    def values(self):
        if not self.data.values():
            return "[]"
        return " ".join(map(str, list(self.data.values())))
