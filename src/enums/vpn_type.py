'''
Module for VPN type enumeration.
'''

from enum import Enum
from typing import TypeVar

T = TypeVar('T')


class VpnType(Enum):
    '''
    VPN type enumeration.
    '''

    NONE: str = ''
    PRITUNL: str = 'PRITUNL'
    WIREGUARD: str = 'WIREGUARD'
    OPEN_VPN: str = 'OPEN_VPN'
    GLOBAL_PROTECT: str = 'GLOBAL_PROTECT'

    def visit(self, visitor: 'VpnTypeVisitor[T]') -> T:
        '''
        Visit the VPN type.

        Args:
            visitor (VpnTypeVisitor[T]): Visitor to visit the VPN type
        '''
        if self == VpnType.NONE:
            return visitor.visit_none()
        if self == VpnType.PRITUNL:
            return visitor.visit_pritunl()
        if self == VpnType.WIREGUARD:
            return visitor.visit_wireguard()
        if self == VpnType.OPEN_VPN:
            return visitor.visit_open_vpn()
        if self == VpnType.GLOBAL_PROTECT:
            return visitor.visit_global_protect()
        raise ValueError('VPN Type visit not implemented')

# pylint: disable-next=inherit-non-class
class VpnTypeVisitor:
    '''
    Visitor for VPN types. This is used to visit the VPN type and return the
    appropriate data.
    '''

    def visit_none(self) -> T:
        '''Visit None VPN data.'''
        raise NotImplementedError

    def visit_pritunl(self) -> T:
        '''Visit Pritunl VPN data.'''
        raise NotImplementedError

    def visit_wireguard(self) -> T:
        '''Visit Wireguard VPN data.'''
        raise NotImplementedError

    def visit_open_vpn(self) -> T:
        '''Visit OpenVPN VPN data.'''
        raise NotImplementedError

    def visit_global_protect(self) -> T:
        '''Visit GlobalProtect VPN data.'''
        raise NotImplementedError
