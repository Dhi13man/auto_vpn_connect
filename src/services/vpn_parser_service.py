'''
Module for parsing VPN data from JSON
'''

from json import loads
from zope.interface import implementer

from src.models.vpn_data.abstract_vpn_data import AbstractVpnData
from src.models.vpn_data.pritunl_vpn_data import PritunlVpnData
from src.enums.vpn_data.vpn_type import VpnTypeVisitor, VpnType


@implementer(VpnTypeVisitor)
class _VpnParsingVisitor:
    '''
    Visitor for parsing VPN data from JSON

    Attributes:
        json (dict): JSON data to parse
    '''

    def __init__(self, json: dict):
        self.json: dict = json

    def visit_pritunl(self) -> AbstractVpnData:
        '''Visit Pritunl VPN type'''
        return PritunlVpnData.from_json(self.json)

    def visit_wireguard(self) -> AbstractVpnData:
        '''Visit Wireguard VPN type'''
        raise NotImplementedError

    def visit_openvpn(self) -> AbstractVpnData:
        '''Visit OpenVPN VPN type'''
        raise NotImplementedError

    def visit_none(self) -> AbstractVpnData:
        '''Visit VPN type not specified'''
        raise ValueError('Invalid VPN type')


class VpnDataParserService:
    '''
    Service for parsing VPN data from JSON

    Attributes:
        vpn_data (str): VPN data to parse
    '''

    _vpn_list_key: str = 'vpn_list'
    _config_key: str = 'config'

    def parse_vpn_data(self, vpn_data: str) -> list[AbstractVpnData]:
        '''
        Parse VPN data from JSON.

        Also injects any global configs into the VPN data classes.

        Args:
            vpn_data (str): VPN data to parse

        Returns:
            list[AbstractVpnData]: List of VPN data objects
        '''
        vpn_data_dict: dict = loads(vpn_data)
        self.inject_configs(vpn_data_dict.get(
            VpnDataParserService._config_key, {}))
        vpn_list: list[AbstractVpnData] = []
        for vpn_json in vpn_data_dict[VpnDataParserService._vpn_list_key]:
            vpn_type: VpnType = VpnType(vpn_json[AbstractVpnData.vpn_type_key])
            vpn: AbstractVpnData = vpn_type.visit(_VpnParsingVisitor(vpn_json))
            vpn_list.append(vpn)
        return vpn_list

    def inject_configs(self, vpn_config: dict):
        '''
        Inject global configs into the VPN data classes.

        Args:
            vpn_config (dict): Global config map to inject from the JSON
        '''
        # Check if Pritunl config exists
        if vpn_config.get(VpnType.PRITUNL.value):
            pritunl_config: dict = vpn_config[VpnType.PRITUNL.value]
            PritunlVpnData.cli_path = pritunl_config.get(
                'cli_path', PritunlVpnData.cli_path)
