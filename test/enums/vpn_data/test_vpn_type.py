'''
Test VPN type enum module
'''

from zope.interface import implementer

from src.enums.vpn_type import VpnType, VpnTypeVisitor

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


class TestVpnType:
    '''
    Test VPN type enum
    '''

    def test_vpn_type(self) -> None:
        '''
        Test VPN type enum
        '''
        # Arrange
        expected_vpn_type_pritunl: str = 'PRITUNL'
        expected_vpn_type_none: str = ''

        # Act
        actual_vpn_type_pritunl: str = VpnType.PRITUNL.value
        actual_vpn_type_none: str = VpnType.NONE.value

        # Assert
        assert expected_vpn_type_pritunl == actual_vpn_type_pritunl
        assert expected_vpn_type_none == actual_vpn_type_none

    def test_visit(self) -> None:
        '''
        Test visiting VPN type
        '''
        # Arrange
        test_visitor: _TestVpnTypeVisitor = _TestVpnTypeVisitor()

        # Act and Assert
        assert VpnType.PRITUNL.visit(test_visitor) == VpnType.PRITUNL
        assert VpnType.WIREGUARD.visit(test_visitor) == VpnType.WIREGUARD
        assert VpnType.OPEN_VPN.visit(test_visitor) == VpnType.OPEN_VPN
        assert VpnType.NONE.visit(test_visitor) == VpnType.NONE
