from abc import ABC, abstractmethod
import pickle
import json


#  Part 1
class SerializationInterface(ABC):

    @abstractmethod
    def save_to_file(self, data=None):
        pass

    @abstractmethod
    def load_from_file(self):
        pass


class SerializationPickle(SerializationInterface):

    def __init__(self, filename: str):
        self.filename = filename

    def save_to_file(self, data=None):
        with open(self.filename, "wb") as fh:
            pickle.dump(data, fh)

    def load_from_file(self):
        with open(self.filename, "rb") as fh:
            unpacked = pickle.load(fh)
        return unpacked


class SerializationJson(SerializationInterface):

    def __init__(self, filename: str):
        self.filename = filename

    def save_to_file(self, data=None):
        with open(self.filename, "w") as fh:
            json.dump(data, fh)

    def load_from_file(self):
        with open(self.filename, "r") as fh:
            unpacked = json.load(fh)
        return unpacked


# Part 2
class Meta(type):
    instances_created = 0

    def __new__(mcs, name, bases, namespace):
        instance = super().__new__(mcs, name, bases, namespace)
        instance.class_number = mcs.instances_created
        mcs.instances_created += 1
        return instance


if __name__ == "__main__":
    # part 1
    some_data = [0, (1, 2), "three", {"one": 1, "two": 2}]
    instance1 = SerializationPickle("data.dat")
    instance2 = SerializationJson("data.json")

    instance1.save_to_file(some_data)
    print(instance1.load_from_file())
    instance2.save_to_file(some_data)
    print(instance2.load_from_file())

    # part 2
    Meta.children_number = 0


    class Cls1(metaclass=Meta):
        def __init__(self, data):
            self.data = data


    class Cls2(metaclass=Meta):
        def __init__(self, data):
            self.data = data


    assert (Cls1.class_number, Cls2.class_number) == (0, 1)
    a, b = Cls1(''), Cls2('')
    assert (a.class_number, b.class_number) == (0, 1)
