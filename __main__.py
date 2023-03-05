#!/usr/bin/env python3

from threading import Thread

from src.models.vpn_data import interface
from src.models.vpn_data import pritunl_vpn_data

from sys import argv

def get_switch() -> chr:
  if len(argv) < 2:
    return input("Please enter whether you would like to Connect (c) or Disconnect (d): ").lower()
  else:
    return argv[1].lower()

if __name__ == "__main__":
  # Get and Validate user switch to know whether to connect or disconnect VPNs
  switch: chr = get_switch()
  if switch not in ["c", "d"]:
    raise ValueError("Invalid switch. Please enter either 'c' or 'd'")

  # List all VPNs
  vpn_data_list: list[interface.VpnDataInterface] = [
    pritunl_vpn_data.PritunlVpnData(id="", pin="", totp_url=""),
  ]

  # Perform action on all VPNs
  threads: set[Thread] = set()
  for vpn in vpn_data_list:
    t: Thread = Thread(target=vpn.connect if switch == 'c' else vpn.disconnect)
    t.start()
    threads.add(t)

  # Ensure all threads complete before exit
  for t in threads: t.join()
    
