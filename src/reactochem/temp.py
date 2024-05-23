from reactochem import Reaction, Reactor

reaction = Reaction("Reaction 1", ["A", "B", "C"], [-1, -1, 1], "0.05*A*B")
initial_concs = {"A": 1, "B": 1, "C": 0}
feed_concs = {"A": 1, "B": 1, "C": 0}
reaction2 = Reaction("Reaction 23", ["A", "B", "C"], [1, 1, -1], "0.025*C")

batch = Reactor("Batch", 10, [reaction, reaction2], initial_concs)
fedbatch = Reactor("Fed-batch", 10, [reaction, reaction2], initial_concs,
                    0.5, 0.1, feed_concs)
cstr = Reactor("CSTR", 10, [reaction, reaction2], initial_concs, 0.5, 0.1,
                feed_concs)
pfr = Reactor("PFR", 10, [reaction, reaction2], initial_concs, 0.5, 1,
                feed_concs)

fedbatch.run(30, plot = True)

time_conversion_batch = batch.find_conversion("A", 0.4)[0]
time_conversion_fedbatch = fedbatch.find_conversion("A", 0.4)[0]
time_conversion_cstr = cstr.find_conversion("A", 0.4)[0]
time_conversion_pfr = pfr.find_conversion("A", 0.4)[0]

print(time_conversion_batch)
print(time_conversion_fedbatch)
print(time_conversion_cstr)
print(time_conversion_pfr)