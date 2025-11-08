from Modules.n_puzzle_game import N_Puzzle_Problem, N_Puzzle_Solver
from aima_toolkit.SearchProblemPackage import Node, Heuristic, SearchStatus
from typing import Callable
import argparse

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

def parse_state(state_str: str, dim: int) -> tuple[int, ...]:
    parts = state_str.replace(",", " ").split()
    expected = dim * dim
    if len(parts) != expected:
        raise ValueError(
            f"Expected {expected} tiles for a {dim}x{dim} puzzle, got {len(parts)}."
        )
    tiles = tuple(int(p) for p in parts)
    return tiles


def build_heuristic(name: str, problem: N_Puzzle_Problem, dim: int):
  if name == "pdb":
    n = dim * dim
    return PDB_heuristic( problem, tuple(range(1, n//2 + 1)), tuple(range(n//2 + 1, n)))
  elif name == "manhattan":
    return manhattan_distance_heuristic( problem )
  else:
    raise ValueError( f"Unknown heuristic: {name}" )


def main( ):
  parser = argparse.ArgumentParser(
    description="Solve the N-Puzzle from the command line."
  )

  parser.add_argument(
    "--dim",
    "-d",
    type=int,
    default=3,
    help="Board dimension N for an N×N puzzle (default: 3).",
  )

  parser.add_argument(
    "--state",
    "-s",
    required=True,
    help='Initial state as a flat list, e.g. "1 2 0 7 6 5 4 3 8".',
  )
  parser.add_argument(
    "--heuristic",
    "-H",
    choices=[ "pdb", "manhattan" ],
    default="pdb",
    help="Heuristic to use (default: pdb for 3x3, otherwise manhattan).",
  )

  args = parser.parse_args( )

  dim = args.dim
  initial_state = parse_state( args.state, dim )
  goal_state = make_goal_state( dim )

  print( f"Dimension: {dim}x{dim}" )
  print( f"Initial state: {initial_state}" )
  print( f"Goal state:    {goal_state}" )
  print( f"Heuristic:     {args.heuristic}" )
  print( "Solving...\n" )

  problem = N_Puzzle_Problem(
    board_dim=dim,
    initial_state=initial_state,
    goal_state=goal_state,
  )

  heuristic = build_heuristic( args.heuristic, problem, dim )
  solution = N_Puzzle_Solver( problem, heuristic=heuristic)

  if solution == SearchStatus.FAILURE:
    print( f"No solution found." )
    return

  for index, action in enumerate( solution.get_actions( ) ):
    print( f"Step {index}: {action}" )

  print( f"\nSolution length: {len( solution.get_actions( ) )} moves." )


if __name__ == "__main__":
  main( )