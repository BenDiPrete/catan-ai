from __future__ import annotations

import random
from typing import List, Optional, TYPE_CHECKING

from IPython.display import clear_output

from board import Board
# from datatypes import Resource
from enums import NodeStructure

if TYPE_CHECKING:
    from player import Player

class Game:
    def __init__(self, board: Board, players: List[Player], plot_board: bool = False, clear_plots: bool = False):
        self.board = board
        self.players = players.copy()
        random.shuffle(players)
        self.plot_board = plot_board
        self.clear_plots = clear_plots
        self.current_player_index = 0
        self.turn_count = 0
        self.game_over = False

    def roll_dice(self) -> int:
        return random.randint(1, 6) + random.randint(1, 6)

    def produce_resources(self, roll: int):
        # For each tile that has this roll number, give resources to players 
        # who have a settlement on adjacent nodes.
        for tile in self.board.tiles:
            if tile.number == roll:
                # Find players who have settlements at adjacent nodes (not implemented yet)
                for node in tile.nodes:
                    # If a node is owned by a player, give them the resource.
                    if node.owner:
                        if node.structure == NodeStructure.SETTLEMENT:
                            node.owner.resources[tile.resource] += 1
                        elif node.structure == NodeStructure.CITY:
                            node.owner.resources[tile.resource] += 2
                        else:
                            raise ValueError("Unexpected node structure")

    def check_win_condition(self) -> Optional[Player]:
        # Check if any player meets the victory condition (e.g., 10 points in standard Catan)
        for player in self.players:
            if player.points >= 10:
                return player
        return None

    def play_turn(self):
        if self.game_over:
            return
        current_player = self.players[self.current_player_index]

        # 1. Roll dice and produce resources
        roll = self.roll_dice()
        self.produce_resources(roll)

        # 2. Player takes turn
        current_player.take_turn(self)

        # 3. Check win condition
        winner = self.check_win_condition()
        if winner:
            print(f"{winner.name} wins the game!")
            self.game_over = True
            return

        # Move to the next player
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        self.turn_count += 1

    def play_game(self):
        # A simple loop to play until there is a winner:
        if self.plot_board:
            self._plot_board()

        self._run_starting_phase()

        # while not self.game_over:
        #     self.play_turn()

    def _run_starting_phase(self):
        # Place initial settlements and roads
        for player in self.players:
            player.place_initial_settlement_and_road(self)
            if self.plot_board:
                self._plot_board()
        
        # Reverse order for second settlement placement
        for player in reversed(self.players):
            player.place_initial_settlement_and_road(self)
            if self.plot_board:
                self._plot_board()

    def _add_structure(self, node_id: int, structure: NodeStructure, player: Player):
        # Helper method to add a structure to a node
        node = self.board.get_node_by_id(node_id)
        node.structure = structure
        node.owner = player

    def _add_road(self, edge_id: int, player: Player):
        # Helper method to add a road to an edge
        edge = self.board.get_edge_by_id(edge_id)
        edge.owner = player

    def _plot_board(self):
        # Helper method to plot the board
        if self.clear_plots:
            #print("Clearing Output")
            clear_output()
        self.board.plot()
