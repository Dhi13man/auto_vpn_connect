from enum import Enum
from typing import TypeVar
from zope.interface import interfacemethod, Interface

T = TypeVar("T")

class VpnType(Enum):
    """VPN type enumeration."""
    
    NONE: str = "NONE"
    PRITUNL: str = "PRITUNL"
    WIREGUARD: str = "WIREGUARD" 
    OPEN_VPN: str = "OPEN_VPN"

    def visit(self, visitor: "VpnTypeVisitor[T]") -> T:
        """Visit VPN data."""
        if self == VpnType.NONE:
            return visitor.visit_none()
        elif self == VpnType.PRITUNL:
            return visitor.visit_pritunl()
        elif self == VpnType.WIREGUARD:
            return visitor.visit_wireguard()
        elif self == VpnType.OPEN_VPN:
            return visitor.visit_open_vpn()
        else:
            raise ValueError("VPN Type visit not implemented")

class VpnTypeVisitor(Interface):
    """Visitor for VPN types."""
    
    @interfacemethod
    def visit_pritunl(self) -> T:
        """Visit Pritunl VPN data."""
        raise NotImplementedError

    @interfacemethod
    def visit_wireguard(self) -> T:
        """Visit Wireguard VPN data."""
        raise NotImplementedError
    
    @interfacemethod
    def visit_open_vpn(self) -> T:
        """Visit OpenVPN VPN data."""
        raise NotImplementedError

    @interfacemethod
    def visit_none(self) -> T:
        """Visit None VPN data."""
        raise NotImplementedError
