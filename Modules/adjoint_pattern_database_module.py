import math
from Modules.Search_Problem.expand import expand
from Modules.Search_Problem.node import Node
from Modules.n_puzzle_game import N_Puzzle_Problem
from Modules.que import Priority_Que

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

def translate_state_to_key(state: tuple, problem: N_Puzzle_Problem, focus_tiles: tuple) -> str:
    assert len(state) == problem.n, "State length does not match the problem's board dimension."

    result = ""
    for tile in focus_tiles:
        x,y=problem._translate_position(state.index(tile))
        result += f"{y}{x}"

    return result

def generate_pattern_dictionary(all_states: dict, problem : PatternGenerator):
    pattern_dictionary = {}
    for state, cost in all_states.items():
        key = translate_state_to_key(state, problem, problem.focus_tiles)
        if key not in pattern_dictionary or pattern_dictionary[key] > cost:
            pattern_dictionary[key] = cost

    return pattern_dictionary


from rich.progress import Progress
def generate_adjoint_patterns(board_dim: int, focus_tiles: tuple, goal_state: tuple) -> dict:
  number_of_tiles = board_dim ** 2
  k = len(focus_tiles)

  assert k <= number_of_tiles, "Number of focus tiles cannot exceed total number of tiles."
  assert k > 0, "Number of focus tiles cannot be negative."

  backwards_problem = PatternGenerator(board_dim=int(math.sqrt(number_of_tiles)), initial_state=goal_state, goal_state=goal_state, focus_tiles=focus_tiles)

  root_node = Node(state=goal_state)

  frontier = Priority_Que(evaluation_func=lambda node: node.path_cost)
  reached = {}

  frontier.push(root_node)

  with Progress() as progress:
    total_states = math.perm(number_of_tiles, number_of_tiles)/2
    task = progress.add_task("[cyan]Generating adjoint patterns...", total=total_states)

    while len(frontier) > 0:
        node : Node = frontier.pop()

        progress.update(task, completed=len(reached))

        for child in expand(backwards_problem, node):
            if reached.get(child.state) is None or reached[child.state] > child.path_cost:
                frontier.push(child)
                reached[child.state] = child.path_cost


    save_pattern_db(pattern_db=generate_pattern_dictionary(reached, backwards_problem), n=number_of_tiles, tiles=focus_tiles)

  return reached


import pickle
import os

def save_pattern_db(pattern_db, n, tiles):
    folder = f"Pattern_Databases/"
    os.makedirs(folder, exist_ok=True)

    filename = f"N{n}_tiles_{'_'.join(map(str, tiles))}.pkl"
    path = os.path.join(folder, filename)

    with open(path, "wb") as f:
        pickle.dump(pattern_db, f, protocol=pickle.HIGHEST_PROTOCOL)

    print(f"[+] Saved pattern DB to {path}")

def load_pattern_db(problem : N_Puzzle_Problem, tiles):
    folder = f"Pattern_Databases/"
    filename = f"N{problem.n}_tiles_{'_'.join(map(str, tiles))}.pkl"
    path = os.path.join(folder, filename)

    # If file doesn't exist → generate it
    if not os.path.exists(path):
        print(f"[!] Pattern DB not found at {path}. Generating...")
        # Import here to avoid circular import
        from Modules.adjoint_pattern_database_module import generate_adjoint_patterns  
        generate_adjoint_patterns(board_dim=problem.board_dim, focus_tiles=tiles, goal_state=problem.goal_state)

    # Now load it
    with open(path, "rb") as f:
        return pickle.load(f)