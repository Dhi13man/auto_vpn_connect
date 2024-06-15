'''
This is the entry point for the VPN Switcher application.
'''

from threading import Thread
import argparse
from sys import exit as end
from time import sleep

from src.models.user_switches import UserSwitches
from vpn_model import abstract_vpn_model
from src.services.vpn_parser_service import VpnDataParserService

PROMPT: str = 'Run in Connect (c), Disconnect (d), or be in Always-Connected mode (w)'
DEFAULT_VPN_DATA_PATH: str = './vpn_data.json'


def get_user_switches() -> UserSwitches:
    '''
    Get user switches from command line arguments or prompt user for input.

    Returns:
      UserSwitches: User switches in a structured object
    '''
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('-a', '--action', help=PROMPT, type=str)
    parser.add_argument(
        '-p',
        '--path',
        help='Path to VPN data JSON file',
        type=str,
        required=False
    )
    parser.add_argument(
        '-v',
        '--verbose',
        help='Whether to run in verbose mode. DEFAULT false',
        type=bool,
        default=False,
        required=False
    )
    args: argparse.Namespace = parser.parse_args()
    if args.action is None and args.path is None and args.verbose is False:
        parser.print_help()
        end(0)
    return UserSwitches(
        args.action if args.action else input(f'{PROMPT}: ').lower(),
        args.path if args.path else DEFAULT_VPN_DATA_PATH,
        args.verbose if args.verbose else False
    )


if __name__ == '__main__':
    # Get and Validate user switch to know whether to connect or disconnect VPNs
    user_switches: UserSwitches = get_user_switches()
    if user_switches.action not in ['w', 'c', 'd']:
        raise ValueError(f'Invalid action switch. {PROMPT}!')

    # List all VPNs
    vpn_data_list: list[abstract_vpn_model.AbstractVpnModel] = []
    with open(user_switches.vpn_data_json_path, 'r', encoding='utf-8') as f:
        vpn_parser_service: VpnDataParserService = VpnDataParserService()
        vpn_data_list = vpn_parser_service.parse_vpn_data(f.read())

    while True:
        # Perform action on all VPNs
        threads: set[Thread] = set()
        for vpn in vpn_data_list:
            t: Thread = Thread(
                target=vpn.disconnect if user_switches.action == 'd' else vpn.connect,
                kwargs={'verbose': user_switches.verbose}
            )
            t.start()
            threads.add(t)

        # Ensure all threads complete
        for t in threads:
            t.join()

        # If not in watch mode, exit
        if user_switches.action != 'w':
            break

        sleep(5)
