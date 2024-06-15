'''
Abstract class for VPN data.
'''

from src.enums.vpn_type import VpnType, VpnTypeVisitor, T
from src.models.vpn_config.abstract_vpn_config import AbstractVpnConfig

class GlobalProtectVpnConfig(AbstractVpnConfig):
    '''
    Abstract class for VPN data.

    Attributes:
        vpn_id (str): ID of the VPN
    '''

    _vpn_type: VpnType = VpnType.GLOBAL_PROTECT
    service_load_command_key: str = "service_load_command"
    servkce_unload_command_key: str = "service_unload_command"
    process_kill_command_key: str = "process_kill_command"
    default_service_load_command: str = (
        "launchctl load /Library/LaunchAgents/com.paloaltonetworks.gp.pangpa.plist"
    )
    default_service_unload_command: str = (
        "launchctl unload /Library/LaunchAgents/com.paloaltonetworks.gp.pangpa.plist"
    )
    default_process_kill_command: str = "pkill -9 -f GlobalProtect"

    def __init__(
        self,
        service_load_command: str = default_service_load_command,
        service_unload_command: str = default_service_unload_command,
        process_kill_command: str = default_process_kill_command
    ):
        self.service_load_command: str = service_load_command
        self.service_unload_command: str = service_unload_command
        self.process_kill_command: str = process_kill_command

    def get_vpn_type(self) -> VpnType:
        '''
        Get the type of the VPN.

        Returns:
            VpnType: Type of the VPN
        '''
        return GlobalProtectVpnConfig._vpn_type

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
            GlobalProtectVpnConfig.vpn_type_key: self.get_vpn_type().value,
            GlobalProtectVpnConfig.service_load_command_key: self.service_load_command,
            GlobalProtectVpnConfig.servkce_unload_command_key: self.service_unload_command,
            GlobalProtectVpnConfig.process_kill_command_key: self.process_kill_command
        }

    @staticmethod
    def from_json(json: dict) -> 'GlobalProtectVpnConfig':
        '''
        Create a VPN data object from a JSON string.

        Args:
            json (dict): JSON string of the VPN data
        '''
        vpn_type: VpnType = VpnType(
            json.get(GlobalProtectVpnConfig.vpn_type_key, VpnType.GLOBAL_PROTECT)
        )
        if vpn_type != GlobalProtectVpnConfig._vpn_type:
            raise ValueError(f'Invalid VPN type {vpn_type}')
        return GlobalProtectVpnConfig(
            service_load_command=json.get(GlobalProtectVpnConfig.service_load_command_key),
            service_unload_command=json.get(GlobalProtectVpnConfig.servkce_unload_command_key),
            process_kill_command=json.get(GlobalProtectVpnConfig.process_kill_command_key)
        )
