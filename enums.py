from enum import Enum

class Resource(Enum):
    WOOD = 0
    BRICK = 1
    SHEEP = 2
    WHEAT = 3
    ORE = 4
    DESERT = 5

class NodeStructure(Enum):
    NONE = 0
    SETTLEMENT = 1
    CITY = 2
