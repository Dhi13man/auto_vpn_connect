class UserSwitches:
  def __init__(self, action: str, vpn_data_json_path: str, verbose: bool = False):
    self.action: str = action
    self.vpn_data_json_path: str = vpn_data_json_path
    self.verbose: bool = verbose