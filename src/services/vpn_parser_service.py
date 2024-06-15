'''
Module for parsing VPN data from JSON
'''

from json import loads
from zope.interface import implementer

from vpn_model.abstract_vpn_model import AbstractVpnModel
from vpn_model.pritunl_vpn_model import PritunlVpnModel
from src.models.vpn_config.pritunl_vpn_config import PritunlVpnConfig
from src.enums.vpn_type import VpnTypeVisitor, VpnType


@implementer(VpnTypeVisitor)
class _VpnParsingVisitor:
    '''
    Visitor for parsing VPN data from JSON

    Attributes:
        json (dict): JSON data to parse
    '''

    def __init__(self, data_json: dict, config_json: dict):
        self.data_json: dict = data_json
        self.config_json: dict = config_json

    def visit_none(self) -> AbstractVpnModel:
        '''Visit VPN type not specified'''
        raise ValueError('Invalid VPN type')

    def visit_pritunl(self) -> AbstractVpnModel:
        '''Visit Pritunl VPN type'''
        config: PritunlVpnConfig = PritunlVpnConfig.from_json(self.config_json)
        return PritunlVpnModel.from_json_with_config(self.data_json, config)

    def visit_wireguard(self) -> AbstractVpnModel:
        '''Visit Wireguard VPN type'''
        raise NotImplementedError

    def visit_open_vpn(self) -> AbstractVpnModel:
        '''Visit OpenVPN VPN type'''
        raise NotImplementedError


class VpnDataParserService:
    '''
    Service for parsing VPN data from JSON

    Attributes:
        vpn_data (str): VPN data to parse
    '''

    _vpn_list_key: str = 'vpn_list'
    _config_key: str = 'config'

    def parse_vpn_data(self, vpn_data: str) -> list[AbstractVpnModel]:
        '''
        Parse VPN data from JSON.

        Also injects any global configs into the VPN data classes.

        Args:
            vpn_data (str): VPN data to parse

        Returns:
            list[AbstractVpnData]: List of VPN data objects
        '''
        vpn_data_dict: dict = loads(vpn_data)
        vpn_config_json: dict = vpn_data_dict.get(VpnDataParserService._config_key, {})
        vpn_list: list[AbstractVpnModel] = []
        for vpn_json in vpn_data_dict[VpnDataParserService._vpn_list_key]:
            vpn: _VpnParsingVisitor = self.generate_vpn_from_config_and_data(
                vpn_config_json,
                vpn_json
            )
            vpn_list.append(vpn)
        return vpn_list

    def generate_vpn_from_config_and_data(self, vpn_config_json, vpn_json) -> AbstractVpnModel:
        '''
        Generate a VPN data object from a config and data JSON.
        
        Args:
            vpn_config_json (dict): JSON of the VPN config
            vpn_json (dict): JSON of the VPN data
            
        Returns:
            AbstractVpnData: VPN data object
        '''
        vpn_type: VpnType = VpnType(vpn_json[AbstractVpnModel.vpn_type_key])
        parsing_visitor: _VpnParsingVisitor = _VpnParsingVisitor(vpn_json, vpn_config_json)
        return vpn_type.visit(parsing_visitor)
