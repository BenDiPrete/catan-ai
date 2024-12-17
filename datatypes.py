from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Tuple, TYPE_CHECKING

from enums import NodeStructure, Resource

if TYPE_CHECKING:
    from player import Player

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
    owner: Optional[Player] = None
    structure: NodeStructure = NodeStructure.NONE
    
@dataclass
class Edge:
    """Represents an edge on the board where a road can be placed."""
    id: int
    nodes: Tuple[Node, Node] = field(default_factory=list)
    tiles: List[Tile] = field(default_factory=list)
    owner: Optional[Player] = None
