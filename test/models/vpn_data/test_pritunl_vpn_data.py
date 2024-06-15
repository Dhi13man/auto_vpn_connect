'''
Test Pritunl VPN Data Model module
'''

from zope.interface import implementer

from src.enums.vpn_type import VpnType, VpnTypeVisitor
from src.models.vpn_model.pritunl_vpn_model import PritunlVpnModel
from src.models.vpn_config.pritunl_vpn_config import PritunlVpnConfig


@implementer(VpnTypeVisitor)
class _TestVpnTypeVisitor:
    '''
    Visitor that returns the VPN type itself
    '''

    def visit_pritunl(self) -> VpnType:
        '''Visit Pritunl VPN type'''
        return VpnType.PRITUNL

    def visit_wireguard(self) -> VpnType:
        '''Visit Wireguard VPN type'''
        return VpnType.WIREGUARD

    def visit_open_vpn(self) -> VpnType:
        '''Visit OpenVPN VPN type'''
        return VpnType.OPEN_VPN

    def visit_none(self) -> VpnType:
        '''Visit VPN type not specified'''
        return VpnType.NONE


class TestPritunlVpnData:
    '''
    Test PritunlVpnData class
    '''
    mock_vpn_type: str = 'PRITUNL'
    mock_vpn_id: str = 'test_id'
    mock_pin: str = 'test_pin'
    mock_token: str = 'test_token'
    mock_totp_url: str = 'otpauth://totp/test.package@tester?secret=TEST_SECRET&issuer=test'
    mock_vpn_id: str = 'test_id'
    mock_json: dict = {
        'vpn_type': mock_vpn_type,
        'vpn_id': mock_vpn_id,
        'pin': mock_pin,
        'token': mock_token,
        'totp_url': mock_totp_url
    }
    mock_config: PritunlVpnConfig = PritunlVpnConfig()
    sut: PritunlVpnModel = PritunlVpnModel(
        mock_vpn_id,
        config=mock_config,
        pin=mock_pin,
        token=mock_token,
        totp_url=mock_totp_url
    )

    def test_get_vpn_id(self):
        '''
        Test get_vpn_id method
        '''
        # Act
        actual_vpn_id: str = TestPritunlVpnData.sut.get_vpn_id()

        # Assert
        assert TestPritunlVpnData.mock_vpn_id == actual_vpn_id

    def test_get_vpn_type(self):
        '''
        Test get_vpn_type method
        '''
        # Act
        actual_vpn_type: VpnType = TestPritunlVpnData.sut.get_vpn_type()

        # Assert
        assert VpnType.PRITUNL == actual_vpn_type

    def test_get_pin(self):
        '''
        Test get_pin method
        '''
        # Act
        actual_pin: str = TestPritunlVpnData.sut.get_pin()

        # Assert
        assert TestPritunlVpnData.mock_pin == actual_pin

    def test_get_token(self):
        '''
        Test get_token method
        '''
        # Act
        actual_token: str = TestPritunlVpnData.sut.get_token()

        # Assert
        assert TestPritunlVpnData.mock_token == actual_token

    def test_visit(self):
        '''
        Test visiting VPN type
        '''
        # Arrange
        test_visitor: _TestVpnTypeVisitor = _TestVpnTypeVisitor()

        # Act
        actual_vpn_type: VpnType = TestPritunlVpnData.sut.visit(test_visitor)

        # Assert
        assert VpnType.PRITUNL == actual_vpn_type

    def test_to_json(self):
        '''
        Test to_json method
        '''
        # Act
        actual_json: dict = TestPritunlVpnData.sut.to_json()

        # Assert
        assert TestPritunlVpnData.mock_json == actual_json

    def test_from_json(self):
        '''
        Test from_json method
        '''
        # Arrange
        mock_config: PritunlVpnConfig = PritunlVpnConfig()
        
        # Act
        actual_vpn_data: PritunlVpnModel = PritunlVpnModel.from_json_with_config(
            TestPritunlVpnData.mock_json,
            mock_config
        )

        # Assert
        assert TestPritunlVpnData.mock_vpn_id == actual_vpn_data.get_vpn_id()
        assert TestPritunlVpnData.mock_vpn_type == actual_vpn_data.get_vpn_type().value
        assert TestPritunlVpnData.mock_pin == actual_vpn_data.get_pin()
        assert TestPritunlVpnData.mock_token == actual_vpn_data.get_token()
