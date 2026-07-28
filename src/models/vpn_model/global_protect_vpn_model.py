'''
This file contains the GlobalProtectVpnModel implementation of AbstractVpnModel.
'''

from shlex import split
from subprocess import run, CompletedProcess
from time import sleep

from src.models.vpn_config.global_protect_vpn_config import GlobalProtectVpnConfig
from src.models.vpn_model.abstract_vpn_model import AbstractVpnModel
from src.enums.vpn_type import VpnType, VpnTypeVisitor, T


class GlobalProtectVpnModel(AbstractVpnModel):
    '''
    Concrete AbstractVpnModel implementation for GlobalProtect VPNs.

    Attributes:
        vpn_id (str): ID of the GlobalProtect VPN
    '''

    _vpn_type: VpnType = VpnType.GLOBAL_PROTECT

    def __init__(self, vpn_id: str, config: GlobalProtectVpnConfig) -> None:
        super().__init__(vpn_id=vpn_id, config=config)
        self.service_load_command: str = config.service_load_command
        self.service_unload_command: str = config.service_unload_command
        self.process_kill_command: str = config.process_kill_command

    def get_vpn_type(self) -> VpnType:
        '''
        Get the type of the GlobalProtect VPN.

        Returns:
            VpnType: Type of the VPN
        '''
        return GlobalProtectVpnModel._vpn_type

    def connect(self, verbose: bool) -> CompletedProcess:
        '''
        Connect to the GlobalProtect VPN.

        Args:
            verbose (bool): Whether to print the output of the connection process
        '''
        if verbose:
            print(f'Connecting to {self.get_vpn_id()}...')
        process: CompletedProcess = run(split(self.service_load_command), check=False)
        if verbose:
            print('GlobalProtect connect command completed!')
            print(f'Return code: {process.returncode}')
        return process

    def disconnect(self, verbose: bool) -> CompletedProcess:
        '''
        Disconnect from the GlobalProtect VPN.

        Args:
            verbose (bool): Whether to print the output of the disconnection process
        '''
        if verbose:
            print(f'Disconnecting from {self.get_vpn_id()}')
        unloading_process: CompletedProcess = run(
            split(self.service_unload_command), check=False
        )
        sleep(1)
        kill_process: CompletedProcess = run(
            split(self.process_kill_command), check=False
        )
        if verbose:
            print('GlobalProtect disconnect commands completed!')
            print(f'Unload return code: {unloading_process.returncode}')
            print(f'Process stop return code: {kill_process.returncode}')
        return kill_process

    def visit(self, visitor: 'VpnTypeVisitor[T]') -> T:
        '''
        Visit the GlobalProtect VPN with a VpnTypeVisitor.

        Args:
            visitor (VpnTypeVisitor): Visitor to visit the GlobalProtect VPN with
        '''
        return visitor.visit_global_protect()

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
