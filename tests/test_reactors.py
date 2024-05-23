import pytest
from reactochem import Reactor, Reaction


reaction = Reaction("Reaction 1", ["A", "B", "C"], [-1, -1, 1], "0.05*A*B")
initial_concs = {"A": 1, "B": 1, "C": 0}
feed_concs = {"A": 1, "B": 1, "C": 0}
reaction2 = Reaction("Reaction 23", ["A", "B", "C"], [1, 1, -1], "0.025*C")


def test_valid_reactors():
    """
    Test function ensures that the Reactor class can be instantiated with
    valid arguments.

    """
    batch = Reactor("Batch", 10, [reaction], initial_concs)
    fedbatch = Reactor("Fed-batch", 10, [reaction], initial_concs, 0.5, 0.1,
                       feed_concs)
    cstr = Reactor("CSTR", 10, [reaction], initial_concs, 0.5, 0.1, feed_concs)
    pfr = Reactor("PFR", 10, [reaction], initial_concs, 0.5, 1, feed_concs)

    assert batch
    assert fedbatch
    assert cstr
    assert pfr


def test_invalid_volume():
    """This test should raise a ValueError as the volume of the reactor
    cannot be negative or zero.

    """
    with pytest.raises(ValueError):
        Reactor("Batch", 0, [reaction], initial_concs)
    with pytest.raises(ValueError):
        Reactor("Batch", -10, [reaction], initial_concs)
    with pytest.raises(ValueError):
        Reactor(
            "Fed-batch", 0, [reaction], initial_concs, 0.5, 0.1,
            feed_concs
            )
    with pytest.raises(ValueError):
        Reactor("Fed-batch", -10, [reaction], initial_concs, 0.5, 0.1,
                feed_concs)
    with pytest.raises(ValueError):
        Reactor("Fed-batch", 10, [reaction], initial_concs, -0.5, 0.1,
                feed_concs)
    with pytest.raises(ValueError):
        Reactor(
            "Fed-batch", 10, [reaction], initial_concs, 15, 0.1,
            feed_concs
            )
    with pytest.raises(ValueError):
        Reactor(
            "CSTR", 0, [reaction], initial_concs, 0.5, 0.1,
            feed_concs
            )
    with pytest.raises(ValueError):
        Reactor(
            "CSTR", -10, [reaction], initial_concs, 0.5, 0.1, feed_concs
            )
    with pytest.raises(ValueError):
        Reactor(
            "CSTR", 10, [reaction], initial_concs, -0.5, 0.1, feed_concs
            )
    with pytest.raises(ValueError):
        Reactor(
            "CSTR", 10, [reaction], initial_concs, 15, 0.1, feed_concs
            )
    with pytest.raises(ValueError):
        Reactor(
            "PFR", 0, [reaction], initial_concs, 0.5, 1, feed_concs
            )
    with pytest.raises(ValueError):
        Reactor(
            "PFR", -10, [reaction], initial_concs, 0.5, 1, feed_concs
            )


def test_invalid_concentrations():
    """This test should raise a ValueError as the initial concentrations
    cannot be negative.

    """
    initial_concs_negative = {"A": -1, "B": 2, "C": 0}
    feed_concs_negative = {"A": 1, "B": 2, "C": -1}
    with pytest.raises(ValueError):
        Reactor("Batch", 10, [reaction], initial_concs_negative)
    with pytest.raises(ValueError):
        Reactor("Fed-batch", 10, [reaction], initial_concs_negative, 0.5, 0.1,
                feed_concs)
    with pytest.raises(ValueError):
        Reactor("Fed-batch", 10, [reaction], initial_concs, 0.5, 0.1,
                feed_concs_negative)
    with pytest.raises(ValueError):
        Reactor("CSTR", 10, [reaction], initial_concs_negative, 0.5, 0.1,
                feed_concs)
    with pytest.raises(ValueError):
        Reactor("CSTR", 10, [reaction], initial_concs, 0.5, 0.1,
                feed_concs_negative)
    with pytest.raises(ValueError):
        Reactor(
            "PFR", 10, [reaction], initial_concs, 0.5, 1,
            feed_concs_negative
            )


def test_run():
    """This test checks that the run method of the Reactor class returns the
    correct concentrations of species at the end of the reaction.

    """
    batch = Reactor("Batch", 10, [reaction, reaction2], initial_concs)
    fedbatch = Reactor("Fed-batch", 10, [reaction, reaction2], initial_concs,
                       0.5, 0.1, feed_concs)
    cstr = Reactor("CSTR", 10, [reaction, reaction2], initial_concs, 0.5, 0.1,
                   feed_concs)
    pfr = Reactor("PFR", 10, [reaction, reaction2], initial_concs, 0.5, 1,
                  feed_concs)

    concentrations_batch = batch.run(10)[1]
    last_concentrations_batch = {
        species: concentrations[-1] for species, concentrations in
        concentrations_batch.items()
    }
    concentrations_fedbatch = fedbatch.run(10)[1]
    last_concentrations_fedbatch = {
        species: concentrations[-1] for species, concentrations in
        concentrations_fedbatch.items()
    }
    concentrations_cstr = cstr.run(10)[1]
    last_concentrations_cstr = {
        species: concentrations[-1] for species, concentrations in
        concentrations_cstr.items()
    }
    concentrations_pfr = pfr.run(10)[1]
    last_concentrations_pfr = {
        species: concentrations[-1] for species, concentrations in
        concentrations_pfr.items()
    }

    assert last_concentrations_batch == pytest.approx({'A': 0.700, 'B': 0.700,
                                                       'C': 0.299}, abs=1e-3)
    assert last_concentrations_fedbatch == pytest.approx({'A': 0.784,
                                                          'B': 0.784,
                                                          'C': 0.216},
                                                         abs=1e-3)
    assert last_concentrations_cstr == pytest.approx({'A': 0.784, 'B': 0.784,
                                                      'C': 0.216}, abs=1e-3)
    assert last_concentrations_pfr == pytest.approx({'A': 0.700, 'B': 0.700,
                                                     'C': 0.299}, abs=1e-3)


def test_find_steady_state():
    """This test checks that the find_steady_state method of the Reactor class
    returns the correct time to reach steady state.

    """
    batch = Reactor("Batch", 10, [reaction, reaction2], initial_concs)
    fedbatch = Reactor("Fed-batch", 10, [reaction, reaction2], initial_concs,
                       0.5, 0.1, feed_concs)
    cstr = Reactor("CSTR", 10, [reaction, reaction2], initial_concs, 0.5, 0.1,
                   feed_concs)
    pfr = Reactor("PFR", 10, [reaction, reaction2], initial_concs, 0.5, 1,
                  feed_concs)

    time_steady_state_batch = batch.find_steady_state()[0]
    time_steady_state_fedbatch = fedbatch.find_steady_state()[0]
    time_steady_state_cstr = cstr.find_steady_state()[0]
    time_steady_state_pfr = pfr.find_steady_state()[0]

    assert time_steady_state_batch == pytest.approx(44.744, abs=1e-3)
    assert time_steady_state_fedbatch == pytest.approx(116.116, abs=1e-3)
    assert time_steady_state_cstr == pytest.approx(500)
    assert time_steady_state_pfr == pytest.approx(44.744, abs=1e-3)


def test_find_conversion():
    """This test checks that the find_conversion method of the Reactor class
    returns the correct time to reach a certain conversion of a species.

    """
    batch = Reactor("Batch", 10, [reaction, reaction2], initial_concs)
    fedbatch = Reactor("Fed-batch", 10, [reaction, reaction2], initial_concs,
                       0.5, 0.1, feed_concs)
    cstr = Reactor("CSTR", 10, [reaction, reaction2], initial_concs, 0.5, 0.1,
                   feed_concs)
    pfr = Reactor("PFR", 10, [reaction, reaction2], initial_concs, 0.5, 1,
                  feed_concs)

    time_conversion_batch = batch.find_conversion("A", 0.4)[0]
    time_conversion_fedbatch = fedbatch.find_conversion("A", 0.4)[0]
    time_conversion_cstr = cstr.find_conversion("A", 0.4)[0]
    time_conversion_pfr = pfr.find_conversion("A", 0.4)[0]

    assert time_conversion_batch == pytest.approx(18.498, abs=1e-3)
    assert time_conversion_fedbatch == pytest.approx(56.256, abs=1e-3)
    assert time_conversion_cstr == pytest.approx(56.556, abs=1e-3)
    assert time_conversion_pfr == pytest.approx(18.498, abs=1e-3)
