from subprocess import CompletedProcess
import zope.interface

class VpnDataInterface(zope.interface.Interface):  
    def connect(self) -> CompletedProcess:
        pass

    def disconnect(self) -> CompletedProcess:
        pass