from custom_network import CustomNetwork
from create_custom_router import create_custom_router
from keyboard_interpreter import read_command
from custom_tcp_message import ETCP_MSG_TYPE, CustomTcpMessage


def start_simulation():
    network = CustomNetwork()
    network.add_router(create_custom_router('Test_router_1', "100.0.0.1", 8))
    network.add_router(create_custom_router('Test_router_2', "100.0.0.2", 8))
    network.add_router(create_custom_router('Test_router_3', "100.0.0.3", 8))
    network.add_router(create_custom_router('Test_router_4', "100.0.0.4", 8))
    network.add_link(0, 1)
    network.add_link(0, 2)
    network.add_link(2, 3)

    ## first syn synack ack 
    
    for routers in network.routers:
        for other_routers in network.routers:
            if routers != other_routers and network.routers.index(other_routers)>network.routers.index(routers):
                routers.send_tcp_msg(other_routers, CustomTcpMessage(ETCP_MSG_TYPE.SYN))
                other_routers.receive_tcp_msg(routers, CustomTcpMessage(ETCP_MSG_TYPE.SYN))
                other_routers.send_tcp_msg(routers, CustomTcpMessage(ETCP_MSG_TYPE.SYN_ACK))
                routers.receive_tcp_msg(other_routers, CustomTcpMessage(ETCP_MSG_TYPE.SYN_ACK))
                routers.send_tcp_msg(other_routers, CustomTcpMessage(ETCP_MSG_TYPE.ACK))
                other_routers.receive_tcp_msg(routers, CustomTcpMessage(ETCP_MSG_TYPE.ACK))


    userContinue = True
    while(userContinue):
        ##Magic for routers here

        for routers in network.routers:
            for other_routers in network.routers:
                if routers != other_routers:
                    routers.send_packet(other_routers)

        answer = input("Do you want to stop the simulation? (y/n)")
        if answer.lower() == "y":
            break
        pass
    

    #print("SENDING PACKET FROM Test_router_1 to Test_router_2")

    ###########################For dev purposes, NEEDS TO BE CHANGED###########################
    #answer = input("Do you want to keep the current network? (y/n)")
    answer = "y"
    ###########################################################################################
    if answer.lower() == "y":
        return network
    else:
        return CustomNetwork()
