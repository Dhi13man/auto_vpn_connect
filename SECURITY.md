# Security policy

## Supported versions

Security fixes are made on the `main` branch. The v0.0.1 and v0.0.2 executables
predate the current security fixes and are not supported.

## Reporting a vulnerability

Report vulnerabilities through
[GitHub private vulnerability reporting](https://github.com/Dhi13man/auto_vpn_connect/security/advisories/new).
Do not include secrets or exploit details in a public issue.

Include the affected version or commit, operating system, reproduction steps,
impact, and any suggested mitigation. You can expect:

- Acknowledgement within 7 days
- A status update at least every 14 days while the report remains open
- A remediation target of 30 days for confirmed critical or high-severity issues

These are response targets, not disclosure deadlines. We will coordinate a
release and credit with the reporter when appropriate.

## Local secret handling

`vpn_data.json` can contain PINs, tokens, and TOTP secrets. The file is ignored
by Git; keep it outside shared folders, restrict its filesystem permissions,
and remove it before sharing logs or support bundles. Verbose mode intentionally
omits authentication values.
