import pytest
from reactochem import Reaction

def test_valid_reaction() -> None:
    """This test should pass every time"""
    reaction = Reaction(
        "Reaction 1", ["A", "B", "C"], [-1, -1, 1], "0.2*A**2*B"
    )
    assert reaction.name == "Reaction 1"
    assert reaction.species_coeffs == {"A": -1, "B": -1, "C": 1}
    assert str(reaction.rate_law) == "0.2*A**2*B"

def test_species_coeffs_mismatch() -> None:
    """This test should raise a ValueError as the length of species and
    coefficients do not match"""
    with pytest.raises(ValueError):
        Reaction(
            "Reaction 1", ["A", "B", "C"], [-1, -1], "0.2*A**2*B"
        )

def test_invalid_symbol() -> None:
    """This test should raise a ValueError as a symbol in the rate law 
    is not specified as a species"""
    with pytest.raises(ValueError):
        Reaction(
            "Reaction 1", ["A", "B", "C"], [-1, -1, 1], "0.2*A**2*B*D"
        )

def test_same_specie() -> None:
    """This test should raise a ValueError as there cannot be the same
    species in the species list"""
    with pytest.raises(ValueError):
        Reaction(
            "Reaction 1", ["A", "A", "C"], [-1, -1, 1], "0.2*A**2*B"
        )

def test_str() -> None:
    """This test should pass every time"""
    reaction = Reaction(
        "Reaction 1", ["A", "B", "C"], [-1, -1, 1], "0.2*A**2*B"
    )
    assert str(reaction) == (
        "Species: {'A': -1, 'B': -1, 'C': 1}\n"
        "Rate law: 0.2*A**2*B"
    )

def test_calculate_rate() -> None:
    """This test should pass every time"""
    reaction = Reaction(
        "Reaction 1", ["A", "B", "C"], [-1, -1, 1], "0.2*A**2*B"
    )
    assert reaction.calculate_rate({"A": 1, "B": 2, "C": 3}) == 0.4

def test_wrong_species() -> None:
    """This test should raise a ValueError as the reaction rate 
    calculation includes a species that is not involved in the reaction"""
    with pytest.raises(ValueError):
        reaction = Reaction(
            "Reaction 1", ["A", "B", "C"], [-1, -1, 1], "0.2*A**2*Z"
        )
