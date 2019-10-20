class RelayType:
    R52PI = 1
    SEQUENTMICROSYSTEMS = 2
    SEEED = 3

    __defs = {}
    __imps = {}
    @staticmethod
    def _add_type(definition, implementation):
        if definition['id'] in RelayType.__defs:
            raise ValueError("Duplicated registration for relay type with ID " + str(definition['id']))
        RelayType.__defs[definition['id']] = definition;
        RelayType.__imps[definition['id']] = implementation;

    @staticmethod
    def get_types():
        print(str(list(RelayType.__defs.values())))
        return list(RelayType.__defs.values())

    @staticmethod
    def get_by_id(id):
        if id not in RelayType.__imps:
            raise ValueError("Not a valid Relay Type ID" + str(id))

        return RelayType.__imps[id]

    def get_name(self):
        return RelayType.__defs[self.get_id()]['name']


###########################################
#                                         #
#               RelayTypeI2C              #
#                                         #
###########################################
import smbus2 as smbus #needs python3-smbus

class RelayTypeI2C(RelayType):
    __buses = {}
    @staticmethod
    def __open_bus(bus):
        return RelayTypeI2C.__buses.setdefault(bus, smbus.SMBus(bus))

    def __init__(self, bus_address, board_address, relay_number):
        self.__bus = RelayTypeI2C.__open_bus(bus_address)
        self.__board_address = board_address
        self._relay_number = relay_number

    def _read_byte(self, data_address):
        return self.__bus.read_byte_data(self.__board_address, data_address)

    def _write_byte(self, data_address, value):
        self.__bus.write_byte_data(self.__board_address, data_address, value)
