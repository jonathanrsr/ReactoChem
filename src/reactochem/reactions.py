import sympy
from typing import List, Dict

class Reaction:
    def __init__(
            self, name: str, species: List[str], coeffs: List[float], 
            rate_law: str
        ) -> None:
        """Initialize a Reaction object.

        The rate law must be written in terms of the species with no 
        other symbols, i.e. the rate law cannot be written in terms of
        time or other variables. The species and coefficients must be
        specified in the same order.

        Args:
            name (str): The name of the reaction
            species (List[str]): Species involved in the reaction
            coeffs (List[float]): Stoechiometric coefficients 
                corresponding to the species (same order as species 
                list)
            rate_law (str): The rate law expression for the reaction

        Raises:
            ValueError: If the length of species and coeffs do not 
                match.
            ValueError: If a symbol in the rate law is not specified 
                as a species.
            ValueError: If there are repeated species in the species

        Returns:
            None

        """
        # Check if the length of species and coefficients match
        if (len(species) != len(coeffs)):
            raise ValueError(
                """Length of species and coefficients must match."""
            )
        
        self.name = name
        self.species_coeffs = dict(zip(species, coeffs))

        # Convert the rate law string to a sympy expression
        self.rate_law = sympy.sympify(rate_law)

        # Check if no other symbols are present in the rate law
        for symbol in self.rate_law.free_symbols:
            if (str(symbol) not in self.species_coeffs.keys()):
                raise ValueError(
                    f"Symbol '{symbol}' is not specified as a species."
                )
            
        # Check if there are no repeated species
        if (len(set(species)) != len(species)):
            raise ValueError(
                """Species cannot be repeated in the species list."""
            )

    def __str__(self) -> str:
        """Returns a string representation of the Reaction object.

        The string includes the species coefficients and the rate law.

        Returns:
            str: A string representation of the Reaction object.
            
        """
        return(
            f"Species: {self.species_coeffs}\n"
            f"Rate law: {self.rate_law}"
        )
    
    def calculate_rate(self,concentrations: Dict[str, float]) -> float:
        """Calculates the reaction rate based on the given concentrations 
        of species.

        Args:
            concentrations (Dict[str, float]): A list containing the 
                concentrations of species involved in the reaction

        Returns:
            float: The calculated reaction rate

        """
        
        # Substitute the concentrations into the rate law
        substituted_rate = self.rate_law.subs(concentrations)
        
        return substituted_rate