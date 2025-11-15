"""Controller module for predicting actions"""
from abc import ABC, abstractmethod
from sim.action import Action


class Controller(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def predict(self) -> Action:
        pass

