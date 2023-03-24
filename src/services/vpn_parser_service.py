from json import loads

from src.models.vpn_data.interface import VpnDataInterface, VPN_TYPE_KEY
from src.models.vpn_data.pritunl_vpn_data import PritunlVpnData
from src.enums.vpn_data.vpn_type import VpnTypeVisitor, VpnType

class _VpnParsingVisitor(VpnTypeVisitor[VpnDataInterface]):
    def __init__(self, json: dict) -> None:
        self.json: dict = json
    
    def visit_pritunl(self) -> VpnDataInterface:
        return PritunlVpnData.from_json(self.json)

    def visit_wireguard(self) -> VpnDataInterface:
        """Visit Wireguard VPN data."""
        raise NotImplementedError

    def visit_none(self) -> VpnDataInterface:
        raise ValueError("Invalid VPN type")

class VpnParserService:
    def parse_vpn_data(self, vpn_data: str) -> list[VpnDataInterface]:
        vpn_list: list[VpnDataInterface] = []
        for vpn_json in loads(vpn_data):
            vpn_type: VpnType = VpnType(vpn_json[VPN_TYPE_KEY])
            vpn: VpnDataInterface = vpn_type.visit(_VpnParsingVisitor(vpn_json))
            vpn_list.append(vpn)
        return vpn_list
