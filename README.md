# auto_vpn_connect

[![CI](https://github.com/Dhi13man/auto_vpn_connect/actions/workflows/python-app.yml/badge.svg)](https://github.com/Dhi13man/auto_vpn_connect/actions/workflows/python-app.yml)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/Dhi13man/auto_vpn_connect/badge)](https://scorecard.dev/viewer/?uri=github.com/Dhi13man/auto_vpn_connect)
[![Latest release](https://img.shields.io/github/v/release/Dhi13man/auto_vpn_connect)](https://github.com/Dhi13man/auto_vpn_connect/releases/latest)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Connect, disconnect, or keep supported VPN clients connected from one Python CLI.

Supported clients:

- [Pritunl Client](https://client.pritunl.com/)
- [Palo Alto GlobalProtect](https://docs.paloaltonetworks.com/globalprotect)

> **Warning**: The local configuration can contain VPN PINs, tokens, and TOTP
> secrets. Keep `vpn_data.json` private and never commit it.

## Prerequisites

- Python 3.10 or later when running from source
- The desktop client for each configured VPN
- Pritunl's `pritunl-client` command for Pritunl profiles
- macOS `launchctl` and `pkill` for the default GlobalProtect commands

## Installation

Download a platform executable from the
[releases page](https://github.com/Dhi13man/auto_vpn_connect/releases), or run
the source directly:

```bash
git clone https://github.com/Dhi13man/auto_vpn_connect.git
cd auto_vpn_connect
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On PowerShell, activate the environment with `.venv\Scripts\Activate.ps1`.

## Quick start

1. Copy the example configuration:

   ```bash
   cp vpn_data.example.json vpn_data.json
   ```

2. Replace the placeholders in `vpn_data.json` with your VPN profiles.

3. Restrict access to the file on Unix-like systems:

   ```bash
   chmod 600 vpn_data.json
   ```

4. Connect all configured VPNs:

   ```bash
   python __main__.py --action c --path vpn_data.json
   ```

For a downloaded executable, replace `python __main__.py` with its filename.

## Usage

```text
usage: __main__.py [-h] [-a ACTION] [-p PATH] [-v]
```

| Option | Purpose | Default |
| ------ | ------- | ------- |
| `-a`, `--action` | `c`, `d`, or `w` | Prompt |
| `-p`, `--path` | Path to the local VPN configuration | `./vpn_data.json` |
| `-v`, `--verbose` | Print profile names and return codes | Disabled |

Action `w` retries the connection every five seconds.

Examples:

```bash
python __main__.py --action c --path vpn_data.json
python __main__.py --action d --verbose
python __main__.py --action w --path /secure/path/vpn_data.json
```

Verbose output never prints configured PINs, TOTP values, or tokens.

## Configuration

Start from [`vpn_data.example.json`](vpn_data.example.json). Each item in
`vpn_list` requires a `vpn_id` and a supported `vpn_type`.

### Pritunl

| Field | Purpose |
| ----- | ------- |
| `vpn_id` | Profile ID from `pritunl-client list` or the client UI |
| `pin` | Optional profile PIN |
| `totp_url` | Optional `otpauth://` URI from the profile's TOTP setup |
| `token` | Optional profile token |
| `config.PRITUNL.cli_path` | Path to `pritunl-client` |

Pritunl combines the configured authentication values for the client's `-p`
argument. Other users on the same machine may be able to inspect process
arguments, so use this tool only on a trusted workstation.

### GlobalProtect

GlobalProtect uses the commands under `config.GLOBAL_PROTECT`. The defaults
load and unload Palo Alto's macOS launch agent, then send `SIGTERM` only to a
process whose exact name is `GlobalProtect`.

The command fields are executed directly without a shell. They still control
which local executables run, so edit them only in a trusted configuration.

## Development

Install the pinned development tools:

```bash
python -m pip install -r requirements-dev.txt
```

Run the same quality gates used in CI:

```bash
flake8 $(git ls-files '*.py') --count --select=E9,F63,F7,F82 --show-source --statistics
pylint $(git ls-files '*.py')
python -m pip_audit -r requirements-dev.txt
python -m pytest --cov=src --cov-report=term-missing --cov-fail-under=70
pyinstaller --onefile --noconsole --name auto_vpn_connect __main__.py
```

Tests mock subprocess and time boundaries. They do not run Pritunl,
GlobalProtect, `launchctl`, or `pkill`.

## Contributing and security

See [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request. Report
vulnerabilities through the process in [SECURITY.md](SECURITY.md), not a public
issue.

## License

Licensed under the [MIT License](LICENSE).
