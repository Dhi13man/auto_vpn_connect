'''
Test Abstract VPN Data Model module
'''

import pytest
from zope.interface import implementer

from src.enums.vpn_data.vpn_type import VpnType, VpnTypeVisitor
from src.models.vpn_data.abstract_vpn_data import AbstractVpnData
from src.models.vpn_data.pritunl_vpn_data import PritunlVpnData

# pylint: disable=duplicate-code


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


class TestAbstractVpnData:
    '''
    Test AbstractVpnData class
    '''
    mock_vpn_id: str = 'test_id'
    sut: AbstractVpnData = PritunlVpnData(mock_vpn_id)

    def test_get_vpn_id(self):
        '''
        Test get_vpn_id method
        '''
        # Act
        actual_vpn_id: str = TestAbstractVpnData.sut.get_vpn_id()

        # Assert
        assert TestAbstractVpnData.mock_vpn_id == actual_vpn_id

    def test_get_vpn_type(self):
        '''
        Test get_vpn_type method
        '''
        # Act
        actual_vpn_type: VpnType = TestAbstractVpnData.sut.get_vpn_type()

        # Assert
        assert VpnType.PRITUNL == actual_vpn_type

    def test_visit(self):
        '''
        Test visiting VPN type
        '''
        # Arrange
        test_visitor: _TestVpnTypeVisitor = _TestVpnTypeVisitor()

        # Act
        actual_vpn_type: VpnType = TestAbstractVpnData.sut.visit(test_visitor)

        # Assert
        assert VpnType.PRITUNL == actual_vpn_type

    def test_to_json(self):
        '''
        Test to_json method
        '''
        # Act
        actual_json: dict = TestAbstractVpnData.sut.to_json()
        expected_json: dict = {
            'vpn_id': 'test_id',
            'vpn_type': 'PRITUNL',
            'pin': '', 
            'totp_url': '',
            'token': ''
        }

        # Assert
        assert expected_json == actual_json

    def test_from_json(self):
        '''
        Test from_json method
        '''
        # Arrange
        json_str: dict = {'vpn_id': 'test_id', 'vpn_type': ''}

        # Act
        with pytest.raises(TypeError) as excinfo:
            AbstractVpnData.from_json(json_str)

            # Assert
            assert excinfo.match(
                'Can\'t instantiate abstract class AbstractVpnData with abstract methods'
            )
