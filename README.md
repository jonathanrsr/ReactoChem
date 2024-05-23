# ReactoChem Package

This package provides functionality to define chemical reactions and calculate their rates based on given concentrations of species. It also includes a `Reactor` class for simulating chemical reactors and analyzing reaction behavior.

## Installation

You can install the package using pip:

```
pip install reactochem
```

or directly from the GitHub repo:

## Usage

### Importing the Classes

```python
from reaction_package.reactions import Reaction
from reaction_package.reactor import Reactor
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

### Creating a Reactor Object

To create a Reactor object, you need to provide the following parameters:

- `reactor_type`: The type of reactor (Batch, Fed-batch, CSTR, PFR).
- `volume`: Volume of the reactor.
- `reactions`: Reactions taking place in the reactor.
- Additional parameters based on the reactor type (e.g., `initial_bulk_concentrations_dict` for Batch reactors).

```python
reactor = Reactor(
    reactor_type="Batch",
    volume=100, 
    reactions=[reaction], 
    initial_bulk_concentrations_dict={"A": 1.0, "B": 2.0, "C": 0.5}
)
```

### Running a Simulation

You can run a simulation of the reactor using the `run` method, specifying the time or volume for the simulation and whether to plot the results.

```python
time, concentrations = reactor.run(10, plot=True)
```

### Finding Steady State

You can find the steady state of the reactor using the `find_steady_state` method.

```python
steady_state_time, steady_state_concentrations = reactor.find_steady_state()
```

### Finding Conversion

You can find the time at which a given species reaches a desired conversion using the `find_conversion` method.

```python
conversion_time, conversion_concentrations = reactor.find_conversion("A", 0.8)
```

---

Feel free to modify and expand this README file according to your package's specific features and functionalities!
