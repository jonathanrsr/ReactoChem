from .reactions import Reaction
from typing import List, Dict, Union, Tuple
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

class Reactor():
    def __init__(
        self, reactor_type: str, volume: float, reactions: List[Reaction], 
        initial_bulk_concentrations_dict: Dict[str, float] = {}, 
        initial_volume: float = 0, flow_rate: float = 0, 
        inlet_concentrations_dict: Dict[str, float] = {}
    ) -> None:
        """ Initialize a Reactor object.

        These reactors can be of the following types: Batch, Fed-batch,
        CSTR, PFR. The Reactor object can be used to simulate the
        behavior of a chemical reactor based on the type of reactor and
        the reactions taking place in the reactor, based on the initial
        conditions and parameters provided.

        Args:
            reactor_type (str): The type of reactor (Batch, Fed-batch, 
                CSTR, PFR).
            volume (float): Volume of the reactor.
            reactions (List[Reaction]): Reactions taking place in the 
                reactor.
            initial_bulk_concentrations_dict: Dict[str, float]: The 
                initial concentrations of the species in the reactor, 
                default is None, but must be specified for batch, 
                fed-batch, and CSTR reactors.
            initial_volume (float): The initial volume of the reactor,
                default is None, but must be specified for fed-batch and 
                CSTR reactors.
            flow_rate (float): The flow rate of the reactor, default 
                is None but must be specified for fed-batch, CSTR and 
                PFR reactors.
            inlet_concentrations_dict (Dict[str, float]): The inlet
                concentrations of the reaction, default is None but must
                be specified for fed-batch, CSTR, and PFR reactors.

        Raises:
            ValueError: If the volume of the reactor is less than or
                equal to 0
            ValueError: If the initial concentrations are not provided 
                for all species involved in the reactions
            ValueError: If the required parameters are not provided 
                for specific reactor types
            ValueError: If the flow rate is 0 for PFR reactors

        Returns:
            None

        """
        self.reactor_type = reactor_type
        if volume <= 0:
            raise ValueError(
                """Volume of the reactor must be greater than 0."""
            )
        self.volume = volume
        self.reactions = reactions

        # Check if initial concentrations are provided for all species
        all_species = set()
        for reaction in reactions:
            all_species.update(reaction.species_coeffs.keys())
        
        if (self.reactor_type in ["Batch", "Fed-batch", "CSTR"]):
            missing_species = (
                all_species - initial_bulk_concentrations_dict.keys()
            )
        elif (self.reactor_type == "PFR"):
            missing_species = (
                all_species - inlet_concentrations_dict.keys()
            )
        if (missing_species):
            raise ValueError(
                f"""Missing initial concentrations for species: 
                {missing_species}"""
            )
        
        # Check that initial concentrations are not negative
        if self.reactor_type != "PFR":
            for species, concentration in (
                initial_bulk_concentrations_dict.items()
            ):
                if concentration < 0:
                    raise ValueError(
                        f"""Initial concentration for species '{species}' is 
                        negative: {concentration}"""
                    )
            self.initial_bulk_concentrations_dict = dict(sorted(
                initial_bulk_concentrations_dict.items()
            ))
        
        if (self.reactor_type in ["Fed-batch", "CSTR"]):
            self.inlet_concentrations_dict = dict(
                sorted(inlet_concentrations_dict.items())
            )

        # Check that feed concentrations are not negative (only for PFR)
        else:
            for species, concentration in inlet_concentrations_dict.items():
                if concentration < 0:
                    raise ValueError(
                        f"""Inlet concentration for species '{species}' 
                        is negative: {concentration}"""
                    )
            self.inlet_concentrations_dict = dict(
                sorted(inlet_concentrations_dict.items())
            )

        # Check required parameters based on reactor type
        required_parameters = {
            "Fed-batch": ["inlet_concentrations_dict"],
            "CSTR": [ "inlet_concentrations_dict"],
            "PFR": ["flow_rate", "inlet_concentrations_dict"]
        }
        if (reactor_type in required_parameters):
            for parameter in required_parameters[reactor_type]:
                if (locals()[parameter] in (0, {})):
                    raise ValueError(
                        f"""{parameter.replace("_", " ").capitalize()} must be 
                        specified for {reactor_type} reactor."""
                    )
        
        if (self.reactor_type == "PFR" and flow_rate == 0):
            raise ValueError(
                """Flow rate must be greater than 0 for PFR reactors."""
            )

        self.initial_volume = initial_volume
        self.flow_rate = flow_rate
        self.inlet_concentrations_dict = dict(
            sorted(inlet_concentrations_dict.items())
        ) if (inlet_concentrations_dict) else None

    def __str__(self) -> str:
        """Returns a string representation of the Reactor object.

        The string includes the volume, list of reactions, and initial
        bulk concentrations.

        Returns:
            str: A string representation of the Reaction object

        """
        reactions_str = "\n".join([f"{i + 1}. {reaction}" for i, reaction 
            in enumerate(self.reactions)])
        
        return(
            f"Volume: {self.volume}\n"
            f"Reactions: {reactions_str}\n"
            f"""Initial bulk concentrations: {
                self.initial_bulk_concentrations_dict
            }\n"""
            f"Initial volume: {self.initial_volume}\n"
            f"Flow rate: {self.flow_rate}\n"
            f"Inlet concentrations: {self.inlet_concentrations_dict}"
        )
    
    def initialize_coeffs_matrix(self):
        """Initialize a matrix of stoichiometric coefficients for each 
        species in each reaction, where the number of rows is the number 
        of species and the number of columns is the number of reactions.
            
        Returns:
            np.ndarray: A matrix of stoichiometric coefficients for 
            each species in each reaction
        
        """
        num_species = len(self.initial_bulk_concentrations_dict)
        num_reactions = len(self.reactions)
        coeffs_matrix = np.zeros([num_species, num_reactions])

        for i, reaction in enumerate(self.reactions):
            for j, specie in enumerate(
                self.initial_bulk_concentrations_dict.keys()
            ):
                if (specie in reaction.species_coeffs):
                    coeffs_matrix[j, i] = (
                        reaction.species_coeffs[specie]
                    )

        return coeffs_matrix
    
    def calculate_concentration(self, x, y):
        """Calculate the concentration of each species at a given time 
        or volume.
            
        Args:
            x (float): The time or volume at which the concentrations 
                are calculated
            y (np.ndarray): The moles or molar flow of each 
                species at the time or volume
        
        Returns:
            np.ndarray: The concentration of each species at the time
            or volume
            
        """
        if (self.reactor_type == "Batch"):
            concentrations = y/self.volume
        elif (self.reactor_type in ["Fed-batch", "CSTR"]):
            volume = min(
                self.initial_volume + self.flow_rate*x, self.volume
            )
            concentrations = y/volume
        elif (self.reactor_type == "PFR"):
            concentrations = y/self.flow_rate

        return concentrations

    def calculate_reaction_rates(self, concentrations_dict) -> np.ndarray:
        """Calculate the reaction rates of all the reactions happening
        in the reactor at a given time (Batch, Fed-batch, CSTR) or 
        volume (PFR).

        Args:
            concentrations_dict (Dict[str, float]): A dictionary 
                containing the concentrations of each species

        Returns:
            np.ndarray: An array of reaction rates for each reaction

        """
        return np.array([
            reaction.calculate_rate(concentrations_dict) 
            for reaction in self.reactions
        ]).reshape(-1, 1)
    
    def calculate_transformation_rates(self, coeffs_matrix, reaction_rates):
        """Calculate the transformation rates of each species based on 
        the stoichiometric coefficients and reaction rates.
            
        Args:
            coeffs_matrix (np.ndarray): A matrix of stoichiometric 
                coefficients for each species in each reaction
            reaction_rates (np.ndarray): An array of reaction rates 
                for each reaction
            
        Returns:
            np.ndarray: An array of transformation rates for each species
        
        """
        return np.dot(coeffs_matrix, reaction_rates).reshape(-1)
    
    def run(self, x: float = None, plot: bool = False, 
            full_output: bool = False,
        ) -> Union[np.ndarray, tuple[np.ndarray, Dict[str, np.ndarray], 
                                             Dict[Reaction, np.ndarray], 
                                             Dict[str, np.ndarray]]
                                             ]:
        """Run the reaction simulation for a given time period.

        Args:
            time (float): The time period for which the simulation 
                should run for batch, fed-batch and CSTR reactors, 
                default is None but must be specified for batch, 
                fed-batch and CSTR reactors
                
                If None is provided for a PFR, the simulation will run until
                the volume of the reactor is reached
            plot (bool): Whether to plot the concentration, number of 
                moles or molar flow, reaction rates and transformation
                rates, default is False

                Setting plot to True will override full_output to True
           
            full_output (bool): Whether to return the full output of 
                the simulation, default is False

        Raises:
            ValueError: If time is not specified for batch, fed-batch,
                and CSTR reactors

        Returns:
            Tuple[np.ndarray, Dict[str, np.ndarray], Dict[str, np.ndarray], Dict[Reaction, np.ndarray], Dict[str, np.ndarray]]:
            In order : the time, the concentrations, the number of moles
            or molar flow, the reaction rates and the transformation 
            rates at each time or volume if full_output is True, else 
            only the time and concentrations are returned

        """
        if (self.reactor_type in ["Batch", "Fed-batch", "CSTR"]):
            if (x is None):
                raise ValueError(
                    """Time must be specified for batch, fed-batch, and 
                    CSTR reactors."""
                )
        
        def ODE(x: float, y: np.ndarray) -> np.ndarray:
            """Calculate the rate of change of moles for the Batch,
            Fed-batch, CSTR reactors or of the molar flow for the PFR
            reactor.

            Args:
                x (float): The time at which the rate of change of y 
                    is calculated for batch, fed-batch and CSTR reactors
                    or the volume for PFR reactors
                y (np.ndarray): The moles or molar flow of each species

            Returns:
                np.ndarray: The rate of change of y for each species 
                    at the time or volume based on the type of reactor

            """
            concentrations = self.calculate_concentration(x, y)
            concentrations_dict = dict(zip(
                self.initial_bulk_concentrations_dict.keys(), concentrations
            ))

            coeffs_matrix = self.initialize_coeffs_matrix()
            reaction_rates = self.calculate_reaction_rates(concentrations_dict)
            transformation_rates = self.calculate_transformation_rates(
                coeffs_matrix, reaction_rates
            )

            # Calculate the rate of change of moles or molar flow
            if (self.reactor_type == "Batch"):
                dy_dx = transformation_rates*self.volume
            elif (self.reactor_type == "Fed-batch"):
                volume = min(
                    self.initial_volume + self.flow_rate*x, self.volume
                )
                current_flow_rate_inlet = self.flow_rate if (
                    volume < self.volume
                ) else 0
                dy_dx = transformation_rates*volume + current_flow_rate_inlet*(
                    np.array(
                        list(self.inlet_concentrations_dict.values())
                    )
                )
            elif (self.reactor_type == "CSTR"):
                volume = min(
                    self.initial_volume + self.flow_rate*x, self.volume
                )
                current_flow_rate_outlet = 0 if (volume < self.volume) else (
                    self.flow_rate
                )
                dy_dx = transformation_rates*volume + self.flow_rate*(
                    np.array(
                        list(self.inlet_concentrations_dict.values())
                    )) - current_flow_rate_outlet*concentrations
            elif (self.reactor_type == "PFR"):
                dy_dx = transformation_rates

            return dy_dx
        
        # Initialize the initial conditions based on the reactor type
        if (self.reactor_type == "Batch"):
            initial_y = np.array(list(
                self.initial_bulk_concentrations_dict.values()
            ))*self.volume
        elif (self.reactor_type in ["Fed-batch", "CSTR"]):
            initial_y = np.array(list(
                self.initial_bulk_concentrations_dict.values()
            ))*self.initial_volume
        elif (self.reactor_type == "PFR"):
            initial_y = np.array(list(
                self.inlet_concentrations_dict.values()
            ))*self.flow_rate
        
        x_points = np.linspace(0, x, 1000)
        results = solve_ivp(
            ODE, [0, x], initial_y, method = "Radau", 
            t_eval = x_points, max_step = x/100
        )

        x = results.t
        y = results.y.T

        # Calculate the concentrations at each time or volume
        if (self.reactor_type in ["Batch"]):
            concentrations = y/self.volume
        elif (self.reactor_type in ["Fed-batch", "CSTR"]):
            volume = np.minimum(
                self.initial_volume + self.flow_rate*x, self.volume
            )
            concentrations = y/volume.reshape(-1, 1)
        elif (self.reactor_type == "PFR"):
            concentrations = y/self.flow_rate

        concentrations_dict = {
            specie: concentrations[:, i] for i, specie 
            in enumerate(self.initial_bulk_concentrations_dict.keys())
        }

        if full_output or plot:
            num_species = len(self.initial_bulk_concentrations_dict)
            num_reactions = len(self.reactions)
            coeffs_matrix = self.initialize_coeffs_matrix()
            reaction_rates = np.zeros([num_reactions, len(x)])
            transformation_rates = np.zeros([num_species, len(x)])

            for i in range(len(x)):
                concentrations_at_x = {specie: concentrations_dict[specie][i] for 
                    specie in concentrations_dict
                }
                reaction_rates[:, i] = self.calculate_reaction_rates(
                    concentrations_at_x
                ).flatten()
                transformation_rates[:, i] = self.calculate_transformation_rates(
                    coeffs_matrix, reaction_rates[:, i]
                )
            
            y_dict = {specie: y[:, i] for i, specie in enumerate(
                self.initial_bulk_concentrations_dict.keys()
            )}
            reaction_rates_dict = {reaction.name: reaction_rates[i] for 
                i, reaction in enumerate(self.reactions)
            }
            transformation_rates_dict = {specie: transformation_rates[i] for
                i, specie in enumerate(
                    self.initial_bulk_concentrations_dict.keys()
                )
            }

            if (plot):
                fig, axs = plt.subplots(2, 2, figsize=(10, 8))
                for ax, data, ylabel in zip(
                    axs.flat, [concentrations, y, reaction_rates.T, 
                            transformation_rates.T],
                            ["Concentration", "Moles" if 
                            (self.reactor_type != "PFR") else "Molar flow", 
                            "Reaction rates", 
                            "Transformation rates"]
                ):
                    ax.plot(x, data, linewidth = 1.0)
                    ax.set_xlabel(
                        "Time" if (self.reactor_type != "PFR") else "Volume"
                    )
                    ax.set_ylabel(ylabel)
                    ax.legend(
                        list(self.initial_bulk_concentrations_dict.keys() if (
                            ylabel != "Reaction rates") else [
                                reaction.name for reaction in self.reactions
                            ]
                        )
                    )

                    if (ylabel != "Transformation rates"):
                        ax.set_ylim(0)

                    if (self.reactor_type in ["Fed-batch", "CSTR"]):
                        volume = np.minimum(
                            self.initial_volume + self.flow_rate*x, self.volume
                        )
                        ax_volume = ax.twinx()
                        ax_volume.plot(
                            x, volume, color = "black", linestyle = "--", 
                            linewidth = 1.0
                        )
                        ax_volume.set_ylabel("Volume")

                plt.tight_layout()
                plt.show()

        if (full_output):
            return (
                x, concentrations_dict, y_dict, reaction_rates_dict, 
                transformation_rates_dict
            )

        return x, concentrations_dict
    
    def find_steady_state(
            self, guess: float = 10, threshold: float = 1e-3, 
            max_interations: int = 10
        ) -> tuple[float, Dict[str, float]]:
        """Find the steady state of the reaction system.

        Args:
            guess (float): The initial guess for the time or volume at 
                which the steady state is reached, default is 10
            threshold (float): The threshold value for determining 
                steady state (the maximal rate of change of concentration 
                over time), default is 1e-3
            max_interations (int): The maximum number of iterations to
                find the steady state, default is 10

        Raises:
            ValueError: If the steady state is not reached within the
            maximum number of iterations

        Returns:
            Tuple[float, Dict[str, float], Dict[str, float], Dict[Reaction, float], Dict[str, float]]: 
            In order : the time, the concentrations, the number of moles
            or molar flow, the reaction rates and the transformation rates
            at the steady state

        """
        steady_state_reached = False
        iteration_count = 0

        # Run a simulation to find the steady state
        while not steady_state_reached and iteration_count < max_interations:
            iteration_count += 1
            (
                x,
                concentrations_dict,
                y_dict,
                reaction_rates_dict,
                transformation_rates_dict
             ) = self.run(guess, full_output = True)

            transformation_rates = np.array(
                list(transformation_rates_dict.values())
            ).T

            below_threshold = np.all(
                np.abs(transformation_rates) < threshold, axis = 1
            )

            if (np.any(below_threshold)):
                # Find the time at which the steady state is reached
                x_steady_state = x[np.where(below_threshold)[0][0]]
                steady_state_reached = True
            else:
                guess *= 10  # Increase time guess

        if (not steady_state_reached):
            raise ValueError(
                """Steady state not reached within the maximum number of 
                iterations."""
            )
    
        steady_state_concentrations_dict = {
            specie: concentrations_dict[specie][np.where(
                below_threshold
            )[0][0]] 
            for specie in concentrations_dict
        }
        steady_state_y_dict = {
            specie: y_dict[specie][np.where(
                below_threshold
            )[0][0]] 
            for specie in y_dict
        }
        steady_state_reaction_rates_dict = {
            reaction: reaction_rates_dict[reaction][np.where(
                below_threshold
            )[0][0]] 
            for reaction in reaction_rates_dict
        }
        steady_state_transformation_rates_dict = {
            specie: transformation_rates_dict[specie][np.where(
                below_threshold
            )[0][0]] 
            for specie in transformation_rates_dict
        }
        
        return (
            x_steady_state, steady_state_concentrations_dict,
            steady_state_y_dict, steady_state_reaction_rates_dict,
            steady_state_transformation_rates_dict
        )
    
    def find_conversion(
            self, specie: str, conversion_target: float, guess: float = 10
        ) -> Tuple[float, Dict[str, float], Dict[str, float],
                    Dict[Reaction, float], Dict[str, float]]:
        """Calculate the time at which a given species reaches a desired
        conversion.

        Args:
            specie (str): The species of interest
            conversion_target (float): The desired conversion
            guess (float): The initial guess for the time or volume at
                which the desired conversion is reached, default is 10

        Raises:
            ValueError: If the desired conversion is higher than the
                conversion at steady state

        Returns:
            Tuple[float, Dict[str, float], Dict[str, float], Dict[Reaction, float], Dict[str, float]]:
            In order : the time, the concentrations, 
            the number of moles or molar flow, the reaction rates and 
            the transformation rates at the desired conversion

        """ 
        initial_concentration_specie = (
            self.initial_bulk_concentrations_dict[specie]
        )

        final_concentration_specie = (
            initial_concentration_specie*(1 - conversion_target)
        )

        steady_state_data = self.find_steady_state(guess = guess)
        x_steady_state = steady_state_data[0]
        concentration_steady_state_specie = steady_state_data[1][specie]
        """
        Calculate the maximal conversion (conversion at steady state) 
        that can be obtain for the specie
        """
        maximal_conversion = (
            (
                initial_concentration_specie -
                concentration_steady_state_specie
            )/initial_concentration_specie
        )

        if (conversion_target > maximal_conversion):
            raise ValueError(
                f"""Conversion rate too high. Maximum conversion rate: 
                {maximal_conversion}"""
            )
        
        (
            x,
            concentrations_dict,
            y_dict,
            reaction_rates_dict,
            transformation_rates_dict
        ) = self.run(x_steady_state, full_output = True)

        # Find the time at which the desired conversion is reached
        index_conversion_reached = np.where(
            concentrations_dict[specie] <= final_concentration_specie
        )[0][0]

        time_conversion_reached = x[index_conversion_reached]
        concentrations_conversion_reached = {
            specie: concentrations_dict[specie][index_conversion_reached]
        }
        y_conversion_reached = {
            specie: y_dict[specie][index_conversion_reached]
        }
        reaction_rates_conversion_reached = {
            reaction: reaction_rates_dict[reaction][index_conversion_reached] 
            for reaction in reaction_rates_dict
        }
        transformation_rates_conversion_reached = {
            specie: transformation_rates_dict[specie][index_conversion_reached]
        }

        return (time_conversion_reached, concentrations_conversion_reached,
            y_conversion_reached, reaction_rates_conversion_reached,
            transformation_rates_conversion_reached
        )