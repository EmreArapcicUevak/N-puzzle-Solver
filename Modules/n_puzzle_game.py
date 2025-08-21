from Modules.Search_Problem.search_problem import Search_Problem
from Modules.Search_Problem.node import Node
from Modules.Search_Problem.expand import expand
from Modules.que import Priority_Que
from typing import Callable

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
        #print(f"Checking if {state} is goal state.")
        return state == self.goal_state

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
      empty_index = state.index(0)
      x, y = self._translate_position(empty_index)

      # Compute new coordinates based on action
      if action == "left":
          new_x, new_y = x - 1, y
      elif action == "right":
          new_x, new_y = x + 1, y
      elif action == "up":
          new_x, new_y = x, y - 1
      elif action == "down":
          new_x, new_y = x, y + 1
      else:
          raise ValueError(f"Invalid action: {action}")

      # Convert back to 1D index
      swap_index = self._translate_index(new_x, new_y)

      # Create new tuple with swapped values
      state_list = list(state)   # convert tuple → list
      state_list[empty_index], state_list[swap_index] = state_list[swap_index], state_list[empty_index]
      return tuple(state_list)   # back to tuple
    
    def ACTION_COST(self, state, action, new_state):
        # Return the cost of the action (uniform cost in this case)
        return 1

    def _translate_position(self, pos):
        # Translate a 1D position to 2D coordinates
        assert 0 <= pos < self.n, "Invalid position."
        return (pos % self.board_dim, pos // self.board_dim)

    def _translate_index(self, x : int, y : int) -> int:
        # Translate 2D coordinates to a 1D position
        assert 0 <= x < self.board_dim and 0 <= y < self.board_dim, "Invalid position."
        return x + y * self.board_dim



def N_Puzzle_Solver(n_puzzle_problem : N_Puzzle_Problem, heuristic : Callable[[Node], float | int] | None = None):
    # Implement the A* search algorithm or any other search algorithm
    f = None
    if heuristic:
        f = lambda n: n.path_cost + heuristic(n)
    else:
        f = lambda n: n.path_cost

    root_node = Node(state=n_puzzle_problem.initial_state)

    reached = {root_node.state: 0}
    frontier = Priority_Que(evaluation_func=f)
    frontier.push(root_node)

    while len(frontier) > 0:
        current_node = frontier.pop()
        if n_puzzle_problem.IS_GOAL(current_node.state):
            return current_node
        elif reached[current_node.state] < current_node.path_cost:
            continue

        for child_node in expand(n_puzzle_problem, current_node):
            if reached.get(child_node.state) is None or reached[child_node.state] > child_node.path_cost:
                reached[child_node.state] = child_node.path_cost
                frontier.push(child_node)


    return None