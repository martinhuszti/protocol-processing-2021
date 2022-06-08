from custom_network import CustomNetwork
from create_custom_router import create_custom_router
from keyboard_interpreter import read_command

def start_simulation():
    network = CustomNetwork()
    network.add_router(create_custom_router('Test_router_1', "100.0.0.1", 8))
    network.add_router(create_custom_router('Test_router_2', "100.0.0.2", 8))
    network.add_link(0, 1)



    ###########################For dev purposes, NEEDS TO BE CHANGED###########################
    #answer = input("Do you want to keep the current network? (y/n)")
    answer = "y"
    ###########################################################################################
    if answer.lower() == "y":
        return network
    else:
        return CustomNetwork()
