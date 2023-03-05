from pyotp import totp, parse_uri

from subprocess import run, CompletedProcess

import zope.interface

import src.models.vpn_data.interface as vdi

@zope.interface.implementer(vdi.VpnDataInterface)
class PritunlVpnData:
  id: str
  pin: str
  token: str
  totp_url: str
  totp_obj: totp.TOTP

  def __init__(self, id: str, *, pin: str="", totp_url: str="", token: str = "") -> None:
    self.id: str = id
    self.pin: str = pin
    self.token: str = token
    self.totp_url: str = totp_url
    self.totp_obj: totp.TOTP = parse_uri(totp_url) if totp_url else None

  def get_id(self) -> str:
    return self.id

  def get_pin(self) -> str:
    return self.pin
  
  def get_token(self) -> str:
    return self.token

  def get_totp(self) -> str:
    return self.totp_obj.now() if self.totp_obj else ""

  def disconnect(self) -> CompletedProcess:
    return run([
     "/Applications/Pritunl.app/Contents/Resources/pritunl-client",
     "stop",
     self.get_id()
    ])

  def connect(self) -> CompletedProcess:
    pin: str = self.get_pin()
    totp: str = self.get_totp()
    token: str = self.get_token()
    return run([
      "/Applications/Pritunl.app/Contents/Resources/pritunl-client",
      "start",
      self.get_id(),
      "-p",
      f"{pin}{totp}{token}"
    ])