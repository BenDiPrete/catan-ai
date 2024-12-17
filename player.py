from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional

from datatypes import Resource
from enums import NodeStructure
from game import Game

class Player(ABC):
	"""Abstract Player class. Different player types must implement 'take_turn'."""
	def __init__(self, name: str, color: str):
		self.name = name
		self.color = color
		self.resources = {
			Resource.WOOD: 0,
			Resource.BRICK: 0,
			Resource.SHEEP: 0,
			Resource.WHEAT: 0,
			Resource.ORE: 0
		}
		self.points = 0
		# Additional fields like settlements, roads, etc., would go here

	@abstractmethod
	def take_turn(self, game: Game):
		"""Implement logic for a single turn. 
		The 'game' object is provided so the player can query the board state."""
		pass
	
	@abstractmethod
	def place_initial_settlement_and_road(self, game: Game):
		"""Implement logic for placing one initial settlement and one adjacent road.
		This is part of the initial setup phase."""
		pass

class HumanPlayer(Player):
	"""A human player who is prompted for actions in the console or via a GUI."""
	def take_turn(self, game: Game):
		# This could be replaced with actual input handling:
		# For a console-based approach:
		print(f"{self.name}, it's your turn!")
		# For demonstration, we'll say the human does nothing special
		# In a real implementation, you'd prompt for moves, trades, builds, etc.
		pass
	
	def place_initial_settlement_and_road(self, game: Game):
		"""Implement logic for placing one initial settlement and one adjacent road.
		This is part of the initial setup phase."""
		settlement_location = int(input(f"Current player: {self.name}. Choose a node for your initial settlement: "))
		road_location = int(input(f"Current player: {self.name} Choose an adjacent road: "))
		game._add_structure(settlement_location, NodeStructure.SETTLEMENT, self)
		game._add_road(road_location, self)
		# In a real implementation, you'd validate these choices
		# and update the board state accordingly

class AIPlayer(Player):
	"""An AI player that uses heuristics or other logic to decide moves."""
	def take_turn(self, game: Game):
		# Implement AI logic:
		# For now, just print that the AI is taking a turn
		print(f"{self.name} (AI) is thinking...")

		# Example heuristic: If AI can build a settlement, do so:
		# (The details of checking resources and board state would be more complex.)
		# For now, just a placeholder:
		pass

	def place_initial_settlement_and_road(self, game: Game):
		"""Implement logic for placing one initial settlement and one adjacent road.
		This is part of the initial setup phase."""
		pass