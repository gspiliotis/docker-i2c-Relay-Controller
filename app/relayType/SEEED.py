from .base import *

_ID = RelayType.SEEED
_NAME = 'Seeed-4'
_DESCRIPTION = 'Seeed Raspberry Pi Relay Board v1.0'
_URL = 'https://www.seeedstudio.com/Raspberry-Pi-Relay-Board-v1.0-p-2409.html'

class __myRelayType(RelayTypeI2C):

    DEVICE_REG_MODE1 = 0x06

    def __init__(self, bus_address, board_address, relay_number):
        if (relay_number < 1 or relay_number > 4):
            raise ValueError("relay_number out of range (1-4) " + relay_number)
        super().__init__(bus_address, board_address, relay_number)

    def get_id(self):
        return _ID

    def __get_mask(self):
        return (1 << (self._relay_number - 1))

    def get(self):
        val = self._read_byte(self.DEVICE_REG_MODE1)
        return (val & (self.__get_mask())) > 0

    def set(self, value):
        oldVal = self._read_byte(self.DEVICE_REG_MODE1)
        if value:
            val = oldVal | (self.__get_mask())
        else:
            val = oldVal & (~self.__get_mask())
        self._write_byte(self.DEVICE_REG_MODE1, val)

RelayType._add_type({'id': _ID,
                    'name': _NAME,
                    'description': _DESCRIPTION,
                    'url': _URL
                    },
                    __myRelayType)
