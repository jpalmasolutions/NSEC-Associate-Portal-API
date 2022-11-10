from jsons import JsonSerializable
from abc import ABC,abstractclassmethod

class Model(ABC,JsonSerializable):

    @abstractclassmethod
    def assign_id(self) -> None:
        pass