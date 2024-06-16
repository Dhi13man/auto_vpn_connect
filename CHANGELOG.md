# Releases

## [0.0.2] - 16th June 2024

1. Integrated one-step [Palo Alto Global Protect](https://docs.paloaltonetworks.com/globalprotect) VPN connection/disconnection.
2. Decoupled VPN Config and VPN Data Models for future flexibility.
3. Removed unnecessary Zope Interfaces dependency as it does not seem worth the maintenance effort.
4. Upgraded `pyinstaller` dependency to leave vulnerable version.

## [0.0.1] - 25th March 2023

Initial implementation of the base features of the auto_vpn_connect script:

1. Connect/Disconnect and set up Auto-Connect to Pritunl VPNs.
2. Save PINs, Tokens and auto fetch TOTPs using pyotp by providing the TOTP URL to minimise the effort to connect to VPNs, after a one-time setup.
3. Set up customisable JSON VPN profiles and configs to customise where various CLIs and dependencies might be located
4. Extensibility to add other VPN clients with ease.
