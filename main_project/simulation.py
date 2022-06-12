from custom_network import CustomNetwork
from create_custom_router import create_custom_router
from keyboard_interpreter import read_command
from custom_tcp_message import ETCP_MSG_TYPE, CustomTcpMessage
from custom_packet import CustomPacket


def start_simulation():
    network = CustomNetwork()
    print("Welcome to the simulation!\n\n")

    print("#####################################################\n")
    print("Creation of three basic AS\n")
    print("#####################################################\n")
    network.add_router(create_custom_router('AS_1', "100.0.1.0", 24))
    network.add_router(create_custom_router('AS_2', "100.0.2.0", 24))
    network.add_router(create_custom_router('AS_3', "100.0.3.0", 24))
    network.add_router(create_custom_router('AS_4', "100.0.4.0", 24))

    print("#####################################################\n")
    print("Creation of three links\n")
    print("#####################################################\n")


    network.add_link(0, 1)
    network.add_link(0, 2)
    network.add_link(2, 3)


    print("#####################################################\n")
    print("Trying to send a packet from AS_1 to AS_2. Direct link available\n")
    print("#####################################################\n")

    network.routers[0].send_packet(CustomPacket(network.routers[0].ip_address,network.routers[1].ip_address))
    
    print("#####################################################\n")
    print("Trying to send a packet from AS_1 to AS_4. No direct link available\n")
    print("#####################################################\n")  

    network.routers[0].send_packet(CustomPacket(network.routers[0].ip_address,network.routers[3].ip_address))
    

    ###########################For dev purposes, NEEDS TO BE CHANGED###########################
    answer = input("Do you want to keep the current network? (y/n)")

    ###########################################################################################
    if answer.lower() == "y":
        return network
    else:
        return CustomNetwork()
