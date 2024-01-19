import copy
import math
import random
from typing import List, Tuple

from checkers_app.game_engine import game_engine
from checkers_app.game_engine.game import Game
from checkers_app.mcts.node import MCTSNode
from constant import SIMULATION_DEPTH


class MonteCarloTreeSearch:
    def __init__(self, initial_state: Game, exploration_constant: float = 1.41, iterations: int = 1000) -> None:
        self.root = MCTSNode(initial_state)
        self.exploration_constant = exploration_constant
        self.iterations = iterations

    def run(self) -> MCTSNode:
        for _ in range(self.iterations):
            selected_node = self._select(self.root)
            result = self._simulate(selected_node.state)
            self._backpropagate(selected_node, result)
        return self._best_child(self.root)

    def _select(self, node: MCTSNode) -> MCTSNode:
        while not self._is_terminal(node.state):
            if not self._fully_expanded(node):
                return self._expand(node)
            else:
                node = self._best_uct(node)
        return node

    def _expand(self, node: MCTSNode) -> MCTSNode:
        action = node.untried_actions.pop()
        new_state = self._perform_action(node.state, action)
        child_node = MCTSNode(new_state, parent=node)
        node.children.append(child_node)
        return child_node

    def _simulate(self, state: Game) -> int:
        simulation_moves = 0
        current_state = state
        while not self._is_terminal(current_state) and simulation_moves < SIMULATION_DEPTH:
            action = random.choice(self._get_all_actions(current_state))
            current_state = self._perform_action(current_state, action)
            simulation_moves += 1
        return self._get_result(current_state)

    def _best_uct(self, node: MCTSNode) -> MCTSNode:
        uct_values = [
            child.value / child.visits + self.exploration_constant * math.sqrt(math.log(node.visits / child.visits))
            if child.visits > 0
            else float("-inf")
            for child in node.children
        ]
        return node.children[uct_values.index(max(uct_values))]

    def _is_terminal(self, state: Game) -> bool:
        return not self._get_all_actions(state)

    @staticmethod
    def _fully_expanded(node: MCTSNode) -> bool:
        return not node.untried_actions

    @staticmethod
    def _backpropagate(node: MCTSNode, result: int) -> None:
        while node:
            node.visits += 1
            node.value += result
            node = node.parent

    @staticmethod
    def _best_child(node: MCTSNode) -> MCTSNode:
        def score(child_node: MCTSNode) -> float:
            if child_node.value == 0:
                return float("-inf")
            return child_node.visits / child_node.value

        return max(node.children, key=score)

    @staticmethod
    def _get_all_actions(state: Game) -> List[Tuple[int, int]]:
        all_actions = []
        game_engine.update_pawns_with_legal_moves(game=state)

        if state.captures:
            for from_coords in state.captures:
                for to_coords in state.captures[from_coords].keys():
                    all_actions.append((from_coords, to_coords))
        elif state.basic_moves:
            for from_coords in state.basic_moves:
                for to_coords in state.basic_moves[from_coords]:
                    all_actions.append((from_coords, to_coords))
        return all_actions

    @staticmethod
    def _perform_action(state: Game, action: Tuple[int, int]) -> Game:
        from_cords, to_cords = action
        current_state = copy.deepcopy(state)

        game_engine.move_pawn(current_state, from_cords, to_cords)

        if from_cords in current_state.captures.keys():
            capture_pawn_cords = current_state.captures[from_cords][to_cords]
            game_engine.make_pawn_capture(current_state, capture_pawn_cords)

        game_engine.switch_active_player(current_state)
        return current_state

    @staticmethod
    def _get_result(state: Game) -> int:
        white_pawns = sum(1 for row in state.board.matrix for pawn in row if pawn.value == -1)
        black_pawns = sum(1 for row in state.board.matrix for pawn in row if pawn.value == 1)

        if black_pawns:
            return 2
        elif white_pawns:
            return -2

        return white_pawns - black_pawns
