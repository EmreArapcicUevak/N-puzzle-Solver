import math
import numpy as np
from Modules.Search_Problem.expand import expand
from Modules.Search_Problem.node import Node
from Modules.n_puzzle_game import N_Puzzle_Problem
from Modules.que import Priority_Que
from rich.progress import Progress
import pickle
import os

def calculate_array_size(number_of_tiles : int, k : int) -> int:
    if not isinstance(number_of_tiles, int) or not isinstance(k, int):
        raise TypeError("Both arguments must be integers.")
    if number_of_tiles < 1 or k < 0 or k >= number_of_tiles:
        raise ValueError("Invalid input values.")
    
    # Calculate the size of the array needed to store the tile configurations
    return math.prod(range(number_of_tiles, number_of_tiles - k - 1, -1))


class PatternGenerator(N_Puzzle_Problem):
    def __init__(self, board_dim: int, initial_state: tuple, goal_state: tuple, focus_tiles: tuple):
        super().__init__(board_dim, initial_state, goal_state)
        self.focus_tiles = focus_tiles

    def ACTION_COST(self, state, action, new_state):
        old_empty_index = state.index(0)
        if new_state[old_empty_index] in self.focus_tiles:
            return 1
        else:
            return 0
        

def generate_adjoint_patterns(board_dim: int, focus_tiles: tuple, goal_state: tuple) -> dict:
  number_of_tiles = board_dim ** 2
  k = len(focus_tiles)

  assert k <= number_of_tiles, "Number of focus tiles cannot exceed total number of tiles."
  assert k > 0, "Number of focus tiles cannot be negative."


  array_size = calculate_array_size(number_of_tiles, k)
  backwards_problem = PatternGenerator(board_dim=int(math.sqrt(number_of_tiles)), initial_state=goal_state, goal_state=goal_state, focus_tiles=focus_tiles)

  root_node = Node(state=goal_state)

  reached = {}
  frontier = Priority_Que(evaluation_func=lambda node: node.path_cost)
  frontier.push(root_node)

  with Progress() as progress:
    total_states = math.perm(number_of_tiles, number_of_tiles)
    task = progress.add_task("[cyan]Generating adjoint patterns...", total=total_states)

    while len(frontier) > 0:
        node : Node = frontier.pop()

        reached[node.state] = node.path_cost
        progress.update(task, completed=len(reached))


        for child in expand(backwards_problem, node):
            if reached.get(child.state) is None or reached[child.state] > child.path_cost:
                frontier.push(child)

    save_pattern_db(reached=reached, n=number_of_tiles, tiles=focus_tiles)

  return reached

def save_pattern_db(reached, n, tiles):
    folder = f"Pattern_Databases/"
    os.makedirs(folder, exist_ok=True)

    filename = f"N{n}_tiles_{'_'.join(map(str, tiles))}.pkl"
    path = os.path.join(folder, filename)

    with open(path, "wb") as f:
        pickle.dump(reached, f, protocol=pickle.HIGHEST_PROTOCOL)

    print(f"[+] Saved pattern DB to {path}")

def load_pattern_db(n, tiles):
    folder = f"Pattern_Databases/"
    filename = f"N{n}_tiles_{'_'.join(map(str, tiles))}.pkl"
    path = os.path.join(folder, filename)

    with open(path, "rb") as f:
        return pickle.load(f)