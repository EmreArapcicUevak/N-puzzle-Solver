import math
import numpy as np

def calculate_array_size(number_of_tiles : int, k : int) -> int:
    if not isinstance(number_of_tiles, int) or not isinstance(k, int):
        raise TypeError("Both arguments must be integers.")
    if number_of_tiles < 1 or k < 0 or k >= number_of_tiles:
        raise ValueError("Invalid input values.")
    
    # Calculate the size of the array needed to store the tile configurations
    return math.prod(range(number_of_tiles, number_of_tiles - k - 1, -1))


class AdjointPatternProblem:


def generate_adjoint_patterns(number_of_tiles: int, k: int) -> np.ndarray:
    array_size = calculate_array_size(number_of_tiles, k)
    return np.zeros((array_size, k), dtype=int)