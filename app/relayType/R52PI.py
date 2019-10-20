from .base import *

_ID = RelayType.R52PI
_NAME = '52pi-4'
_DESCRIPTION = '52pi DockerPi 4 Channel Relay SKU: EP-0099'
_URL = 'https://wiki.52pi.com/index.php/DockerPi_4_Channel_Relay_SKU:_EP-0099'

class __myRelayType(RelayTypeI2C):

    def __init__(self, bus_address, board_address, relay_number):
        if (relay_number < 1 or relay_number > 4):
            raise ValueError("relay_number out of range (1-4) " + relay_number)
        super().__init__(bus_address, board_address, relay_number)

    def get_id(self):
        return _ID

    def get(self):
        return self._read_byte(self._relay_number) > 0

    def set(self, value):
        self._write_byte(self._relay_number, value)

RelayType._add_type({'id': _ID,
                    'name': _NAME,
                    'description': _DESCRIPTION,
                    'url': _URL
                    },
                    __myRelayType)
