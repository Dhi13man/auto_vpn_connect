# auto_vpn_connect

[![License](https://img.shields.io/github/license/dhi13man/auto_vpn_connect)](https://github.com/Dhi13man/auto_vpn_connect/blob/main/LICENSE)
[![Language](https://img.shields.io/badge/language-Dart-blue.svg)](https://dart.dev)
[![Language](https://img.shields.io/badge/language-Flutter-blue.svg)](https://flutter.dev)
[![Contributors](https://img.shields.io/github/contributors-anon/dhi13man/auto_vpn_connect?style=flat)](https://github.com/Dhi13man/auto_vpn_connect/graphs/contributors)
[![GitHub forks](https://img.shields.io/github/forks/dhi13man/auto_vpn_connect?style=social)](https://github.com/Dhi13man/auto_vpn_connect/network/members)
[![GitHub Repo stars](https://img.shields.io/github/stars/dhi13man/auto_vpn_connect?style=social)](https://github.com/Dhi13man/auto_vpn_connect/stargazers)
[![Last Commit](https://img.shields.io/github/last-commit/dhi13man/auto_vpn_connect)](https://github.com/Dhi13man/auto_vpn_connect/commits/main)
[![auto_vpn_connect version](https://img.shields.io/pub/v/auto_vpn_connect.svg)](https://pub.dev/packages/auto_vpn_connect)
[!["Buy Me A Coffee"](https://img.buymeacoffee.com/button-api/?text=Buy%20me%20an%20Ego%20boost&emoji=%F0%9F%98%B3&slug=dhi13man&button_colour=FF5F5F&font_colour=ffffff&font_family=Lato&outline_colour=000000&coffee_colour=FFDD00****)](https://www.buymeacoffee.com/dhi13man)

A Python script that allows users to automatically connect to VPNs with minimal effort. As of now, only Pritunl VPNs are supported.

## Usage

1. Go to the [releases](https://github.com/Dhi13man/auto_proxy_wifi/releases) page and download the latest release binary, or clone this repository.

2. In the same directory as the script, or inside the root of the repository, create a file called `vpn_data.json` and fill it with the following information (replace the values with your own):

    ```json
    [
        {
            "id": "<vpn_id_1>",
            "vpn_type": "PRITUNL",
            "pin": "<vpn_pin_1>",
        },
        {
            "id": "<vpn_id_2>",
            "vpn_type": "PRITUNL",
            "pin": "<vpn_pin_2>",
            "totp_url": "<totp_url>"
        },
        {
            "id": "<vpn_id_3>",
            "vpn_type": "PRITUNL", 
            "pin": "<vpn_pin_3>",
            "token": "<vpn_token>"
        },
    ]
    ```

3. After ensuring that the `vpn_data.json` is proper, run the downloaded binary, or the script with `python3 -m .` from the root of the repository.

### User Switches

1. Action Switch `-a` / `--action` (optional): The action switch allows the user to specify the action that the script should perform. If the action switch is not specified, the script will run in interactive mode, which will prompt the user to select an action.

    ```bash
    cd <path_to_script>
    ./auto_vpn_connect --action <action>
    ```

    ```bash
    cd <path_to_repository>
    python3 -m . --action <action> 
    ```

    Running with action switch will run the script with the specified action. The available actions are:

    - `c`: Connects to the VPNs
    - `d`: Disconnects from the VPNs
    - `w`: Runs the script in watch mode, which will automatically re-attempt connecting to the VPNs when they disconnect.

2. VPN Data Path Switch `-p` / `--path` (optional): The VPN Data Path Switch allows the user to specify the absolute path to the `vpn_data.json` file. If the switch is not specified, the script will look for the file in the directory it is run from, or in the root of the repository, if the script is run from the root of the cloned repository.

    ```bash
    cd <path_to_script>
    ./auto_vpn_connect --vpn_data_path <path_to_vpn_data.json>
    ```

    ```bash
    cd <path_to_repository>
    python3 -m . --vpn_data_path <path_to_vpn_data.json>
    ```

3. Verbose Switch `-v` / `--verbose` (optional): The verbose switch allows the user to specify whether the script should print verbose output. If the switch is not specified, the script will run in non-verbose mode.

    ```bash
    cd <path_to_script>
    ./auto_vpn_connect --verbose
    ```

    ```bash
    cd <path_to_repository>
    python3 -m . --verbose
    ```

### Examples

```bash
cd <path_to_script>
./auto_vpn_connect --action c --vpn_data_path <path_to_folder>/vpn_data.json --verbose true
```

```bash
cd <path_to_repository>
python3 -m . --action w --vpn_data_path <path_to_folder>/vpn_data.json --verbose false
```

```bash
cd <path_to_script>
./auto_vpn_connect --action d
```

## Development

### Setup

1. Clone the repository
2. Install the [Development Dependencies](#dependencies) with `pip3 install -r requirements.txt`
3. Run `python3 -m .` from the root of the repository

### Dependencies

- Python 3.10+
- [pyotp](https://pypi.org/project/pyotp/): Used for generating OTPs
- [zope](https://pypi.org/project/zope/): Used for type hinting

### Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.
