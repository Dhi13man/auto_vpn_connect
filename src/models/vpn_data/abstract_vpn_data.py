from subprocess import CompletedProcess
from abc import ABC, abstractmethod

from src.enums.vpn_data.vpn_type import VpnType, VpnTypeVisitor, T

VPN_ID_KEY: str = "id"
VPN_TYPE_KEY: str = "vpn_type"

class AbstractVpnData(ABC):
    @abstractmethod
    def get_id(self) -> str:
        raise NotImplementedError
    
    @abstractmethod
    def get_vpn_type() -> VpnType:
        return VpnType.NONE
    
    @abstractmethod
    def connect(self, verbose: bool) -> CompletedProcess:
        raise NotImplementedError

    @abstractmethod
    def disconnect(self, verbose: bool) -> CompletedProcess:
        raise NotImplementedError
    
    def visit(self, visitor: "VpnTypeVisitor[T]") -> T:
        return visitor.visit_none()
    
    def get_global_id(self) -> str:
        return f"{self.get_vpn_type()}_{self.get_id()}"
    
    @abstractmethod
    def to_json(self) -> str:
        raise NotImplementedError
    
    @abstractmethod
    def from_json(json: dict) -> "AbstractVpnData":
        raise NotImplementedError
