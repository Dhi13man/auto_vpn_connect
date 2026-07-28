# Releases

## Unreleased

### Security

- Prevent verbose Pritunl connections from logging PIN, TOTP, or token values.
- Replace broad forced GlobalProtect process termination with exact-name
  `SIGTERM`, and deprecate the v0.0.1 and v0.0.2 executables built before these
  fixes.

## [0.0.2] - 16th June 2024

1. Integrated one-step Palo Alto GlobalProtect VPN connection/disconnection.
2. Decoupled VPN Config and VPN Data Models for future flexibility.
3. Removed the unnecessary Zope Interfaces dependency to reduce maintenance.
4. Upgraded `pyinstaller` dependency to leave vulnerable version.

## [0.0.1] - 25th March 2023

Initial implementation of the base features of the auto_vpn_connect script:

1. Connect/Disconnect and set up Auto-Connect to Pritunl VPNs.
2. Save PINs and tokens, and fetch TOTPs from a configured `otpauth://` URI.
3. Configure VPN profiles and client executable locations with JSON.
4. Extensibility to add other VPN clients with ease.
