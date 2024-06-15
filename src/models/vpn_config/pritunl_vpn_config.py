'''
Abstract class for VPN data.
'''

from src.enums.vpn_type import VpnType, VpnTypeVisitor, T
from src.models.vpn_config.abstract_vpn_config import AbstractVpnConfig

class PritunlVpnConfig(AbstractVpnConfig):
    '''
    Abstract class for VPN data.

    Attributes:
        vpn_id (str): ID of the VPN
    '''

    vpn_type_key: str = 'vpn_type'
    _vpn_type: VpnType = VpnType.PRITUNL
    cli_path_key: str = "cli_path"
    default_cli_path: str = "/Applications/Pritunl.app/Contents/Resources/pritunl-client"

    def __init__(self, cli_path: str=default_cli_path) -> None:
        self.cli_path = cli_path

    def get_vpn_type(self) -> VpnType:
        '''
        Get the type of the VPN.

        Returns:
            VpnType: Type of the VPN
        '''
        return PritunlVpnConfig._vpn_type

    def visit(self, visitor: 'VpnTypeVisitor[T]') -> T:
        '''
        Visit the VPN with a VpnTypeVisitor.

        Args:
            visitor (VpnTypeVisitor): Visitor to visit the Pritunl VPN with
        '''
        return visitor.visit_none()

    def to_json(self) -> dict:
        '''
        Convert the VPN data to a JSON string.

        Returns:
            str: JSON string of the VPN data
        '''
        return {
            AbstractVpnConfig.vpn_type_key: self.get_vpn_type().value,
            PritunlVpnConfig.cli_path_key: self.cli_path
        }

    @staticmethod
    def from_json(json: dict) -> 'PritunlVpnConfig':
        '''
        Create a VPN data object from a JSON string.

        Args:
            json (dict): JSON string of the VPN data
        '''
        vpn_type: VpnType = VpnType(json[PritunlVpnConfig.vpn_type_key])
        if vpn_type != PritunlVpnConfig._vpn_type:
            raise ValueError(f'Invalid VPN type {vpn_type} for AbstractVpnConfig')
        return PritunlVpnConfig(cli_path=json[PritunlVpnConfig.cli_path_key])
