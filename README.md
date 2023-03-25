# auto_vpn_connect

[![License](https://img.shields.io/github/license/dhi13man/auto_vpn_connect)](https://github.com/Dhi13man/auto_vpn_connect/blob/main/LICENSE)
[![Contributors](https://img.shields.io/github/contributors-anon/dhi13man/auto_vpn_connect?style=flat)](https://github.com/Dhi13man/auto_vpn_connect/graphs/contributors)
[![GitHub forks](https://img.shields.io/github/forks/dhi13man/auto_vpn_connect?style=social)](https://github.com/Dhi13man/auto_vpn_connect/network/members)
[![GitHub Repo stars](https://img.shields.io/github/stars/dhi13man/auto_vpn_connect?style=social)](https://github.com/Dhi13man/auto_vpn_connect/stargazers)
[![Last Commit](https://img.shields.io/github/last-commit/dhi13man/auto_vpn_connect)](https://github.com/Dhi13man/auto_vpn_connect/commits/main)
[![Build, Format, Test](https://github.com/dhi13man/auto_vpn_connect/actions/workflows/python-app.yml/badge.svg)](https://github.com/Dhi13man/auto_vpn_connect/actions)

[![Language](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
[!["Buy Me A Coffee"](https://img.buymeacoffee.com/button-api/?text=Buy%20me%20an%20Ego%20boost&emoji=%F0%9F%98%B3&slug=dhi13man&button_colour=FF5F5F&font_colour=ffffff&font_family=Lato&outline_colour=000000&coffee_colour=FFDD00****)](https://www.buymeacoffee.com/dhi13man)

A Python script that allows users to automatically connect to VPNs with minimal effort. As of now, only [Pritunl VPNs](https://docs.pritunl.com/docs/command-line-interface) are supported.

## Usage

### Steps

1. Go to the [releases](https://github.com/Dhi13man/auto_vpn_connect/releases) page and download the latest release binary, or clone this repository.

2. In the same directory as the script, or inside the root of the repository, create a file called `vpn_data.json` and fill it with the following information (replace the values with your own):

    ```json
    {
        "config": {
            "PRITUNL": {
                "cli_path": "/Applications/Pritunl.app/Contents/Resources/pritunl-client"
            }
        },
        "vpn_list": [
            {
                "vpn_id": "<vpn_id_1>",
                "vpn_type": "PRITUNL",
                "pin": "<vpn_pin_1>",
            },
            {
                "vpn_id": "<vpn_id_2>",
                "vpn_type": "PRITUNL",
                "pin": "<vpn_pin_2>",
                "totp_url": "<totp_url>"
            },
            {
                "vpn_id": "<vpn_id_3>",
                "vpn_type": "PRITUNL", 
                "pin": "<vpn_pin_3>",
                "token": "<vpn_token>"
            },
        ]
    }
    ```

3. After ensuring that the `vpn_data.json` is proper, run the downloaded binary, or the script with `python3 -m .` from the root of the repository.

### User Switches

1. _Action Switch_ `-a` / `--action` (optional): The action switch allows the user to specify the action that the script should perform. If the action switch is not specified, the script will run in interactive mode, which will prompt the user to select an action.

    ```bash
    cd <path_to_script>
    ./auto_vpn_connect --action <action>
    ```

    ```bash
    cd <path_to_repository>
    python3 -m . -a <action> 
    ```

    Running with action switch will run the script with the specified action. The available actions are:

    - `c`: Connects to the VPNs
    - `d`: Disconnects from the VPNs
    - `w`: Runs the script in watch mode, which will automatically re-attempt connecting to the VPNs when they disconnect.

2. _VPN Data Path Switch_ `-p` / `--path` (optional): The VPN Data Path Switch allows the user to specify the absolute path to the `vpn_data.json` file. If the switch is not specified, the script will look for the file in the directory it is run from, or in the root of the repository, if the script is run from the root of the cloned repository.

    ```bash
    cd <path_to_script>
    ./auto_vpn_connect -p <path_to_vpn_data.json>
    ```

    ```bash
    cd <path_to_repository>
    python3 -m . --path <path_to_vpn_data.json>
    ```

3. _Verbose Switch_ `-v` / `--verbose` (optional): The verbose switch allows the user to specify whether the script should print verbose output. If the switch is not specified, the script will run in non-verbose mode.

    ```bash
    cd <path_to_script>
    ./auto_vpn_connect --verbose true
    ```

    ```bash
    cd <path_to_repository>
    python3 -m . -v true
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

#### Development Dependencies

- [Python 3.10+](https://www.python.org/downloads/): Used for developing the script
- [pyotp](https://pypi.org/project/pyotp/): Used for generating OTPs
- [zope.interface](https://pypi.org/project/zope.interface/): Used for type hinting

#### External Dependencies

- [Pritunl VPN Client](https://docs.pritunl.com/docs/command-line-interface): Used for connecting, disconnecting to VPNs (only supported VPN type as of now)

## Build

This project uses [PyInstaller](https://www.pyinstaller.org/) to build the binary. To build the binary, run the following command from the root of the repository:

```bash
pyinstaller --onefile --windowed __main__.py
```

This will create a `dist` folder in the root of the repository, which will contain the binary without any dependencies.

The binary can be run from anywhere following the [Usage](#usage) instructions.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Screenshots

| ![Connect using Repository with VPN Data Config Path Provided](https://raw.githubusercontent.com/Dhi13man/auto_vpn_connect/main/assets/screenshots/connect_vpn_data_config_path.png) |
|:--:|
| Connect using Repository, with VPN Data Config Path Provided |

| ![Disconnect with CLI in Verbose Mode](https://raw.githubusercontent.com/Dhi13man/auto_vpn_connect/main/assets/screenshots/disconnect_verbose.png) |
|:--:|
| Disconnect using CLI, in Verbose Mode |
