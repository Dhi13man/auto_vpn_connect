# Pull request

## Why

Explain the user problem, security concern, or maintenance risk this addresses.

## What changed

- Summarize the smallest behaviorally relevant changes.

## Test plan

- [ ] Unit tests cover success and failure paths
- [ ] Subprocess and time boundaries are mocked
- [ ] `pylint`, `flake8`, `pip-audit`, pytest coverage, and PyInstaller build pass
- [ ] No VPN command or real credential was used during testing

## Compatibility and security

Describe affected VPN clients and operating systems. Confirm that logs,
fixtures, and screenshots contain no private configuration.
