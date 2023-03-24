'''
Module for VPN type enumeration.
'''

from enum import Enum
from typing import TypeVar
from zope.interface import interfacemethod, Interface

T = TypeVar('T')


class VpnType(Enum):
    '''
    VPN type enumeration.
    '''

    NONE: str = 'NONE'
    PRITUNL: str = 'PRITUNL'
    WIREGUARD: str = 'WIREGUARD'
    OPEN_VPN: str = 'OPEN_VPN'

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
        raise ValueError('VPN Type visit not implemented')


class VpnTypeVisitor(Interface):
    '''
    Visitor for VPN types. This is used to visit the VPN type and return the
    appropriate data.
    '''

    @interfacemethod
    def visit_pritunl(self) -> T:
        '''Visit Pritunl VPN data.'''
        raise NotImplementedError

    @interfacemethod
    def visit_wireguard(self) -> T:
        '''Visit Wireguard VPN data.'''
        raise NotImplementedError

    @interfacemethod
    def visit_open_vpn(self) -> T:
        '''Visit OpenVPN VPN data.'''
        raise NotImplementedError

    @interfacemethod
    def visit_none(self) -> T:
        '''Visit None VPN data.'''
        raise NotImplementedError
