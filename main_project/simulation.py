from custom_network import CustomNetwork
from create_custom_router import create_custom_router
from keyboard_interpreter import read_command
from bgp import start_connection_BGP

def start_simulation():
    network = CustomNetwork()
    network.add_router(create_custom_router('Test_router_1', "100.0.0.1", 8))
    network.add_router(create_custom_router('Test_router_2', "100.0.0.2", 8))
    network.add_link(0, 1)

    start_connection_BGP(network.routers[0], network.routers[1])

    sc = input("Do you want to keep the simulated network? (y/n)")
    if sc == "y":
        return network
    else:
        return CustomNetwork()
