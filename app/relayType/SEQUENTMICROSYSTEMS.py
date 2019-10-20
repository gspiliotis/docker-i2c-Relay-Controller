from .base import *

_ID = RelayType.SEQUENTMICROSYSTEMS
_NAME = 'Sequent-8'
_DESCRIPTION = '8-RELAY Stackable Card for Raspberry Pi'
_URL = 'https://www.sequentmicrosystems.com/8relays.html'

class __myRelayType(RelayTypeI2C):

    RELAY8_INPORT_REG_ADD = 0x00
    RELAY8_OUTPORT_REG_ADD = 0x01
    RELAY8_POLINV_REG_ADD = 0x02
    RELAY8_CFG_REG_ADD = 0x03

    def __init__(self, bus_address, board_address, relay_number):
        if (relay_number < 1 or relay_number > 8):
            raise ValueError("relay_number out of range (1-4) " + relay_number)
        super().__init__(bus_address, board_address, relay_number)
        if self._read_byte(self.RELAY8_CFG_REG_ADD):
            self._write_byte(self.RELAY8_CFG_REG_ADD, 0)

    def get_id(self):
        return _ID

    def __get_mask(self):
        return (1 << (self._relay_number - 1))

    def get(self):
        val = self._read_byte(self.RELAY8_INPORT_REG_ADD)
        return (val & (self.__get_mask())) > 0

    def set(self, value):
        oldVal = self._read_byte(self.RELAY8_INPORT_REG_ADD)
        if value:
            val = oldVal | (self.__get_mask())
        else:
            val = oldVal & (~self.__get_mask())
        self._write_byte(self.RELAY8_OUTPORT_REG_ADD, val)

RelayType._add_type({'id': _ID,
                    'name': _NAME,
                    'description': _DESCRIPTION,
                    'url': _URL
                    },
                    __myRelayType)
