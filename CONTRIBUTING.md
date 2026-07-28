# Contributing to auto_vpn_connect

Contributions are welcome for supported VPN behavior, tests, security fixes,
and documentation. By participating, you agree to follow the
[Code of Conduct](.github/CODE_OF_CONDUCT.md).

## Before you start

- Search [existing issues](https://github.com/Dhi13man/auto_vpn_connect/issues).
- Open an issue before large behavior or compatibility changes.
- Never commit VPN profiles, PINs, tokens, TOTP secrets, or private endpoints.

Security vulnerabilities belong in the private reporting channel described in
[SECURITY.md](SECURITY.md).

## Development setup

```bash
git clone https://github.com/Dhi13man/auto_vpn_connect.git
cd auto_vpn_connect
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
```

On Windows, activate the environment with `.venv\Scripts\activate`.

## Tests and checks

Run these commands before submitting a pull request:

```bash
flake8 $(git ls-files '*.py') --count --select=E9,F63,F7,F82 --show-source --statistics
pylint $(git ls-files '*.py')
python -m pip_audit -r requirements-dev.txt
python -m pytest --cov=src --cov-report=term-missing --cov-fail-under=70
pyinstaller --onefile --noconsole --name auto_vpn_connect __main__.py
```

Tests for VPN behavior must mock subprocess execution. Automated tests must not
connect to a VPN or invoke Pritunl, GlobalProtect, `launchctl`, or `pkill`.

## Pull requests

- Keep each pull request focused on one coherent change.
- Explain why the change is needed and any compatibility trade-offs.
- Add deterministic tests for success and failure paths.
- Update user-facing documentation when behavior changes.
- Confirm that all GitHub checks pass.

Pull requests are reviewed under the terms of the [MIT License](LICENSE).
