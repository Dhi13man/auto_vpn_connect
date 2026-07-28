"""Tests for command-line option parsing."""

from pathlib import Path
from runpy import run_path


def _load_get_user_switches():
    module = run_path(str(Path(__file__).parents[1] / "__main__.py"))
    return module["get_user_switches"]


def test_get_user_switches_when_verbose_flag_is_present_enables_verbose(
    mocker,
) -> None:
    """Enable verbose output when the flag is present."""
    # Arrange
    mocker.patch("sys.argv", ["auto_vpn_connect", "--action", "c", "--verbose"])
    get_user_switches = _load_get_user_switches()

    # Act
    actual = get_user_switches()

    # Assert
    assert actual.get_action() == "c"
    assert actual.is_verbose() is True


def test_get_user_switches_when_verbose_flag_is_absent_disables_verbose(
    mocker,
) -> None:
    """Keep verbose output disabled when the flag is absent."""
    # Arrange
    mocker.patch("sys.argv", ["auto_vpn_connect", "--action", "d"])
    get_user_switches = _load_get_user_switches()

    # Act
    actual = get_user_switches()

    # Assert
    assert actual.get_action() == "d"
    assert actual.is_verbose() is False
