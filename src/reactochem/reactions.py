import sympy
from typing import List, Dict


class Reaction:
    def __init__(
        self, name: str, species: List[str], coeffs: List[float],
        rate_law: str
    ) -> None:
        """
        Initialize a Reaction object.

        Args:
            name (str): The name of the reaction
            species (List[str]): Species involved in the reaction
            coeffs (List[float]): Stoichiometric coefficients corresponding
                        to the species (same order as species list)
            rate_law (str): The rate law expression for the reaction

        Raises:
            ValueError: If the length of species and coeffs do not match.
            ValueError: If a symbol in the rate law is not specified as a
                        species.
            ValueError: If there are repeated species in the species list

        """
        if len(species) != len(coeffs):
            raise ValueError(
                "Length of species and coefficients must match."
            )

        self.name = name
        self.species_coeffs = dict(zip(species, coeffs))
        self.rate_law = sympy.sympify(rate_law)

        for symbol in self.rate_law.free_symbols:
            if str(symbol) not in self.species_coeffs:
                raise ValueError(
                    f"Symbol '{symbol}' is not specified as a species."
                )

        if len(set(species)) != len(species):
            raise ValueError(
                "Species cannot be repeated in the species list."
            )

    def __str__(self) -> str:
        """
        Returns a string representation of the Reaction object.

        Returns:
            str: A string representation of the Reaction object.

        """
        return f"Species: {self.species_coeffs}\nRate law: {self.rate_law}"

    def calculate_rate(self, concentrations: Dict[str, float]) -> float:
        """
        Calculates the reaction rate based on the given concentrations of
        species.

        Args:
            concentrations (Dict[str, float]): A dictionary containing the
                concentrations of species

        Returns:
            float: The calculated reaction rate

        """
        substituted_rate = self.rate_law.subs(concentrations)
        return float(substituted_rate)
