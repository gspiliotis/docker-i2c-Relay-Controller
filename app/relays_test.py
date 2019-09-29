from relays import Relays

#####################################
#              test                 #
#####################################

def test():
    print()
    print("#################################")
    print("TEST: get_relay_byIndex")
    relay = Relays.get_relay_byIndex(0)

    print()
    print("#################################")
    print("TEST: Relay status")
    relay.get_status_HW()

    print()
    print("#################################")
    print("TEST: Relay ON")
    relay.on()

    print()
    print("#################################")
    print("TEST: Relay OFF")
    relay.off()

    print()
    print("#################################")
    print("TEST: Relay TOGGLE")
    relay.toggle()

    print()
    print("#################################")
    print("TEST: Relay all ON")
    Relays.on()

    print()
    print("#################################")
    print("TEST: Relay all OFF")
    Relays.off()

    print()
    print("#################################")
    print("TEST: Relay all TOGGLE")
    Relays.toggle()

    print()
    print("#################################")
    print("TEST: Check invalid index")
    try:
        Relays.get_relay_byIndex(200)
        raise ValueError("Invalid index not detected")
    except ValueError:
        pass #Expected



if __name__ == "__main__":
    test()
