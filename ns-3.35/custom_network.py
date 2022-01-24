from typing import List
from bcolors import bcolors
from custom_packet import CustomPacket
from custom_router import CustomRouter
from custom_tcp_message import ETCP_MSG_TYPE, CustomTcpMessage
from user_interface import print_line


class CustomNetwork:
    def __init__(self):
        self.routers: List[CustomRouter] = []
        self.links = []

    def add_router(self, new_router):
        self.routers.append(new_router)

    def get_network_size(self):
        return len(self.routers)

# idx1 and idx2 are for testing purposes
    def add_link(self, idx1=None, idx2=None):
        self._printRouters()
        if(idx1 != None and idx2 != None):
            first_router_idx = idx1
            second_router_idx = idx2
        else:
            first_router_idx = input('First router index:')
            second_router_idx = input('Second router index:')

        if(int(first_router_idx) >= self.get_network_size() or int(second_router_idx) >= self.get_network_size()):
            print("Invalid indexes... returning")
            pass
        first_router = self.routers[int(first_router_idx)]
        second_router = self.routers[int(second_router_idx)]
        first_router.send_tcp_msg(
            _to=second_router, msg=CustomTcpMessage(type=ETCP_MSG_TYPE.SYN))
        self.links.append((first_router, second_router))
        print('Link created between the two router')

    def remove_link(self):
        self._printLinks()
        selected_idx = input('Link to remove: ')
        if int(selected_idx) >= len(self.links):
            print('Wrong index!')
            return
        selected_link = self.links[int(selected_idx)]
        router1: CustomRouter = selected_link[0]
        router2: CustomRouter = selected_link[1]
        router1.send_tcp_msg(
            _to=router2, msg=CustomTcpMessage(type=ETCP_MSG_TYPE.FIN))
        self.links.pop(int(selected_idx))

    def remove_router(self):
        self.print_network()
        sr = input('Which router you want to remove: ')
        if(sr.isdigit() and int(sr) >= 0 and int(sr) <= len(self.routers)-1):
            self.routers.pop(int(sr))
            print(bcolors.OKGREEN + "The router successfully removed!" + bcolors.ENDC)
        else:
            print(bcolors.FAIL + "The given index is not correct!" + bcolors.ENDC)

    def print_network(self):
        print(bcolors.OKCYAN+"Current network topology:")
        self._printRouters()
        self._printLinks()
        print_line()
        print(bcolors.ENDC)

    def _printRouters(self):
        print("\nRouters")
        for i, r in enumerate(self.routers):
            print(f'{i}: {r.name} - {r.ip_address}')
            print(f'    Connected with:')
            for l in r.links:
                print(f'      - {l.name}')
            print('\n')


    def _printLinks(self):
        print("\nLinks")
        for i, pairs in enumerate(self.links):
            print(f'{i}: {pairs[0].name} - {pairs[1].name}')

    def send_packet(self):
        print("Sending packet from router to router")
        self.print_network()
        inp = input("Index of the source router:")
        ip_to = input("Destination Ip address:")
        if int(inp) >= 0 and int(inp) < len(self.routers):
            selected_router = self.routers[int(inp)]
            selected_router.send_packet(CustomPacket(selected_router.ip_address,ip_to))
        else:
            print("The selected router index is not valid! Try again!")
            
