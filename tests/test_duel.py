from animal_generator.duel import Duel


def test_random():
    value = Duel.random()
    assert value >= 0
    assert value <= Duel.random_value


def test_loss():
    duel = Duel(0, Duel.random_value + 1)
    duel.resolve()
    assert not duel.is_win


def test_win():
    duel = Duel(Duel.random_value, 0)
    duel.resolve()
    assert duel.is_win
