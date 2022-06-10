from custom_network import CustomNetwork
from create_custom_router import create_custom_router
from keyboard_interpreter import read_command
from custom_tcp_message import ETCP_MSG_TYPE, CustomTcpMessage
from custom_packet import CustomPacket


def start_simulation():
    network = CustomNetwork()
    network.add_router(create_custom_router('AS_1', "100.0.1.0", 24))
    network.add_router(create_custom_router('AS_2', "100.0.2.0", 24))
    network.add_router(create_custom_router('AS_3', "100.0.3.0", 24))
    network.add_router(create_custom_router('AS_4', "100.0.4.0", 24))
    network.add_link(0, 1)
    network.add_link(0, 2)
    network.add_link(2, 3)

    ## first syn synack ack 
    
    # for routers in network.routers:
    #     for other_routers in network.routers:
    #         if routers != other_routers and network.routers.index(other_routers)>network.routers.index(routers):
    #             routers.send_tcp_msg(other_routers, CustomTcpMessage(ETCP_MSG_TYPE.SYN))
    #             other_routers.receive_tcp_msg(routers, CustomTcpMessage(ETCP_MSG_TYPE.SYN))
    #             routers.receive_tcp_msg(other_routers, CustomTcpMessage(ETCP_MSG_TYPE.SYN_ACK))
    #             other_routers.receive_tcp_msg(routers, CustomTcpMessage(ETCP_MSG_TYPE.ACK))
    
    #network.routers[0].send_packet(CustomPacket(network.routers[0].ip_address,network.routers[1].ip_address))
    network.routers[0].send_packet(CustomPacket(network.routers[0].ip_address,network.routers[3].ip_address))
    

    ###########################For dev purposes, NEEDS TO BE CHANGED###########################
    #answer = input("Do you want to keep the current network? (y/n)")
    answer = "y"
    ###########################################################################################
    if answer.lower() == "y":
        return network
    else:
        return CustomNetwork()
