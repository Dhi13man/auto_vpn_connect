"""Tests for Pritunl VPN command execution."""

from subprocess import CompletedProcess

import pytest

from src.models.vpn_config.pritunl_vpn_config import PritunlVpnConfig
from src.models.vpn_model.pritunl_vpn_model import PritunlVpnModel


class TestPritunlVpnActions:
    """Verify Pritunl subprocess boundaries without running VPN commands."""

    def test_connect_when_verbose_runs_command_without_logging_secrets(
        self, capsys, mocker
    ) -> None:
        """Run Pritunl while keeping PIN, TOTP, and token out of logs."""
        # Arrange
        sut = PritunlVpnModel(
            "profile-id",
            PritunlVpnConfig(cli_path="pritunl-client"),
            pin="private-pin",
            token="private-token",
        )
        sut.totp_obj = mocker.Mock()
        sut.totp_obj.now.return_value = "654321"
        completed = CompletedProcess(args=[], returncode=0)
        run_mock = mocker.patch(
            "src.models.vpn_model.pritunl_vpn_model.run", return_value=completed
        )

        # Act
        actual = sut.connect(verbose=True)
        output = capsys.readouterr().out

        # Assert
        assert actual is completed
        run_mock.assert_called_once_with(
            [
                "pritunl-client",
                "start",
                "profile-id",
                "-p",
                "private-pin654321private-token",
            ],
            check=False,
        )
        assert "private-pin" not in output
        assert "654321" not in output
        assert "private-token" not in output
        assert "Return code: 0" in output

    def test_connect_when_client_returns_failure_propagates_return_code(
        self, mocker
    ) -> None:
        """Return a failed Pritunl connection process unchanged."""
        # Arrange
        sut = PritunlVpnModel("profile-id", PritunlVpnConfig("pritunl-client"))
        failed = CompletedProcess(args=[], returncode=4)
        mocker.patch("src.models.vpn_model.pritunl_vpn_model.run", return_value=failed)

        # Act
        actual = sut.connect(verbose=False)

        # Assert
        assert actual.returncode == 4

    def test_disconnect_when_requested_runs_expected_command(self, mocker) -> None:
        """Stop only the configured Pritunl profile."""
        # Arrange
        sut = PritunlVpnModel("profile-id", PritunlVpnConfig("pritunl-client"))
        completed = CompletedProcess(args=[], returncode=0)
        run_mock = mocker.patch(
            "src.models.vpn_model.pritunl_vpn_model.run", return_value=completed
        )

        # Act
        actual = sut.disconnect(verbose=False)

        # Assert
        assert actual is completed
        run_mock.assert_called_once_with(
            ["pritunl-client", "stop", "profile-id"], check=False
        )

    def test_disconnect_when_executable_is_missing_propagates_failure(
        self, mocker
    ) -> None:
        """Expose a missing Pritunl executable to the caller."""
        # Arrange
        sut = PritunlVpnModel("profile-id", PritunlVpnConfig("pritunl-client"))
        mocker.patch(
            "src.models.vpn_model.pritunl_vpn_model.run",
            side_effect=FileNotFoundError("pritunl-client"),
        )

        # Act + Assert
        with pytest.raises(FileNotFoundError, match="pritunl-client"):
            sut.disconnect(verbose=False)


def test_from_json_when_cli_path_is_omitted_uses_default() -> None:
    """Use the safe CLI path default when JSON omits it."""
    # Arrange
    config_json = {"vpn_type": "PRITUNL"}

    # Act
    actual = PritunlVpnConfig.from_json(config_json)

    # Assert
    assert actual.cli_path.endswith("/pritunl-client")
