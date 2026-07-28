"""Tests for GlobalProtect VPN command execution."""

from subprocess import CompletedProcess
from unittest.mock import call

import pytest

from src.enums.vpn_type import VpnTypeVisitor
from src.models.vpn_config.global_protect_vpn_config import GlobalProtectVpnConfig
from src.models.vpn_model.global_protect_vpn_model import GlobalProtectVpnModel


class TestGlobalProtectVpnModel:
    """Verify GlobalProtect subprocess boundaries without running VPN commands."""

    def test_connect_when_command_contains_quoted_path_runs_expected_arguments(
        self, mocker
    ) -> None:
        """Preserve quoted executable paths when starting GlobalProtect."""
        # Arrange
        config = GlobalProtectVpnConfig(
            service_load_command='"/Applications/Global Protect" --connect'
        )
        sut = GlobalProtectVpnModel("work", config)
        completed = CompletedProcess(args=[], returncode=0)
        run_mock = mocker.patch(
            "src.models.vpn_model.global_protect_vpn_model.run",
            return_value=completed,
        )

        # Act
        actual = sut.connect(verbose=True)

        # Assert
        assert actual is completed
        run_mock.assert_called_once_with(
            ["/Applications/Global Protect", "--connect"], check=False
        )

    def test_connect_when_executable_is_missing_propagates_failure(
        self, mocker
    ) -> None:
        """Expose a missing GlobalProtect executable to the caller."""
        # Arrange
        sut = GlobalProtectVpnModel("work", GlobalProtectVpnConfig())
        mocker.patch(
            "src.models.vpn_model.global_protect_vpn_model.run",
            side_effect=FileNotFoundError("launchctl"),
        )

        # Act + Assert
        with pytest.raises(FileNotFoundError, match="launchctl"):
            sut.connect(verbose=False)

    def test_disconnect_when_commands_complete_runs_unload_then_scoped_stop(
        self, mocker
    ) -> None:
        """Unload the service before narrowly stopping its process."""
        # Arrange
        config = GlobalProtectVpnConfig()
        sut = GlobalProtectVpnModel("work", config)
        unload = CompletedProcess(args=[], returncode=0)
        stop = CompletedProcess(args=[], returncode=0)
        run_mock = mocker.patch(
            "src.models.vpn_model.global_protect_vpn_model.run",
            side_effect=[unload, stop],
        )
        sleep_mock = mocker.patch("src.models.vpn_model.global_protect_vpn_model.sleep")

        # Act
        actual = sut.disconnect(verbose=False)

        # Assert
        assert actual is stop
        assert run_mock.call_args_list == [
            call(
                [
                    "launchctl",
                    "unload",
                    "/Library/LaunchAgents/com.paloaltonetworks.gp.pangpa.plist",
                ],
                check=False,
            ),
            call(["pkill", "-TERM", "-x", "GlobalProtect"], check=False),
        ]
        sleep_mock.assert_called_once_with(1)

    def test_disconnect_when_stop_fails_returns_failed_process(self, mocker) -> None:
        """Return the process failure from the final disconnect command."""
        # Arrange
        sut = GlobalProtectVpnModel("work", GlobalProtectVpnConfig())
        failed = CompletedProcess(args=[], returncode=1)
        mocker.patch(
            "src.models.vpn_model.global_protect_vpn_model.run",
            side_effect=[CompletedProcess(args=[], returncode=0), failed],
        )
        mocker.patch("src.models.vpn_model.global_protect_vpn_model.sleep")

        # Act
        actual = sut.disconnect(verbose=False)

        # Assert
        assert actual.returncode == 1

    def test_visit_when_global_protect_dispatches_to_global_protect(
        self, mocker
    ) -> None:
        """Dispatch GlobalProtect models to the matching visitor method."""
        # Arrange
        sut = GlobalProtectVpnModel("work", GlobalProtectVpnConfig())
        visitor = mocker.Mock(spec=VpnTypeVisitor)
        visitor.visit_global_protect.return_value = "GLOBAL_PROTECT"

        # Act
        actual = sut.visit(visitor)

        # Assert
        assert actual == "GLOBAL_PROTECT"
        visitor.visit_global_protect.assert_called_once_with()
        visitor.visit_pritunl.assert_not_called()


def test_from_json_when_commands_are_omitted_uses_safe_defaults() -> None:
    """Apply safe command defaults when optional JSON keys are absent."""
    # Arrange
    config_json = {"vpn_type": "GLOBAL_PROTECT"}

    # Act
    actual = GlobalProtectVpnConfig.from_json(config_json)

    # Assert
    assert actual.service_load_command.startswith("launchctl load ")
    assert actual.service_unload_command.startswith("launchctl unload ")
    assert actual.process_kill_command == "pkill -TERM -x GlobalProtect"
