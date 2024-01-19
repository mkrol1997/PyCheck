from typing import List, Tuple

from checkers_app.game_engine import game_engine
from checkers_app.game_engine.game import Game


class MCTSNode:
    def __init__(self, state: Game, parent: Game = None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.value = 0
        self.untried_actions = self._get_unexplored_actions()

    def _get_unexplored_actions(self) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        unexplored_moves = []
        game_engine.update_pawns_with_legal_moves(game=self.state)

        if self.state.captures:
            for from_coords in self.state.captures:
                for to_coords in self.state.captures[from_coords].keys():
                    unexplored_moves.append((from_coords, to_coords))
        elif self.state.basic_moves:
            for from_coords in self.state.basic_moves:
                for to_coords in self.state.basic_moves[from_coords]:
                    unexplored_moves.append((from_coords, to_coords))

        return unexplored_moves
