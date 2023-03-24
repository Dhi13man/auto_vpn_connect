'''
This module contains the UserSwitches data model.
'''


class UserSwitches:
    '''
    This data model contains the user switches for the application.

    Attributes:
        action (str): Action to take. "w" for always-connected, "c" for connect, "d" for disconnect
        vpn_data_json_path (str): The path to the VPN data JSON file
        verbose (bool): Whether to run in verbose mode. DEFAULT false
    '''

    def __init__(self, action: chr, vpn_data_json_path: str, verbose: bool = False):
        self.action: chr = action
        self.vpn_data_json_path: str = vpn_data_json_path
        self.verbose: bool = verbose

    def get_action(self) -> chr:
        '''
        Get the action to take.

        Returns:
            chr: Action to take. "w" for always-connected, "c" for connect, "d" for disconnect
        '''
        return self.action

    def get_vpn_data_json_path(self) -> str:
        '''
        Get the path to the VPN data JSON file.

        Returns:
            str: The path to the VPN data JSON file
        '''
        return self.vpn_data_json_path

    def is_verbose(self) -> bool:
        '''
        Get whether to run in verbose mode.

        Returns:
            bool: Whether to run in verbose mode. DEFAULT false
        '''
        return self.verbose
