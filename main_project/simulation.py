from custom_network import CustomNetwork
from create_custom_router import create_custom_router
from keyboard_interpreter import read_command
from custom_tcp_message import ETCP_MSG_TYPE, CustomTcpMessage
from custom_packet import CustomPacket
import time


def start_simulation():
    network = CustomNetwork()
    print("Welcome to the simulation!\n\n")

    print("\n#####################################################\n")
    print("Creation of three basic AS\n")
    print("#####################################################\n")
    network.add_router(create_custom_router('AS_1', "100.0.1.0", 24))
    network.add_router(create_custom_router('AS_2', "100.0.2.0", 24))
    network.add_router(create_custom_router('AS_3', "100.0.3.0", 24))
    network.add_router(create_custom_router('AS_4', "100.0.4.0", 24))
    time.sleep(2)

    
    print("\n#####################################################\n")
    print("Creation of three links\n")
    print("#####################################################\n")


    network.add_link(0, 1)
    network.add_link(0, 2)
    network.add_link(2, 3)
    time.sleep(5)

    print("\n#####################################################\n")
    print("Stopping keepalive for clarity in terminal\n")
    print("#####################################################\n")

    time.sleep(2)
    print("\n#####################################################\n")
    print("Trying to send a packet from AS_1 to AS_2. Direct link available\n")
    print("#####################################################\n")
    
    network.routers[0].send_packet(CustomPacket(network.routers[0].ip_address,network.routers[1].ip_address))
    time.sleep(2)
    print("\n#####################################################\n")
    print("Trying to send a packet from AS_1 to AS_4. No direct link available\n")
    print("#####################################################\n")  

    network.routers[0].send_packet(CustomPacket(network.routers[0].ip_address,network.routers[3].ip_address))
    
    time.sleep(2)
    print("\n#####################################################\n")
    print("Printing Current routing tables\n")
    print("#####################################################\n")  
    network.print_network()
    
    time.sleep(5)

    print("\n#####################################################\n")
    print("Removing link between AS_1 and AS_2\n")
    print("#####################################################\n")  
    network.remove_link("0")
    time.sleep(2)

    print("\n#####################################################\n")
    print("Printing Current routing tables\n")
    print("#####################################################\n")  
    network.print_network()

    time.sleep(2)

    print("\n#####################################################\n")
    print("Sending packet rerouted to AS_3 from AS_1\n")
    print("#####################################################\n")  
    network.routers[0].send_packet(CustomPacket(network.routers[0].ip_address,network.routers[2].ip_address))

    time.sleep(2)

    print("\n#####################################################\n")
    print("Sending packet rerouted to AS_2 from AS_1. No link are available in AS_2\n")
    print("#####################################################\n")  
    network.routers[0].send_packet(CustomPacket(network.routers[0].ip_address,network.routers[1].ip_address))

    time.sleep(2)

    print("\n#####################################################\n")
    print("Restoring link between AS_1 and AS_2\n")
    print("#####################################################\n")  
    network.add_link(0, 1)

    time.sleep(2)

    print("\n#####################################################\n")
    print("Removing AS_2\n")
    print("#####################################################\n")  
    network.remove_router("1")

    time.sleep(2)

    print("\n#####################################################\n")
    print("Printing Current routing tables\n")
    print("#####################################################\n")  
    network.print_network()

    time.sleep(2)

    print("\n#####################################################\n")
    print("Changing link cost between AS_1 and AS_3 to 1\n")
    print("#####################################################\n")  
    network.update_link_cost("0", "1")

    time.sleep(2)

    print("\n#####################################################\n")
    print("Printing Current routing tables\n")
    print("#####################################################\n")  
    network.print_network()

    time.sleep(2)

    print("\n#####################################################\n")
    print("This is the end of our simulation\n")
    answer = input("Do you want to keep the current network? (y/n)")
    ###########################For dev purposes, NEEDS TO BE CHANGED###########################

    ###########################################################################################
    if answer.lower() == "y":
        print("\n#####################################################\n")
        print("Returning to main menu keeping the current network\n")
        print("#####################################################\n") 
        return network
    else:
        print("\n#####################################################\n")
        print("Returning to main menu with a new network\n")
        print("#####################################################\n")
        return CustomNetwork()
