from Modules.n_puzzle_game import N_Puzzle_Problem, N_Puzzle_Solver
from aima_toolkit.SearchProblemPackage import Node, Heuristic
from typing import Callable

def manhattan_distance_heuristic(problem : N_Puzzle_Problem) -> Heuristic:
    goal_state = problem.goal_state

    def h(node : Node) -> float | int:
        state : tuple = node.state
        distance = 0
        for i in range(len(state)):
            tile = state[i]
            if tile != 0:  # Skip the empty tile
                current_x, current_y = problem._translate_position(i)
                goal_x, goal_y = problem._translate_position(goal_state.index(tile))
                distance += abs(current_x - goal_x) + abs(current_y - goal_y)

        return distance

    return h

def PDB_heuristic(problem : N_Puzzle_Problem, *tiles : tuple[int, ...]) -> Callable[[Node], float | int]:
    import Modules.adjoint_pattern_database_module as APDB

    pdbs = [APDB.load_pattern_db(problem=problem, tiles=tile_tuple) for tile_tuple in tiles]
    def h(node : Node) -> float | int:
        state_keys = [APDB.translate_state_to_key(state=node.state, problem=problem, focus_tiles=tile_tuple) for tile_tuple in tiles]
        return sum(pdb.get(key, float('inf')) for pdb, key in zip(pdbs, state_keys))

    return h

def make_goal_state(n: int) -> tuple:
    return tuple(list(range(1, n * n)) + [0])

dim = 3
problem = N_Puzzle_Problem(board_dim=dim, initial_state=(1,6,2,4,0,5,7,8,3), goal_state=make_goal_state(dim))
solution : Node = N_Puzzle_Solver(problem, heuristic=PDB_heuristic(problem, (1,2,3,4), (5,6,7,8)))

#dim = 4
#problem2 = N_Puzzle_Problem(board_dim=dim, initial_state=(2,7,5,8,1,4,6,12,14,13,3,0,10,9,11,15), goal_state=make_goal_state(dim))
#solution2 : Node = N_Puzzle_Solver(problem2, heuristic=manhattan_distance_heuristic(problem2))

#dim = 4
#problem = N_Puzzle_Problem(board_dim=dim, initial_state=(2,3,4,9,13,1,15,8,14,0,7,12,10,5,6,11), goal_state=make_goal_state(dim))
#solution = N_Puzzle_Solver_PDB(problem, tiles=(1,2,3,4,5,6,7,8))
#problem = N_Puzzle_Problem(board_dim=dim, initial_state=(1, 3, 2, 5, 4, 8, 6 ,7 ,0), goal_state=make_goal_state(dim))
#solution = N_Puzzle_Solver_PDB(problem, tiles=(1,2,3,4))
for index, action in enumerate(solution.get_actions()):
    print(f"Step {index}: {action}")