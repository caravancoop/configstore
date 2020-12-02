import pytest

from configstore.converters import asbool


@pytest.mark.parametrize('value', [
    "true", " true ", " TrUe",
    "on", "ON",
    "\nYes", " \tyes ",
    "1", " 1 ", 1,
    True,
])
def test_asbool_true(value):
    assert asbool(value) is True


@pytest.mark.parametrize('value', [
    "False", "FALSE", "false  ",
    "off", "oFF ",
    "no", "\tno",
    " 0 ", "0", 0,
    "", " ", "\n", "\t",
    False,
])
def test_asbool_false(value):
    assert asbool(value) is False


@pytest.mark.parametrize('value', [
    "y", "n", "t", "f",
    "00", "01", None,
])
def test_asbool_invalid(value):
    with pytest.raises(ValueError):
        asbool(value)
