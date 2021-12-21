from typing import List
from bcolors import bcolors
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

#idx1 and 2 are for testing purposes 
    def add_link(self,idx1,idx2):
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
            _to = second_router, msg= CustomTcpMessage(type=ETCP_MSG_TYPE.SYN))
        self.links.append((first_router,second_router))
        print('Link created between the two router')



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
        for i, r in enumerate(self.routers):
            print(f'{i}: {r.name}') 
        print("\nLinks")
        for pair1,pair2 in self.links:
            print(f'{i}: {pair1.name} - {pair2.name}')
        print_line()
        print(bcolors.ENDC)
