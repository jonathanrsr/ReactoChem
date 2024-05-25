How To Use
==========

Create a Reaction
-----------------

To create a reaction, you need to create a new instance of the `Reaction` class. The constructor takes the following parameters:

    - `name`: The name of the reaction.
    - `species`: A list of the species involved in the reaction.
    - `coeffs`: A list of the stoichiometric coefficients of the species. The list should be in the same order as the species in the `species` list.
    - `rate_law`: A string containing the mathematical expression of the rate law. This string cannot contained symbols, except the species names.

Example:

    First import the module::
    
        from reaction import Reaction
    
    Then create a reaction::
    
        r = Reaction('example1', ['A', 'B', 'C'], [1, 1, -1], '0.2*A*B')
    
    Be sure that the species and coefficients lists are in the same order.

    This following reaction is wrong::

        r = Reaction('example2', ['A', 'B', 'C'], [1, 1, -1], 'k*B*A')

    Because the symbol k is not in the species list, thus cannot be interpreted when calculating the reaction rate.

Create a Reactor
----------------

To create a reactor, you need to create a new instance of the `Reactor` class. The constructor takes the following parameters:

    - `reactor_type`: The type of the reactor (batch, fed-batch, CSTR or PFR).
    - `volume`: The volume of the reactor.
    - `reactions`: A list of the reactions that will take place in the reactor.
    - `initial_bulk_concentrations`: A dictionary containing the initial concentrations of the species (batch, fed-batch and CSTR). The keys are the species names and the values are the initial concentrations.
    - `initial_volume`: The initial volume of the reactor (fed-batch and CSTR).
    - `flow_rate`: The flow rate of the reactor (fed-batch, CSTR and PFR).
    - `inlet_concentrations`: A dictionary containing the inlet concentrations of the species (fed-batch, CSTR and PFR). The keys are the species names and the values are the inlet concentrations.

Example:

    First import the module::
    
        from reaction import Reactor
    
    Then create a reactor::
    
        r = Reactor('Batch', 10, [r], {'A': 1, 'B': 2, 'C': 0})
    
    The reactor is a batch reactor with a volume of 10 L, containing species A, B and C with initial concentrations of 1, 2 and 0 mol/L, respectively.

    You can add multiple reactions to a reactor::

        r = Reactor('CSTR', 10, [r1, r2], {'A': 1, 'B': 2, 'C': 0}, 0, 1, {'A': 1, 'B': 1, 'C': 0})

    The reactor is a CSTR with a volume of 10 L, containing species A, B and C with initial concentrations of 1, 2 and 0 mol/L, respectively. The reactor has two reactions happening, r1 and r2, and the flow rate is 1 L/h.

Run a Simulation
------------------

To run the simulation, you need to call the `run` method of the reactor object. This method takes the following parameters:

    - `time`: The time at which the simulation will stop.
    - `plot`: A boolean indicating if the results should be plotted.
    - `full_output`: A boolean indicating if the full output should be returned. By default, only the time and concentrations are returned, but if `full_output` is `True`, the moles/molar flow, reaction rates and transformations rates are also returned.

Example:

    Start the simulation::
    
        r.run(10, plot=True)

    The simulation will run for 10 seconds and the results will be plotted.

Find Steady-stade Parameters
----------------------------

To find the steady-state of a reactor, you need to call the `steady_state` method of the reactor object. This method takes the following parameters:

    - `guess`: The initial guess at which time the steady-state is reached. The default value is 10.
    - `threshold`: The transformation rates at which the steady-state is considered reached. The default value is 1e-3.
    - `max_iterations`: The maximum number of iterations for the steady-state calculation. The default value is 10.

Example:

    Find the steady-state of the reactor::
    
        t_ss, conc_ss = r.find_steady_state()

    It will return the time at which the steady-state is reached as well as the concentrations at that time.

Find the Time needed to reached a certain Conversion:
-----------------------------------------------------

To find the time to reach a certain conversion, you need to call the `time_to_conversion` method of the reactor object. This method takes the following parameters:

    - `specie`: The specie of interest.
    - `conversion_target`: The target conversion.
    - `guess`: The initial guess at which time the conversion is reached. The default value is 10.

Example:

    Find the time to reach a certain conversion::
    
        t_conv = r.find_conversion('A', 0.5)[0]

It will return the time at which the conversion is reached. The method also returns the concentrations, moles/molar flow, reaction rates and transformation rates at that time::
            
        t_conv, conc_conv, moles_conv, reaction_rates_conv, transformation_rates_conv = r.find_conversion('A', 0.5)
