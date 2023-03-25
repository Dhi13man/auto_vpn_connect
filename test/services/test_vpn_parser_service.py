'''
Test VPN Parser Service module
'''

from json import dumps

from src.services.vpn_parser_service import VpnDataParserService
from src.models.vpn_data.abstract_vpn_data import AbstractVpnData
from src.models.vpn_data.pritunl_vpn_data import PritunlVpnData


class TestVpnParserService:
    '''
    Test VPN Parser Service
    '''
    sut: VpnDataParserService = VpnDataParserService()

    def test_parse_vpn_data(self) -> None:
        '''
        Test parsing VPN data from JSON
        '''
        # Arrange
        # pylint: disable-next=line-too-long
        mock_vpn_type: str = 'PRITUNL'
        mock_vpn_id: str = 'test_id'
        mock_pin: str = 'test_pin'
        mock_token: str = 'test_token'
        mock_totp_url: str = 'otpauth://totp/test.package@tester?secret=TEST_SECRET&issuer=test'
        vpn_data: dict = {
            "vpn_list": [
                {
                    "vpn_type": mock_vpn_type,
                    "vpn_id": mock_vpn_id,
                    "pin": mock_pin,
                    "token": mock_token,
                    "totp_url": mock_totp_url
                }
            ]
        }
        expected_vpn_data: list[AbstractVpnData] = [
            PritunlVpnData(mock_vpn_id, pin=mock_pin,
                           token=mock_token, totp_url=mock_totp_url)
        ]

        # Act
        actual_vpn_data: list[AbstractVpnData] = TestVpnParserService.sut.parse_vpn_data(
            dumps(vpn_data))

        # Assert
        for i, expected in enumerate(expected_vpn_data):
            assert expected.to_json() == actual_vpn_data[i].to_json()

    def test_parse_vpn_data_empty(self) -> None:
        '''
        Test parsing empty VPN data from JSON
        '''
        # Arrange
        vpn_data: str = '{"vpn_list": []}'

        # Act
        actual_vpn_data: list[AbstractVpnData] = TestVpnParserService.sut.parse_vpn_data(
            vpn_data)

        # Assert
        assert len(actual_vpn_data) == 0

    def test_inject_configs(self) -> None:
        '''
        Test injecting global configs into VPN data classes
        '''
        # Arrange
        mock_cli_path: str = 'test_cli_path'
        vpn_config: dict = {
            'PRITUNL': {
                'cli_path': mock_cli_path,
            }
        }

        # Act
        TestVpnParserService.sut.inject_configs(vpn_config)

        # Assert
        assert PritunlVpnData.cli_path == mock_cli_path
