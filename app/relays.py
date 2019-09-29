import os
import os.path
import yaml #needs python3-yaml
import io
from relay import Relay

# Configuration file
CONFIG_FILE = os.getenv('I2C_CONFIG_FILE', "config.yaml")

# 12C Bus Address
I2C_BUS = 1 # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)

# The number of relay ports on the relay board.
NUM_RELAY_PORTS = 4

# Change the following value if your Relay board uses a different I2C address.
DEVICE_ADDRESS = 0x10  # 7 bit address (will be left shifted to add the read write bit)

#####################################
#             Relays                #
#####################################

class Relays:
    __relays = []

    @staticmethod
    def get_relays():
        return Relays.__relays

    @staticmethod
    def get_relays_len():
        return len(Relays.get_relays())

    @staticmethod
    def is_valid_relayIndex(index):
        return (index >= 0) & (index < Relays.get_relays_len())

    @staticmethod
    def get_relay_byIndex(index):
        if not Relays.is_valid_relayIndex(index):
            raise ValueError("Relay index outside range", index, "Min Value:", 0, "Max Value:", Relays.get_relays_len()-1)
        return Relays.get_relays()[index]

    @staticmethod
    def append(relay):
        Relays.get_relays().append(relay)

    @staticmethod
    def read_config():
        # Example
        #
        # relays:
        # - bus: 1
        #   data_address: 0
        #   description: ''
        #   device_address: 16
        #   name: Relay_0
        #   notes: ''
        if os.path.exists(CONFIG_FILE):
            # Read existing config
            print("Reading "+CONFIG_FILE)
            with open(CONFIG_FILE, 'r') as stream:
                config = yaml.safe_load(stream)
                relays_raw = config['relays']
                for relay_raw in relays_raw:
                    Relays.append(Relay(**relay_raw))
        else:
            # Generate default config
            print("Creating "+CONFIG_FILE)
            config = {}
            config['relays'] = []
            for relay in range(1,NUM_RELAY_PORTS+1):
                relay = Relay(
                    bus = I2C_BUS,
                    device_address = DEVICE_ADDRESS,
                    data_address = relay
                )
                Relays.append(relay)
                config['relays'].append(relay.to_dict())
            # Save initial config
            Relays.write_config()

    @staticmethod
    def write_config():
        config = {}
        config['relays'] = Relays.get_relays_raw()
        print("Writing configuration",CONFIG_FILE)
        # Write YAML file
        with io.open(CONFIG_FILE, 'w', encoding='utf8') as outfile:
            yaml.dump(config, outfile, default_flow_style=False, allow_unicode=True)

    @staticmethod
    def get_relays_raw():
        relays_raw = []
        for relay in Relays.get_relays():
            relays_raw.append(relay.to_dict())
        return relays_raw

    @staticmethod
    def set_status(status):
        for relay in Relays.get_relays():
            relay.set_status(status)

    @staticmethod
    def on():
        Relays.set_status(True)

    @staticmethod
    def off():
        Relays.set_status(False)

    @staticmethod
    def toggle():
        for relay in Relays.get_relays():
            relay.set_status(not relay.get_status())





# Init
Relays.read_config()
