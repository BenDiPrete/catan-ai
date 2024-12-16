from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Mapping, Optional, Tuple

import numpy as np
import numpy.typing as npt

class Resource(Enum):
    WOOD = 0
    BRICK = 1
    SHEEP = 2
    WHEAT = 3
    ORE = 4
    DESERT = 5

@dataclass
class Tile:
    """Represents a single hex tile on the board."""
    id: int
    resource: Resource
    number: int
    nodes: List[Node] = field(default_factory=list)
    edges: List[Edge] = field(default_factory=list)

@dataclass
class Node:
    """Represents a vertex on the board where up to three tiles meet."""
    id: int
    edges: List[Edge] = field(default_factory=list)
    tiles: List[Tile] = field(default_factory=list)
    
@dataclass
class Edge:
    """Represents an edge on the board where a road can be placed."""
    id: int
    nodes: Tuple[Node] = field(default_factory=list)
    tiles: List[Tile] = field(default_factory=list)
