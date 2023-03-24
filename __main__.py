#!/usr/bin/env python3

from threading import Thread
import argparse

from src.models.user_switches import UserSwitches
from src.models.vpn_data import abstract_vpn_data
from src.services.vpn_parser_service import VpnParserService

PROMPT: str = "Run in Connect (c), Disconnect (d), or be in Always-Connected mode (w)"
DEFAULT_VPN_DATA_PATH: str = "./vpn_data.json"

def get_user_switches() -> UserSwitches:
  parser: argparse.ArgumentParser = argparse.ArgumentParser()
  parser.add_argument("-s", "--switch", help=PROMPT, type=str)
  parser.add_argument("-p", "--path", help="Path to VPN data JSON file", type=str, required=False)
  parser.add_argument("-v", "--verbose", help="Whether to run in verbose mode. DEFAULT false", type=bool, default=False, required=False)
  parser.print_help()
  args: argparse.Namespace = parser.parse_args()
  return UserSwitches(
    args.switch if args.switch else input(f"{PROMPT}: ").lower(),
    args.path if args.path else DEFAULT_VPN_DATA_PATH,
    args.verbose if args.verbose else False
  )

if __name__ == "__main__":
  # Get and Validate user switch to know whether to connect or disconnect VPNs
  user_switches: UserSwitches = get_user_switches()
  if user_switches.action not in ["w", "c", "d"]:
    raise ValueError(f"Invalid switch. {PROMPT}!'")

  # List all VPNs
  vpn_data_list: list[abstract_vpn_data.AbstractVpnData] = []
  with open(user_switches.vpn_data_json_path, "r") as f:
    vpn_parser_service: VpnParserService = VpnParserService()
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
    for t in threads: t.join()
    
    # If not in watch mode, exit
    if user_switches.action != 'w': break
    
