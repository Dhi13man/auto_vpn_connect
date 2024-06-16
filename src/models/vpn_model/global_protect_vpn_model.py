'''
This file contains the PritunlVpnData class, which is a concrete implementation of the 
AbstractVpnData class.
'''

from subprocess import run, CompletedProcess
from time import sleep

from src.models.vpn_config.global_protect_vpn_config import GlobalProtectVpnConfig
from src.models.vpn_model.abstract_vpn_model import AbstractVpnModel
from src.enums.vpn_type import VpnType, VpnTypeVisitor, T


class GlobalProtectVpnModel(AbstractVpnModel):
    '''
    Concrete implementation of the AbstractVpnData class for Global Protect VPNs

    Attributes:
        id (str): ID of the Pritunl VPN
        pin (str): PIN of the Pritunl VPN
        token (str): Token of the Pritunl VPN
        totp_url (str): TOTP URL of the Pritunl VPN
        totp_obj (pyotp.TOTP): TOTP object of the Pritunl VPN
    '''

    _vpn_type: VpnType = VpnType.GLOBAL_PROTECT

    def __init__(self, vpn_id: str, config: GlobalProtectVpnConfig) -> None:
        super().__init__(vpn_id=vpn_id, config=config)
        self.service_load_command: str = config.service_load_command
        self.service_unload_command: str = config.service_unload_command
        self.process_kill_command: str = config.process_kill_command

    def get_vpn_type(self) -> VpnType:
        '''
        Get the type of the Pritunl VPN.

        Returns:
            VpnType: Type of the VPN
        '''
        return GlobalProtectVpnModel._vpn_type

    def connect(self, verbose: bool) -> CompletedProcess:
        '''
        Connect to the Pritunl VPN.

        Args:
            verbose (bool): Whether to print the output of the connection process
        '''
        if verbose:
            print(f'Connecting to {self.get_vpn_id()}...')
        process: CompletedProcess = run(self.service_load_command.split(), check=False)
        if verbose:
            print('Connect process completed!')
            print(f'Result: {process.stdout}; Error: {process.stderr}')
        return process

    def disconnect(self, verbose: bool) -> CompletedProcess:
        '''
        Disconnect from the Pritunl VPN.

        Args:
            verbose (bool): Whether to print the output of the disconnection process
        '''
        if verbose:
            print(f'Disconnecting from {self.get_vpn_id()}')
        unloading_process: CompletedProcess = run(self.service_unload_command.split(), check=False)
        sleep(1)
        kill_process: CompletedProcess = run(self.process_kill_command.split(), check=False)
        if verbose:
            print('Disconnect process completed!')
            print(
                f'Unloading Result: {unloading_process.stdout}; Error: {unloading_process.stderr}'
            )
            print(
                f'Kill Result: {kill_process.stdout}; Error: {kill_process.stderr}'
            )
        return kill_process

    def visit(self, visitor: 'VpnTypeVisitor[T]') -> T:
        '''
        Visit the Pritunl VPN with a VpnTypeVisitor.

        Args:
            visitor (VpnTypeVisitor): Visitor to visit the Pritunl VPN with
        '''
        return visitor.visit_pritunl()

    def to_json(self) -> dict:
        return {
            GlobalProtectVpnModel._vpn_id_key: self.get_vpn_id(),
            GlobalProtectVpnModel.vpn_type_key: self.get_vpn_type().value,
        }

    @staticmethod
    def from_json_with_config(json: dict, config) -> 'GlobalProtectVpnModel':
        vpn_type: VpnType = VpnType(json.get(GlobalProtectVpnModel.vpn_type_key))
        if vpn_type != GlobalProtectVpnModel._vpn_type:
            raise ValueError(f'Invalid VPN type {vpn_type}')
        return GlobalProtectVpnModel(
            vpn_id=json.get(GlobalProtectVpnModel._vpn_id_key),
            config=config
        )