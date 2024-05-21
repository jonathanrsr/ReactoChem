from reactochem.reactions import Reaction
from reactochem.reactors import Reactor
import matplotlib.pyplot as plt
import numpy as np

reaction1 = Reaction("Reaction 1", ['A', 'B', 'C'], [-1, -1, 1], '0.2*A**2*B')
reaction2 = Reaction("Reaction 2", ['B', 'C', 'D'], [-1, -1, 1], '0.75*B*C')
reaction3 = Reaction("Reaction 3", ['A', 'D'], [2, -0.5], '0.5*D**2')
reaction4 = Reaction("Reaction 4", ['C', 'B'], [-2, 2], '2*C')

initial_concs = {'A': 1, 'C': 0.5, 'B': 2, 'D': 1.5, 'E': 0.5}
feed_concs = {'A': 1, 'C': 0.5, 'B': 2, 'D': 1.5, 'E': 0.5}

batch = Reactor("Batch", 1, [reaction1, reaction2, reaction3, reaction4], initial_concs)
results = batch.run(10, plot = True)
print(batch.find_steady_state())
print(batch.find_conversion("A 0.5"))

""" fedbatch = Reactor("Fed-batch", 1, [reaction1, reaction2, reaction3, reaction4], initial_concs, 0.5, 0.1, feed_concs)
results = fedbatch.run(10, True)

cstr = Reactor("CSTR", 1, [reaction1, reaction2, reaction3, reaction4], initial_concs, 0.5, 0.1, feed_concs)
results = cstr.run(10, True)

pfr = Reactor("PFR", 1, [reaction1, reaction2, reaction3, reaction4], initial_concs, 0.5, 1, feed_concs)
results = pfr.run(10, True) """