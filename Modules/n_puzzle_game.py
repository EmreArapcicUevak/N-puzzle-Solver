from Modules.Search_Problem.search_problem import Search_Problem
from Modules.Search_Problem.node import Node
import numpy as np


# The state is represented by an array, where the empty tile is denoted by 0 and other tiles are denoted 1-N
class N_Puzzle_Problem(Search_Problem):
    def __init__(self, board_dim : int, initial_state : tuple, goal_state : tuple):
        super().__init__(initial_state)
        self.goal_state = goal_state
        self.board_dim = board_dim
        self.n = board_dim ** 2

        assert set(initial_state) == set(range(self.n)), "Invalid initial state."
        assert set(goal_state) == set(range(self.n)), "Invalid goal state."
        assert len(initial_state) == self.n, "Initial state length mismatch."
        assert len(goal_state) == self.n, "Goal state length mismatch."

    def IS_GOAL(self, state):
        # Check if the current state is the goal state
        return np.array_equal(state, self.goal_state)

    def ACTIONS(self, state : tuple):
        actions = []
        board_limit = self.board_dim - 1

        x, y = self._translate_position(state.index(0))  # Find the position of the empty tile (0)
        if x > 0: actions.append("left")
        if x < board_limit: actions.append("right")

        if y > 0: actions.append("up")
        if y < board_limit: actions.append("down")

        return actions

    def RESULT(self, state, action):
        # Return the resulting state after applying the action
        pass
    
    def ACTION_COST(self, state, action, new_state):
        # Return the cost of the action (uniform cost in this case)
        return 1

    def _translate_position(self, pos):
        # Translate a 1D position to 2D coordinates
        assert 0 <= pos < self.n, "Invalid position."
        return (pos % self.board_dim, pos // self.board_dim)
