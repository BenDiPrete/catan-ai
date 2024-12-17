from typing import List, Mapping, Optional, Tuple

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe

from datatypes import Edge, Node, Tile
from enums import Resource

class Board:
    TILES_TO_NODES = [
        [0, 1, 2, 10, 9, 8],        # Tile 0
        [2, 3, 4, 12, 11, 10],      # Tile 1
        [4, 5, 6, 14, 13, 12],      # Tile 2
        [7, 8, 9, 19, 18, 17],      # Tile 3
        [9, 10, 11, 21, 20, 19],    # Tile 4
        [11, 12, 13, 23, 22, 21],   # Tile 5
        [13, 14, 15, 25, 24, 23],   # Tile 6
        [16, 17, 18, 29, 28, 27],   # Tile 7
        [18, 19, 20, 31, 30, 29],   # Tile 8
        [20, 21, 22, 33, 32, 31],   # Tile 9
        [22, 23, 24, 35, 34, 33],   # Tile 10
        [24, 25, 26, 37, 36, 35],   # Tile 11
        [28, 29, 30, 40, 39, 38],   # Tile 12
        [30, 31, 32, 42, 41, 40],   # Tile 13
        [32, 33, 34, 44, 43, 42],   # Tile 14
        [34, 35, 36, 46, 45, 44],   # Tile 15
        [39, 40, 41, 49, 48, 47],   # Tile 16
        [41, 42, 43, 51, 50, 49],   # Tile 17
        [43, 44, 45, 53, 52, 51],   # Tile 18
    ]
    
    TILE_LAYOUT = [3, 4, 5, 4, 3]
    NODE_LAYOUT = [7, 9, 11, 11, 9, 7]
    RESOURCE_NUMBERS = [2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 10, 10, 11, 11, 12]
    RESOURCES = (
        [Resource.WOOD] * 4
        + [Resource.BRICK] * 3
        + [Resource.SHEEP] * 4
        + [Resource.WHEAT] * 4
        + [Resource.ORE] * 3
        + [Resource.DESERT]
    )
    RESOURCE_COLOR_MAP = {
        Resource.WOOD: "forestgreen",
        Resource.BRICK: "firebrick",
        Resource.SHEEP: "greenyellow",
        Resource.WHEAT: "gold",
        Resource.ORE: "silver",
        Resource.DESERT: "lightyellow",
    }

    def __init__(self):
        self.tiles: List[Tile] = []
        self.edges: List[Edge] = []
        self.nodes: List[Node] = []
        self.node_neighbors: Mapping[int, List[int]] = {}
        
        self._create_structure()

    # def _create_structure(self):
    #     """
    #     Create the board structure with a fixed layout:
    #     - 19 tiles arranged in the standard Catan pattern.
    #     - 54 nodes and 72 edges interconnecting them.
        
    #     This method demonstrates the approach rather than fully enumerating 
    #     all connections (which can be quite verbose). You might want to 
    #     factor out data describing the standard board configuration.
    #     """
    #     self.nodes = [Node(id=i) for i in range(54)]
    #     self.edges = []

    #     # Create all tiles:
    #     resource_assignment = np.random.permutation(self.RESOURCES)
    #     number_assignment = np.random.permutation(self.RESOURCE_NUMBERS)
    #     seen_desert = False
    #     self.tiles = []
    #     for i in range(19):
    #         resource = resource_assignment[i]
    #         if resource == Resource.DESERT:
    #             seen_desert = True
    #             self.tiles.append(
    #                 Tile(id=i, resource=resource, number=0)
    #             )
    #             continue
    #         if seen_desert:
    #             number = number_assignment[i - 1]
    #         else:
    #             number = number_assignment[i]
    #         self.tiles.append(
    #             Tile(id=i, resource=resource, number=number)
    #         )
        
    #     # Now we link them all up
    #     for t_id, tile in enumerate(self.tiles):
    #         node_ids = self.TILES_TO_NODES[t_id]

    #         tile_nodes = [self.nodes[n_id] for n_id in node_ids]

    #         tile.nodes = tile_nodes

    #         for n in tile_nodes:
    #             n.tiles.append(tile)
    #         for i in range(len(node_ids)):
    #             n1 = tile_nodes[i]
    #             n2 = tile_nodes[(i + 1) % 6]
    #             if n1.id not in self.node_neighbors:
    #                 self.node_neighbors[n1.id] = []
    #             if n2.id not in self.node_neighbors:
    #                 self.node_neighbors[n2.id] = []
    #             if n2.id in self.node_neighbors[n1.id]:
    #                 edge_set = {n1.id, n2.id}
    #                 for edge in n1.edges:
    #                     a, b = edge.nodes
    #                     if {a.id, b.id} == edge_set:
    #                         edge.tiles.append(tile)
    #                         break
    #                 continue
    #             self.node_neighbors[n1.id].append(n2.id)
    #             self.node_neighbors[n2.id].append(n1.id)
    #             edge = Edge(id=len(self.edges), nodes=(n1, n2))
    #             edge.tiles.append(tile)
    #             tile.edges.append(edge)
                
    #             n1.edges.append(edge)
    #             n2.edges.append(edge)
    #             n1.tiles.append(tile)
    #             n2.tiles.append(tile)
    #             self.edges.append(edge)

    def _create_structure(self):
        self._create_nodes()
        self._create_tiles()
        self._link_tiles_nodes_and_edges()

    def _create_nodes(self):
        """Initialize nodes and related structures."""
        self.nodes = [Node(id=i) for i in range(54)]
        self.edges = []
        self.node_neighbors = {}

    def _create_tiles(self):
        """Randomly assign resources and numbers to tiles, including the desert tile."""
        resource_assignment = np.random.permutation(self.RESOURCES)
        number_assignment = np.random.permutation(self.RESOURCE_NUMBERS)
        seen_desert = False
        self.tiles = []
        for i in range(19):
            resource = resource_assignment[i]
            if resource == Resource.DESERT:
                seen_desert = True
                self.tiles.append(Tile(id=i, resource=resource, number=0))
                continue
            number = number_assignment[i - 1] if seen_desert else number_assignment[i]
            self.tiles.append(Tile(id=i, resource=resource, number=number))

    def _link_tiles_nodes_and_edges(self):
        """Link tiles to their nodes and create edges between nodes."""
        for t_id, tile in enumerate(self.tiles):
            node_ids = self.TILES_TO_NODES[t_id]
            tile.nodes = [self.nodes[n_id] for n_id in node_ids]

            # Assign tile references to nodes
            for node in tile.nodes:
                node.tiles.append(tile)

            # Create or link edges between these nodes
            for i in range(len(node_ids)):
                n1 = tile.nodes[i]
                n2 = tile.nodes[(i + 1) % 6]

                if n1.id not in self.node_neighbors:
                    self.node_neighbors[n1.id] = []
                if n2.id not in self.node_neighbors:
                    self.node_neighbors[n2.id] = []

                if n2.id in self.node_neighbors[n1.id]:
                    # Edge already exists; add this tile to it
                    edge_set = {n1.id, n2.id}
                    for edge in n1.edges:
                        a, b = edge.nodes
                        if {a.id, b.id} == edge_set:
                            edge.tiles.append(tile)
                            tile.edges.append(edge)
                            break
                else:
                    # Create a new edge
                    self.node_neighbors[n1.id].append(n2.id)
                    self.node_neighbors[n2.id].append(n1.id)
                    edge = Edge(id=len(self.edges), nodes=(n1, n2))
                    edge.tiles.append(tile)
                    tile.edges.append(edge)

                    n1.edges.append(edge)
                    n2.edges.append(edge)
                    n1.tiles.append(tile)
                    n2.tiles.append(tile)
                    self.edges.append(edge)

                
    def _get_row_col_from_idx(self, idx: int, layout: List[int]) -> Tuple[int, int]:
        for row, amt in enumerate(layout):
            if idx < amt:
                col = idx
                return row, col
            idx -= amt

    def _get_idx_from_row_col(self, row: int, col: int, layout: List[int]) -> int:
        return sum(layout[:row]) + col

    def _get_node_coords(self, idx: int) -> Tuple[float, float]:
        for i, amt in enumerate(self.NODE_LAYOUT):
            if idx < amt:
                x = idx - (amt // 2)
                y = ((len(self.NODE_LAYOUT) - 1) / 2) - i
                y *= 3 / np.sqrt(3)
                if y > 0:
                    vertical_offset = 1 / (2 * np.sqrt(3))
                else:
                    vertical_offset = -1 / (2 * np.sqrt(3))
                if idx % 2 == 0:
                    y -= vertical_offset
                else:
                    y += vertical_offset
                return x, y
            idx -= amt

    def _get_tile_coords(self, idx: int) -> Tuple[float, float]:
        for i, amt in enumerate(self.TILE_LAYOUT):
            if idx < amt:
                x = (idx - ((amt - 1) / 2)) * 2
                y = 2 - i
                y *= 3 / np.sqrt(3)
                return x, y
            idx -= amt

    def plot(self, show_ids: bool = False):
        plt.figure(figsize=(8, 8))
        for edge in self.edges:
            node_a, node_b = edge.nodes
            id_a, id_b = node_a.id, node_b.id
            x_a, y_a = self._get_node_coords(id_a)
            x_b, y_b = self._get_node_coords(id_b)
            if edge.owner:
                #plt.plot([x_a, x_b], [y_a, y_b], c=edge.owner.color, lw=3, zorder=0, edgecolor='black')
                plt.plot([x_a, x_b], [y_a, y_b], color=edge.owner.color, lw=3, path_effects=[pe.Stroke(linewidth=5, foreground='black'), pe.Normal()], zorder=0)
            else:
                plt.plot([x_a, x_b], [y_a, y_b], c='black', zorder=0)
            if show_ids:
                x_mid = (x_a + x_b) / 2
                y_mid = (y_a + y_b) / 2
                plt.annotate(edge.id, (x_mid, y_mid), textcoords="offset points", xytext=(5,5), ha='center')
        for i, node in enumerate(self.nodes):
            x, y = self._get_node_coords(i)
            if node.owner:
                plt.scatter([x], [y], c=node.owner.color, zorder=1, s=100, edgecolor='black')
            else:
                plt.scatter([x], [y], c='white', zorder=1, s=75, edgecolor='black')
            if show_ids:
                plt.annotate(i, (x, y), textcoords="offset points", xytext=(5,5), ha='center')
        for i, tile in enumerate(self.tiles):
            x, y = self._get_tile_coords(i)
            tile_color = self.RESOURCE_COLOR_MAP[tile.resource]
            vtx_coords = np.array([self._get_node_coords(node.id) for node in tile.nodes + [tile.nodes[0]]])
            plt.fill(vtx_coords[:, 0], vtx_coords[:, 1], c=tile_color, zorder=-1)
            if tile.resource == Resource.DESERT:
                continue
            plt.scatter([x], [y], c="white", zorder=1, s=600, edgecolor='black')
            number = tile.number
            if number in [6, 8]:
                c = "red"
            else:
                c = "black"
            plt.annotate(number, (x, y), c=c, textcoords="offset points", xytext=(0,-4), ha='center')
        plt.xlim(-6, 6)
        plt.ylim(-6, 6)
        plt.axis('off')
        plt.show()

    def get_tile_by_id(self, tile_id: int) -> Optional[Tile]:
        return self.tiles[tile_id] if 0 <= tile_id < len(self.tiles) else None

    def get_node_by_id(self, node_id: int) -> Optional[Node]:
        return self.nodes[node_id] if 0 <= node_id < len(self.nodes) else None

    def get_edge_by_id(self, edge_id: int) -> Optional[Edge]:
        return self.edges[edge_id] if 0 <= edge_id < len(self.edges) else None