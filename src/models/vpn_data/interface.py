from subprocess import CompletedProcess
from zope.interface import Interface, interfacemethod

from src.enums.vpn_data.vpn_type import VpnType

VPN_ID_KEY: str = "id"
VPN_TYPE_KEY: str = "vpn_type"

class VpnDataInterface(Interface):  
    @interfacemethod
    def get_id(self) -> str:
        raise NotImplementedError
    
    @interfacemethod
    def get_vpn_type() -> VpnType:
        return VpnType.NONE
    
    @interfacemethod
    def connect(self) -> CompletedProcess:
        raise NotImplementedError

    @interfacemethod
    def disconnect(self) -> CompletedProcess:
        raise NotImplementedError
    
    @interfacemethod
    def get_global_id(self) -> str:
        return f"{self.get_vpn_type()}_{self.get_id()}"
    
    @interfacemethod
    def to_json(self) -> str:
        raise NotImplementedError
    
    @interfacemethod
    def from_json(json: str) -> "VpnDataInterface":
        raise NotImplementedError
