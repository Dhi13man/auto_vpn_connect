"""
This file contains the PritunlVpnData class, which is a concrete implementation of the 
AbstractVpnData class.
"""

import hashlib
from subprocess import run, CompletedProcess
from urllib.parse import parse_qsl, unquote, urlparse

from pyotp import totp

from src.models.vpn_model.abstract_vpn_model import AbstractVpnModel
from src.enums.vpn_type import VpnType, VpnTypeVisitor, T
from src.models.vpn_config.pritunl_vpn_config import PritunlVpnConfig


class _PritunlTotp(totp.TOTP):
    """
    TOTP generator for secrets issued by a Pritunl server.

    pyotp >= 2.12 rejects secrets shorter than 112 bits, but Pritunl issues
    16-character Base32 (80-bit) secrets by default. As a client, this app has
    to generate codes for whatever secret the server issued, so it accepts
    80-bit secrets while still validating the Base32 encoding.
    """

    min_secret_length_bits = 80


_TOTP_DIGESTS: dict = {
    "SHA1": hashlib.sha1,
    "SHA256": hashlib.sha256,
    "SHA512": hashlib.sha512,
}


def parse_totp_url(totp_url: str) -> totp.TOTP:
    """
    Parse an ``otpauth://totp/...`` URI into a TOTP generator.

    Args:
        totp_url (str): Provisioning URI of the TOTP secret

    Returns:
        pyotp.TOTP: TOTP generator for the URI

    Raises:
        ValueError: If the URI is not a valid TOTP provisioning URI
    """
    parsed = urlparse(totp_url)
    if parsed.scheme != "otpauth" or parsed.netloc != "totp":
        raise ValueError("Not an otpauth://totp URI")
    params: dict = dict(parse_qsl(parsed.query))
    secret: str = params.get("secret", "")
    if not secret:
        raise ValueError("No secret found in URI")
    algorithm: str = params.get("algorithm", "SHA1").upper()
    if algorithm not in _TOTP_DIGESTS:
        raise ValueError("Invalid value for algorithm, must be SHA1, SHA256 or SHA512")
    label: list = parsed.path[1:].split(":", 1)
    return _PritunlTotp(
        secret,
        digits=int(params.get("digits", 6)),
        digest=_TOTP_DIGESTS[algorithm],
        name=unquote(label[-1]) or None,
        issuer=params.get("issuer") or (unquote(label[0]) if len(label) > 1 else None),
        interval=int(params.get("period", 30)),
    )


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

    # pylint: disable=R0913
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
        self.totp_obj: totp.TOTP = parse_totp_url(totp_url) if len(totp_url) > 0 else None
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
            print("Pritunl connect command completed!")
            print(f"Return code: {process.returncode}")
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
            print("Pritunl disconnect command completed!")
            print(f"Return code: {process.returncode}")
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
            PritunlVpnModel._vpn_id_key: self.get_vpn_id(),
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
            vpn_id=json.get(PritunlVpnModel._vpn_id_key),
            config=config,
            pin=json.get(PritunlVpnModel._pin_key, ""),
            totp_url=json.get(PritunlVpnModel._totp_url_key, ""),
            token=json.get(PritunlVpnModel._token_key, ""),
        )
