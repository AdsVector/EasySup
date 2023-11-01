import json
from enum import Enum

class JSON_Manager:
    class Modes(Enum):
        DEFAULT = 0,
        APPEND  = 1

    def __init__(self, file_path):
        self.filename = file_path
        self.data = None
        self.read_file()
    
    def read_file(self):
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}
        self.data = data
    
    def write_file(self):
        with open(self.filename, 'w') as f:
            json.dump(self.data, f, indent=4)

    def add_element(self, keys, element, mode = Modes.DEFAULT):
        self.read_file()
        target = self.data
        for key in keys[:-1]:
            if key not in target:
                target[key] = {}
            target = target[key]

        if (mode == self.Modes.DEFAULT):
            target[keys[-1]] = element
        elif (mode == self.Modes.APPEND):
            if keys[-1] not in target:
                target[keys[-1]] = []
            target[keys[-1]].append(element)
        self.write_file()
        

    def update_element(self, keys, field, value):
        self.read_file()
        target = self.data
        for key in keys[:-1]:
            if key not in target:
                return False
            target = target[key]

        if field not in target[keys[-1]]:
            return False
        target[keys[-1]][field] = value
        self.write_file()
            
        return True        
    
    def delete_elements(self, keys, elements, field=None, mode = Modes.DEFAULT):
        self.read_file()
        target = self.data
        for key in keys[:-1]:
            if key not in target:
                return False
            target = target[key]

        count = 0
        next  = 0
        while count < len(elements):
            if mode == self.Modes.DEFAULT:
                del target[keys[-1]][elements[count]]
                count +=1
            elif mode == self.Modes.APPEND:
                element = target[keys[-1]][next]
                if not field or (field in element and element[field] in elements):
                    target[keys[-1]].remove(element)
                    count +=1
                    next = 0
                else: next += 1
    
        self.write_file()
        return True
    
    def count(self, keys):
        data = self.data
        for key in keys:
            if key not in data:
                return 0
            data = data[key]
        return len(data)