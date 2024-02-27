import abc
from abc import ABC,abstractmethod

class Prompt(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def format(self):
        raise NotImplementedError
    
    def __call__(self,*args,**kwargs):
        return self.format(*args,**kwargs)
    
