'''
Abstract class for VPN data.
'''

from subprocess import CompletedProcess
from abc import ABC, abstractmethod

from src.enums.vpn_data.vpn_type import VpnType, VpnTypeVisitor, T


class AbstractVpnData(ABC):
    '''
    Abstract class for VPN data.

    Attributes:
        vpn_id (str): ID of the VPN
    '''

    vpn_id_key: str = "id"
    vpn_type_key: str = "vpn_type"
    _vpn_type: VpnType = VpnType.NONE

    def __init__(self, vpn_id: str) -> None:
        self.vpn_id: str = vpn_id

    @abstractmethod
    def get_vpn_id(self) -> str:
        '''
        Get the ID of the VPN.

        Returns:
            str: ID of the VPN
        '''
        raise self.vpn_id

    @abstractmethod
    def get_vpn_type(self) -> VpnType:
        '''
        Get the type of the VPN.

        Returns:
            VpnType: Type of the VPN
        '''
        return AbstractVpnData._vpn_type

    @abstractmethod
    def connect(self, verbose: bool) -> CompletedProcess:
        '''
        Connect to the VPN.

        Args:
            verbose (bool): Whether to print the output of the connection process
        '''
        raise NotImplementedError

    @abstractmethod
    def disconnect(self, verbose: bool) -> CompletedProcess:
        '''
        Disconnect from the VPN.

        Args:
            verbose (bool): Whether to print the output of the disconnection process
        '''
        raise NotImplementedError

    def visit(self, visitor: "VpnTypeVisitor[T]") -> T:
        '''
        Visit the VPN with a VpnTypeVisitor.

        Args:
            visitor (VpnTypeVisitor): Visitor to visit the Pritunl VPN with
        '''
        return visitor.visit_none()

    def get_global_id(self) -> str:
        '''
        Get the global ID of the VPN.

        Returns:
            str: Global ID of the VPN. This is the ID of the VPN prefixed with the type of the VPN.
        '''
        return f"{self.get_vpn_type()}_{self.get_vpn_id()}"

    @abstractmethod
    def to_json(self) -> str:
        '''
        Convert the VPN data to a JSON string.

        Returns:
            str: JSON string of the VPN data
        '''
        return {'vpn_id': self.get_vpn_id(), 'vpn_type': self.get_vpn_type()}

    @staticmethod
    def from_json(json: dict) -> "AbstractVpnData":
        '''
        Create a VPN data object from a JSON string.

        Args:
            json (dict): JSON string of the VPN data
        '''
        vpn_type: VpnType = VpnType(json[AbstractVpnData.vpn_type_key])
        if vpn_type != AbstractVpnData._vpn_type:
            raise ValueError(f"Invalid VPN type {vpn_type} for PritunlVpnData")
        return AbstractVpnData(vpn_id=json[AbstractVpnData.vpn_id_key])
