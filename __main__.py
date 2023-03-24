#!/usr/bin/env python3

from threading import Thread
from sys import argv

from src.models.vpn_data import interface
from src.services.vpn_parser_service import VpnParserService

PROMPT: str = "Please enter whether you would like to Connect (c), Disconnect (d), or be in Always-Connect mode (w)"

def get_switch() -> chr:
  if len(argv) < 2:
    return input(f"{PROMPT}: ").lower()
  else:
    return argv[1].lower()

if __name__ == "__main__":
  # Get and Validate user switch to know whether to connect or disconnect VPNs
  switch: chr = get_switch()
  if switch not in ["w", "c", "d"]:
    raise ValueError(f"Invalid switch. {PROMPT}!'")

  # List all VPNs
  vpn_data_list: list[interface.VpnDataInterface] = []
  with open("./vpn_data.json", "r") as f:
    vpn_parser_service: VpnParserService = VpnParserService()
    vpn_data_list = vpn_parser_service.parse_vpn_data(f.read())

  while True:
    # Perform action on all VPNs
    threads: set[Thread] = set()
    for vpn in vpn_data_list:
      t: Thread = Thread(target=vpn.disconnect if switch == 'd' else vpn.connect)
      t.start()
      threads.add(t)

    # Ensure all threads complete before exit
    for t in threads: t.join()
    
    # If not in watch mode, exit
    if switch != 'w': break
    
