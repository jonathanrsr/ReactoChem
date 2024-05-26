How This Works
==============

This section explains the underlying mechanisms of the simulation, including the calculations and processes involved in modeling the evolution of chemical reactions within different types of reactors (Batch, Fed-batch, Continuous Stirred-Tank Reactor (CSTR), and Plug Flow Reactor (PFR)).

Overview
--------

The purpose of the simulation is to observe and analyze the progression of chemical reactions within various reactor types. The simulation makes use of two main class:

1. **Reactor** (from the :mod:`~reactochem.reactors` module): Represents different types of reactors.
2. **Reaction** (from the :mod:`~reactochem.reactions` module): Represents the chemical reactions occurring within the reactors.

The simulation calculates the changes in the concentration of reactants and products over time using specific differential equations tailored for each reactor type. For now, the simulations assume ideal mixing, liquid reactions and isothermal conditions.

Reactor Types and Their Dynamics
--------------------------------

1. **Batch Reactor**:
   
- In a batch reactor, the reaction mixture is placed in a vessel and allowed to react for a certain period without any input or output flows during the reaction.
- The rate of change of the number of moles of a species :math:`N` over time :math:`t` is given by the equation:
    
    :math:`\frac{dN}{dt} = R \cdot A`

    where:
     
    - :math:`R`: is the rate of transformation.
    - :math:`V` is the volume of the reactor.

2. **Fed-batch Reactor**:

- A fed-batch reactor involves feeding reactants into the reactor over time while the reaction is ongoing. The feed is then cut when the mixture's volume reaches the volume of the reactor
- The rate of change of the number of moles of a species :math:`N` over time :math:`t` is given by:
     
    :math:`\frac{dN}{dt} = \dot{V} \cdot C_0 + R \cdot V`

    where:

    - :math:`\dot{V}`: is the volumetric flow rate of the feed.
    - :math:`C_0`: is the concentration in the feed.
    - :math:`R`: is the rate of transformation.
    - :math:`V`: is the volume of the reactor.

- The rate of change of volume :math:`V` is given by:

    :math:`\frac{dV}{dt} = \dot{V}`

    where:

    - :math:`\dot{V}`: is the volumetric flow rate of the feed.

3. **Continuous Stirred-Tank Reactor (CSTR)**:

- In a CSTR, reactants are continuously fed into the reactor and products are continuously removed, while the contents are well mixed. The outlet flow is 0 until the mixture's volume reaches the volume of the reactor, then its flow rate is set to be the same as the inlet flow.
- The rate of change of the number of moles of a species :math:`N` over time :math:`t` is given by:
     
    :math:`\frac{dN}{dt} = \dot{V_{in}} \cdot C_0 - \dot{V_{out}} \cdot C + R \cdot V`

    where:
    
    - :math:`\dot{V}_{in}` is the volumetric flow rate of the inlet.
    - :math:`\dot{V}_{out}` is the volumetric flow rate of the outlet.
    - :math:`C_0` is the concentration of the feed.
    - :math:`C` is the concentration within the reactor.
    - :math:`R` is the rate of transformation.
    - :math:`V` is the volume of the reactor.

4. **Plug Flow Reactor (PFR)**:

- In a PFR, reactants flow through the reactor as a plug, with no back-mixing.
- The rate of change of the molar flow of a species :math:`F` over volume :math:`V` along the reactor is given by:
    
    :math:`\frac{dF}{dV} = R`

    where:

    - :math:`R` is the rate of transformation.

Key Algorithms and Methodologies
--------------------------------

Simulations
~~~~~~~~~~~

The simulation employs the Radau method from the `scipy.integrate.solve_ivp` function to solve the differential equations. They can be stiff in some cases, as the volume's evolution can change brutally in the case of fed-batch and CSTR reactors.

Steady-state
~~~~~~~~~~~~

To find the steady-state of different reactors, the package looks for a point where the transformation rates of all species is under a certain threshold. For that, it runs the simulation for a certain amount of time, looks at the final transformation rates, and if the steady-stade isn't reached, try again with a longer time span.
For the CSTR, the method is different: due to its unique dynamics, the time at which the steady-state is reached :math:`t_{ss}` can be defined as:

    - :math:`t_{ss} = 3 \cdot \tau`

    where:

    - :math:`\tau` is the residence time of the reactor (:math:`\frac{V}{\dot{V}})`.

Conversion
~~~~~~~~~~

Finally, the package can also find the time at which a desired specie reaches a certain conversion. For this, the simulation runs until steady-state, looks at the time where the species reaches the desired conversion, and returns the result. In the case that the concentration at steady-state is higher than the desired concentration, it returns an error to inform the user that the desired conversion cannot be reached with the current conditions.
