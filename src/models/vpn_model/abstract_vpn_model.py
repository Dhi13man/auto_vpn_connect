"""
Abstract class for VPN data.
"""

from subprocess import CompletedProcess
from abc import ABC, abstractmethod

from src.enums.vpn_type import VpnType, VpnTypeVisitor, T
from src.models.vpn_config.abstract_vpn_config import AbstractVpnConfig


class AbstractVpnModel(ABC):
    """
    Abstract class for VPN data.

    Attributes:
        vpn_id (str): ID of the VPN
    """

    _vpn_id_key: str = "vpn_id"
    vpn_type_key: str = "vpn_type"
    _vpn_type: VpnType = VpnType.NONE

    def __init__(self, vpn_id: str, config: AbstractVpnConfig) -> None:
        self.vpn_id: str = vpn_id
        self.config: AbstractVpnConfig = config

    def get_vpn_id(self) -> str:
        """
        Get the ID of the VPN.

        Returns:
            str: ID of the VPN
        """
        return self.vpn_id

    def get_vpn_type(self) -> VpnType:
        """
        Get the type of the VPN.

        Returns:
            VpnType: Type of the VPN
        """
        return AbstractVpnModel._vpn_type

    @abstractmethod
    def connect(self, verbose: bool) -> CompletedProcess:
        """
        Connect to the VPN.

        Args:
            verbose (bool): Whether to print the output of the connection process
        """
        raise NotImplementedError

    @abstractmethod
    def disconnect(self, verbose: bool) -> CompletedProcess:
        """
        Disconnect from the VPN.

        Args:
            verbose (bool): Whether to print the output of the disconnection process
        """
        raise NotImplementedError

    def visit(self, visitor: "VpnTypeVisitor[T]") -> T:
        """
        Visit the VPN with a VpnTypeVisitor.

        Args:
            visitor (VpnTypeVisitor): Visitor to visit the Pritunl VPN with
        """
        return visitor.visit_none()

    def get_global_vpn_id(self) -> str:
        """
        Get the global ID of the VPN.

        Returns:
            str: Global ID of the VPN. This is the ID of the VPN prefixed with the type of the VPN.
        """
        return f"{self.get_vpn_type().name}_{self.get_vpn_id()}"

    def to_json(self) -> dict:
        """
        Convert the VPN data to a JSON string.

        Returns:
            dict: JSON representation of the VPN data
        """
        return {
            AbstractVpnModel._vpn_id_key: self.get_vpn_id(),
            AbstractVpnModel.vpn_type_key: self.get_vpn_type().value,
        }

    @staticmethod
    def from_json_with_config(
        json: dict, config: AbstractVpnConfig
    ) -> "AbstractVpnModel":
        """
        Create a VPN data object from a JSON representation.

        Args:
            json (dict): JSON representation of the VPN data

        Returns:
            AbstractVpnModel: VPN data object
        """
        vpn_type: VpnType = VpnType(json.get(AbstractVpnModel.vpn_type_key))
        if vpn_type != AbstractVpnModel._vpn_type:
            raise ValueError(f"Invalid VPN type {vpn_type}")
        return AbstractVpnModel(
            vpn_id=json.get(AbstractVpnModel._vpn_id_key), config=config
        )
