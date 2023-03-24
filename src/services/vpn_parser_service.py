from json import loads
from zope.interface import implementer

from src.models.vpn_data.abstract_vpn_data import AbstractVpnData, VPN_TYPE_KEY
from src.models.vpn_data.pritunl_vpn_data import PritunlVpnData
from src.enums.vpn_data.vpn_type import VpnTypeVisitor, VpnType

@implementer(VpnTypeVisitor)
class _VpnParsingVisitor:
    def __init__(self, json: dict):
        self.json: dict = json

    def visit_pritunl(self) -> AbstractVpnData:
        return PritunlVpnData.from_json(self.json)

    def visit_wireguard(self) -> AbstractVpnData:
        raise NotImplementedError

    def visit_openvpn(self) -> AbstractVpnData:
        raise NotImplementedError

    def visit_none(self) -> AbstractVpnData:
        raise ValueError("Invalid VPN type")

class VpnParserService:
    def parse_vpn_data(self, vpn_data: str) -> list[AbstractVpnData]:
        vpn_list: list[AbstractVpnData] = []
        for vpn_json in loads(vpn_data):
            vpn_type: VpnType = VpnType(vpn_json[VPN_TYPE_KEY])
            vpn: AbstractVpnData = vpn_type.visit(_VpnParsingVisitor(vpn_json))
            vpn_list.append(vpn)
        return vpn_list
