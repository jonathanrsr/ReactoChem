# ReactoChem Package

This package provides functionality to define chemical reactions via a `Reaction` class and calculate their rates based on given concentrations of species. This reactions can the be used with the `Reactor` class to simulate their evolution inside different types of reactor (for now only batch, fed-batch, CSTR and PFR reactors are available).

## Installation

You can install the package using pip inside the source directory (which contains the pyproject.toml file):

```
pip install .
```

or directly from the GitHub repo:

```
pip install git+https://github.com/jonathanrsr/ReactoChem
```

## Usage

### Importing the Classes

```python
from reactochem.reactions import Reaction
from reactochem.reactor import Reactor
```

### Creating a Reaction Object

To create a Reaction object, you need to provide the following parameters:

- `name`: The name of the reaction.
- `species`: A list of species involved in the reaction.
- `coeffs`: Stoichiometric coefficients corresponding to the species (in the same order as the species list).
- `rate_law`: The rate law expression for the reaction.

```python
reaction1 = Reaction(
    name="Reaction 1",
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
- `initial_bulk_concentrations`: The initial concentrations of the species inside the reactor (Batch, Fed-batch, CSTR).
- `initial_volume`: The initial volume (Fed-batch, CSTR).
- `flow_rate`: The flow rate of the feed (Fed-batch, CSTR, PFR).
- `inlet_concentrations`: The concentrations of the species in the inlet (Fed-batch, CSTR, PFR).

```python
cstr_exemple = Reactor(
    reactor_type="CSTR",
    volume=100, 
    reactions=[reaction], 
    initial_bulk_concentrations_dict={"A": 1.0, "B": 2.0, "C": 0.5},
    initial_volume=0,
    flow_rate=5,
    inlet_concentrations_dict={"A": 1.0, "B": 1.0, "C": 0}
)
```

### Running a Simulation

You can run a simulation of the reactor using the `run` method, specifying the time (Batch, Fed-batch or CSTR) or volume (PFR) for the simulation and whether to plot the results.

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
