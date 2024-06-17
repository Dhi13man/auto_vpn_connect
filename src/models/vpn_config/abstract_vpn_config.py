"""
Abstract class for VPN data.
"""

from abc import ABC

from src.enums.vpn_type import VpnType, VpnTypeVisitor, T


class AbstractVpnConfig(ABC):
    """
    Abstract class for VPN data.
    """

    _vpn_type_key: str = "vpn_type"
    _vpn_type: VpnType = VpnType.NONE

    def get_vpn_type(self) -> VpnType:
        """
        Get the type of the VPN.

        Returns:
            VpnType: Type of the VPN
        """
        return AbstractVpnConfig._vpn_type

    def visit(self, visitor: "VpnTypeVisitor[T]") -> T:
        """
        Visit the VPN with a VpnTypeVisitor.

        Args:
            visitor (VpnTypeVisitor): Visitor to visit the Pritunl VPN with
        """
        return visitor.visit_none()

    def to_json(self) -> dict:
        """
        Convert the VPN data to a JSON representation.

        Returns:
            str: JSON representation of the VPN data
        """
        return {AbstractVpnConfig._vpn_type_key: self.get_vpn_type().value}

    @staticmethod
    def from_json(json: dict) -> "AbstractVpnConfig":
        """
        Create a VPN data object from a JSON representation.

        Args:
            json (dict): JSON representation of the VPN data

        Returns:
            AbstractVpnConfig: VPN data object
        """
        vpn_type: VpnType = VpnType(
            json.get(AbstractVpnConfig._vpn_type_key, VpnType.NONE)
        )
        if vpn_type != AbstractVpnConfig._vpn_type:
            raise ValueError(f"Invalid VPN type {vpn_type}")
        return AbstractVpnConfig()
