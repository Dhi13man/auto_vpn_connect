from pyotp import totp, parse_uri
from subprocess import run, CompletedProcess
from zope.interface import implementer

from src.models.vpn_data.interface import VpnDataInterface, VPN_ID_KEY, VPN_TYPE_KEY
from src.enums.vpn_data.vpn_type import VpnType

@implementer(VpnDataInterface)
class PritunlVpnData:
  _cli_path: str = "/Applications/Pritunl.app/Contents/Resources/pritunl-client"
  _pin_key: str = "pin"
  _token_key: str = "token"
  _totp_url_key: str = "totp_url"

  def __init__(self, id: str, *, pin: str="", totp_url: str="", token: str = "") -> None:
    self.id: str = id
    self.pin: str = pin
    self.token: str = token
    self.totp_url: str = totp_url
    self.totp_obj: totp.TOTP = parse_uri(totp_url) if (totp_url and len(totp_url) > 0) else None

  def get_id(self) -> str:
    return self.id
  
  def get_vpn_type() -> VpnType:
    return VpnType.PRITUNL

  def get_pin(self) -> str:
    return self.pin
  
  def get_token(self) -> str:
    return self.token

  def get_totp(self) -> str:
    return self.totp_obj.now() if self.totp_obj else ""

  def connect(self) -> CompletedProcess:
    pin: str = self.get_pin()
    totp: str = self.get_totp()
    token: str = self.get_token()
    return run([
      PritunlVpnData._cli_path,
      "start",
      self.get_id(),
      "-p",
      f"{pin}{totp}{token}"
    ])

  def disconnect(self) -> CompletedProcess:
    return run([
     PritunlVpnData._cli_path,
     "stop",
     self.get_id()
    ])
  
  def to_json(self) -> dict:
    return {
      VPN_ID_KEY: self.get_id(),
      VPN_TYPE_KEY: self.get_vpn_type(),
      PritunlVpnData._pin_key: self.get_pin(),
      PritunlVpnData._totp_url_key: self.totp_url,
    }
    
  def from_json(json: dict) -> "PritunlVpnData":
    vpn_type: VpnType = VpnType(json[VPN_TYPE_KEY])
    if vpn_type != PritunlVpnData.get_vpn_type():
      raise ValueError(f"Invalid VPN type {vpn_type} for PritunlVpnData")
    return PritunlVpnData(
      id=json[VPN_ID_KEY],
      pin=json[PritunlVpnData._pin_key],
      totp_url=json[PritunlVpnData._totp_url_key],
    )