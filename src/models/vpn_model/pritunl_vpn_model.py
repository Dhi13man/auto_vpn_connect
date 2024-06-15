"""
This file contains the PritunlVpnData class, which is a concrete implementation of the 
AbstractVpnData class.
"""

from subprocess import run, CompletedProcess
from pyotp import totp, parse_uri

from src.models.vpn_model.abstract_vpn_model import AbstractVpnModel
from src.enums.vpn_type import VpnType, VpnTypeVisitor, T
from src.models.vpn_config.pritunl_vpn_config import PritunlVpnConfig


class PritunlVpnModel(AbstractVpnModel):
    """
    Concrete implementation of the AbstractVpnData class for Pritunl VPNs

    Attributes:
        id (str): ID of the Pritunl VPN
        pin (str): PIN of the Pritunl VPN
        token (str): Token of the Pritunl VPN
        totp_url (str): TOTP URL of the Pritunl VPN
        totp_obj (pyotp.TOTP): TOTP object of the Pritunl VPN
    """
    _vpn_type: VpnType = VpnType.PRITUNL
    _pin_key: str = "pin"
    _token_key: str = "token"
    _totp_url_key: str = "totp_url"

    def __init__(
        self,
        vpn_id: str,
        config: PritunlVpnConfig,
        *,
        pin: str = "",
        totp_url: str = "",
        token: str = "",
    ) -> None:
        super().__init__(vpn_id=vpn_id, config=config)
        self.cli_path: str = config.cli_path
        self.pin: str = pin
        self.totp_url: str = totp_url
        self.totp_obj: totp.TOTP = parse_uri(totp_url) if len(totp_url) > 0 else None
        self.token: str = token

    def get_vpn_type(self) -> VpnType:
        """
        Get the type of the Pritunl VPN.

        Returns:
            VpnType: Type of the VPN
        """
        return PritunlVpnModel._vpn_type

    def get_pin(self) -> str:
        """
        Get the PIN of the Pritunl VPN.

        Returns:
            str: PIN of the Pritunl VPN
        """
        return self.pin

    def get_token(self) -> str:
        """
        Get the token of the Pritunl VPN.

        Returns:
            str: Token of the Pritunl VPN
        """
        return self.token

    def get_totp(self) -> str:
        """
        Get the TOTP of the Pritunl VPN.

        Returns:
            str: TOTP of the Pritunl VPN
        """
        return self.totp_obj.now() if self.totp_obj else ""

    def connect(self, verbose: bool) -> CompletedProcess:
        """
        Connect to the Pritunl VPN.

        Args:
            verbose (bool): Whether to print the output of the connection process
        """
        pin: str = self.get_pin()
        vpn_totp: str = self.get_totp()
        token: str = self.get_token()
        if verbose:
            print(f"Connecting to {self.get_vpn_id()}...")
            print(f"Pin: {pin}; TOTP: {vpn_totp}; Token: {token}")
        process: CompletedProcess = run(
            [
                self.cli_path,
                "start",
                self.get_vpn_id(),
                "-p",
                f"{pin}{vpn_totp}{token}",
            ],
            check=False,
        )
        if verbose:
            print("Connect process completed!")
            print(f"Result: {process.stdout}; Error: {process.stderr}")
        return process

    def disconnect(self, verbose: bool) -> CompletedProcess:
        """
        Disconnect from the Pritunl VPN.

        Args:
            verbose (bool): Whether to print the output of the disconnection process
        """
        if verbose:
            print(f"Disconnecting from {self.get_vpn_id()}")
        process: CompletedProcess = run(
            [self.cli_path, "stop", self.get_vpn_id()],
            check=False,
        )
        if verbose:
            print("Disconnect process completed!")
            print(f"Result: {process.stdout}; Error: {process.stderr}")
        return process

    def visit(self, visitor: "VpnTypeVisitor[T]") -> T:
        """
        Visit the Pritunl VPN with a VpnTypeVisitor.

        Args:
            visitor (VpnTypeVisitor): Visitor to visit the Pritunl VPN with
        """
        return visitor.visit_pritunl()

    def to_json(self) -> dict:
        return {
            PritunlVpnModel.vpn_id_key: self.get_vpn_id(),
            PritunlVpnModel.vpn_type_key: self.get_vpn_type().value,
            PritunlVpnModel._pin_key: self.get_pin(),
            PritunlVpnModel._totp_url_key: self.totp_url,
            PritunlVpnModel._token_key: self.get_token(),
        }

    @staticmethod
    def from_json_with_config(json: dict, config: PritunlVpnConfig) -> "PritunlVpnModel":
        vpn_type: VpnType = VpnType(json.get(PritunlVpnModel.vpn_type_key))
        if vpn_type != PritunlVpnModel._vpn_type:
            raise ValueError(f"Invalid VPN type {vpn_type}")
        return PritunlVpnModel(
            vpn_id=json.get(PritunlVpnModel.vpn_id_key),
            config=config,
            pin=json.get(PritunlVpnModel._pin_key, ""),
            totp_url=json.get(PritunlVpnModel._totp_url_key, ""),
            token=json.get(PritunlVpnModel._token_key, ""),
        )
