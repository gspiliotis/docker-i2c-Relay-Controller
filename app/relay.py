from relayType import RelayType
import os
import json
import yaml #needs python3-yaml

#####################################
#             Relay                 #
#####################################
class Relay:

    CONFIG_IS_MASTER = 1
    HW_IS_MASTER = 2

    __buses = {}

    def __init__(self, type, bus, board_address, relay_number,
                 id = None, #Ignored - re-calculated bellow
                 typeName = None, #Ignored - re-calculated bellow
                 name = None,
                 status = False,
                 description="",
                 notes="",
                 sync=None,
                 inverted=False):
        self.__cache = {}
        if (name == None):
            name = "Relay "+str(data_address)
        if (sync == None):
            if (os.getenv('I2C_PERSISTENCE', True)):
                sync = Relay.CONFIG_IS_MASTER
            else:
                sync = Relay.HW_IS_MASTER
        self.__cache['type'] = type
        self.__cache['bus'] = bus
        self.__cache['board_address'] = board_address
        self.__cache['relay_number'] = relay_number
        self.__cache['name'] = name
        self.__cache['status'] = status
        self.__cache['description'] = description
        self.__cache['notes'] = notes
        self.__cache['inverted'] = inverted

        self.__cache['id'] = ( ( bus * 256 ) + board_address ) * 256 + relay_number

        self.__type = RelayType.get_by_id(type)(bus, board_address, relay_number)
        self.__cache['typeName'] = self.__type.get_name()

        if (sync == Relay.CONFIG_IS_MASTER):
            self.set_status(self.__cache['status'])
        elif (sync == Relay.HW_IS_MASTER):
            self.set_status(self.get_status_HW())
        else:
            raise ValueError("Invalid value for sync", sync)

    def get_status_HW(self):
        # Get Status from HW
        status = self.__type.get()
        print('Got HW Status for',self.__cache['name'], '->', status)
        if self.__cache['inverted']:
            status = not status
        return status

    def get_status(self):
        return self.__cache['status']

    def get_id(self):
        return self.__cache['id']

    def set_status(self, status):
        print('Setting relay status', self.__cache['name'], '->', status)

        if (self.get_status_HW() == status):
            print('Unchanged status for', self.__cache['name'], '- keeping', status)
            return False

        if self.__cache['inverted']:
            statusHW = not status
        else:
            statusHW = status
        self.__type.set(statusHW)
        print('Set HW Status for',self.__cache['name'], '->', statusHW)
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

    def get_inverted(self):
        return self.__cache['inverted']

    def set_inverted(self, inverted):
        if (inverted == self.get_inverted()):
            return False

        self.__cache['inverted'] = inverted
        #Set status will addapt HW status to new inverted status
        self.set_status(self.get_status())

    def get_description(self):
        return self.__cache['description']

    def set_description(self, description):
        if (description == self.get_description()):
            return False

        self.__cache['description'] = description
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
