from Modules.adjoint_pattern_database_module import translate_state_to_key, PatternGenerator
import pytest

def test_translate_state_to_key():
    problem = PatternGenerator(board_dim=3, initial_state=(1, 2, 3, 4, 5, 6, 7, 8, 0), goal_state=(1, 2, 3, 4, 5, 6, 7, 8, 0), focus_tiles=(1, 2, 3))
    assert translate_state_to_key((1, 2, 3, 4, 5, 6, 7, 8, 0), problem, problem.focus_tiles) == "000102"
    assert translate_state_to_key((1, 0, 9, 8, 6, 5, 4, 3, 2), problem, problem.focus_tiles) == "002221"

    with pytest.raises(AssertionError):
        assert translate_state_to_key((1, 2, 3), problem, problem.focus_tiles) == "000102"  # Length mismatch