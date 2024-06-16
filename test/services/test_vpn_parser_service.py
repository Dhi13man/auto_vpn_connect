"""
Test VPN Parser Service module
"""

from json import dumps

from src.services.vpn_parser_service import VpnDataParserService
from src.models.vpn_model.abstract_vpn_model import AbstractVpnModel
from src.models.vpn_model.pritunl_vpn_model import PritunlVpnModel


class TestVpnParserService:
    """
    Test VPN Parser Service
    """

    sut: VpnDataParserService = VpnDataParserService()

    def test_parse_vpn_data(self) -> None:
        """
        Test parsing VPN data from JSON
        """
        # Arrange
        mock_vpn_type: str = "PRITUNL"
        mock_vpn_id: str = "test_id"
        mock_pin: str = "test_pin"
        mock_token: str = "test_token"
        mock_totp_url: str = (
            "otpauth://totp/test.package@tester?secret=TEST_SECRET&issuer=test"
        )
        mock_vpn_data: dict = {
            "vpn_list": [
                {
                    "vpn_type": mock_vpn_type,
                    "vpn_id": mock_vpn_id,
                    "pin": mock_pin,
                    "token": mock_token,
                    "totp_url": mock_totp_url,
                }
            ]
        }
        mock_vpn_config: dict = {}
        expected_vpn_data: list[AbstractVpnModel] = [
            PritunlVpnModel(
                mock_vpn_id,
                config=mock_vpn_config,
                pin=mock_pin,
                token=mock_token,
                totp_url=mock_totp_url,
            )
        ]

        # Act
        actual_vpn_data: list[AbstractVpnModel] = (
            TestVpnParserService.sut.parse_vpn_data(
                dumps(mock_vpn_data),
            )
        )

        # Assert
        for i, expected in enumerate(expected_vpn_data):
            assert expected.to_json() == actual_vpn_data[i].to_json()

    def test_parse_vpn_data_empty(self) -> None:
        """
        Test parsing empty VPN data from JSON
        """
        # Arrange
        mock_vpn_data: str = '{"vpn_list": []}'

        # Act
        actual_vpn_data: list[AbstractVpnModel] = (
            TestVpnParserService.sut.parse_vpn_data(
                mock_vpn_data,
            )
        )

        # Assert
        assert len(actual_vpn_data) == 0

    def test_inject_configs(self) -> None:
        """
        Test injecting global configs into VPN data classes
        """
        # Arrange
        mock_cli_path: str = "test_cli_path"
        mock_vpn_config: dict = {
            "PRITUNL": {
                "cli_path": mock_cli_path,
            }
        }
        mock_vpn_data: dict = {
            "vpn_id": "<vpn_id_1>",
            "vpn_type": "PRITUNL",
            "pin": "<vpn_pin_1>",
        }

        # Act
        vpn: PritunlVpnModel = (
            TestVpnParserService.sut.generate_vpn_from_config_and_data(
                mock_vpn_config,
                mock_vpn_data,
            )
        )

        # Assert
        assert vpn.cli_path == mock_cli_path
