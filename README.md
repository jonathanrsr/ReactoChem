# ReactoChem

This package provides functionality to define chemical reactions and calculate their rates based on given concentrations of species.

## Installation

You can install the package using pip:

```
pip install reactochem
```

or directly from the GitHub repository:

```
pip install git+https://github.com/jonathanrsr/ReactoChem
```

## Usage

### Importing the Reaction Class

```python
from reactochem.reactions import Reaction
```

### Creating a Reaction Object

To create a Reaction object, you need to provide the following parameters:

- `name`: The name of the reaction.
- `species`: A list of species involved in the reaction.
- `coeffs`: Stoichiometric coefficients corresponding to the species (in the same order as the species list).
- `rate_law`: The rate law expression for the reaction.

```python
reaction = Reaction(
    name="Reaction1",
    species=["A", "B", "C"],
    coeffs=[1, 2, 1],
    rate_law="k * A * B**2"
)
```

### String Representation of Reaction

You can get a string representation of the Reaction object using the `__str__` method:

```python
print(reaction)
# Output: Species: {'A': 1, 'B': 2, 'C': 1}
#         Rate law: k*A*B**2
```

### Calculating Reaction Rate

To calculate the reaction rate based on given concentrations of species, use the `calculate_rate` method:

```python
concentrations = {'A': 0.5, 'B': 1.0}
rate = reaction.calculate_rate(concentrations)
print(rate)
# Output: Calculated reaction rate
```

---