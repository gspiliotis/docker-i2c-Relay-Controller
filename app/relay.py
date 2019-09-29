import smbus2 as smbus #needs python3-smbus
import os

#####################################
#             Relay                 #
#####################################
class Relay:

    CONFIG_IS_MASTER = 1
    HW_IS_MASTER = 2

    __buses = {}

    def __init__(self, bus, data_address, device_address,
                 name = None,
                 status = False,
                 description="",
                 notes="",
                 sync=None):
        self.__cache = {}
        if (name == None):
            name = "Relay "+str(data_address)
        if (sync == None):
            if (os.getenv('I2C_PERSISTENCE', True)):
                sync = Relay.CONFIG_IS_MASTER
            else:
                sync = Relay.HW_IS_MASTER
        self.__cache['bus'] = bus
        self.__cache['data_address'] = data_address
        self.__cache['device_address'] = device_address
        self.__cache['name'] = name
        self.__cache['status'] = status
        self.__cache['description'] = description
        self.__cache['notes'] = notes

        if (sync == Relay.CONFIG_IS_MASTER):
            self.set_status(self.__cache['status'])
        elif (sync == Relay.CONFIG_IS_MASTER):
            self.get_status()
        else:
            raise ValueError("Invalid value for sync", sync)

    @staticmethod
    def __open_bus(bus):
        return Relay.__buses.setdefault(bus, smbus.SMBus(bus))

    def get_status_HW(self):
        # Get Status from HW
        bus = Relay.__open_bus(self.__cache['bus'])
        status = bus.read_byte_data(self.__cache['device_address'], self.__cache['data_address']) > 0
        print('Status for',self.__cache['name'], '->', status)
        return status

    def get_status(self):
        return self.__cache['status']

    def set_status(self, status):
        print('Setting relay status', self.__cache['name'], '->', status)

        if (self.get_status_HW() == status):
            print('Unchanged - ignoring', self.__cache['name'], status)
            return False

        bus = Relay.__open_bus(self.__cache['bus'])
        bus.write_byte_data(self.__cache['device_address'], self.__cache['data_address'], status)
        self.__cache['status'] = status
        from relays import Relays
        Relays.write_config()

    def on(self):
        self.set_status(True)

    def off(self):
        self.set_status(False)

    def toggle(self):
        self.set_status(not self.get_status())

    def get_name(self):
        return self.__cache['name']

    def set_name(self, name):
        if (name == self.get_name()):
            return False

        self.__cache['name'] = name
        from relays import Relays
        Relays.write_config()

    def get_notes(self):
        return self.__cache['notes']

    def set_notes(self, name):
        if (name == self.get_notes()):
            return False

        self.__cache['notes'] = name
        from relays import Relays
        Relays.write_config()

    def to_dict(self):
        return self.__cache.copy()

    def to_JSON(self):
        return json.dumps(self.__cache)

    def to_JAML(self):
        yaml.dump(self.__cache, default_flow_style=False, allow_unicode=True)
