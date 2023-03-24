from enum import Enum
from typing import TypeVar, Generic
from zope.interface import Interface, interfacemethod

T = TypeVar("T")

class VpnType(Enum):
    """VPN type enumeration."""
    
    NONE: str = "NONE"
    PRITUNL: str = "PRITUNL"
    WIREGUARD: str = "WIREGUARD" 

    def visit(self, visitor: "VpnTypeVisitor[T]") -> T:
        """Visit VPN data."""
        if self == VpnType.NONE:
            return visitor.visit_none()
        elif self == VpnType.PRITUNL:
            return visitor.visit_pritunl()
        elif self == VpnType.WIREGUARD:
            return visitor.visit_wireguard()
        else:
            raise ValueError("Invalid VPN type")

class VpnTypeVisitor(Generic[T]):
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
    def visit_none(self) -> T:
        """Visit None VPN data."""
        raise NotImplementedError
