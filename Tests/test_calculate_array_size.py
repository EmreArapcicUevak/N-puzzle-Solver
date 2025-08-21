import pytest

def test_calculate_array_size():
    from Modules.adjoint_pattern_database_module import calculate_array_size
    assert calculate_array_size(9, 4) == 15120
    assert calculate_array_size(9, 3) == 3024
    assert calculate_array_size(9, 2) == 504
    assert calculate_array_size(9, 1) == 72
    assert calculate_array_size(9, 0) == 9

def test_invalid_input():
    from Modules.adjoint_pattern_database_module import calculate_array_size
    with pytest.raises(TypeError):
        calculate_array_size("9", 4)

    with pytest.raises(TypeError):
        calculate_array_size(9, "4")

    with pytest.raises(ValueError):
        calculate_array_size(9, -1)

    with pytest.raises(ValueError):
        calculate_array_size(9, 10)

    with pytest.raises(ValueError):
        calculate_array_size(9, 9)
    
    with pytest.raises(ValueError):
        calculate_array_size(0, -1)