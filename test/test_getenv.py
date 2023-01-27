from mrrobot.util import env


def test_getenv_with_non_existing_variable():
    assert env("variable_that_does_not_exist") is None
    assert env("variable_that_does_not_exist", 1) == 1
