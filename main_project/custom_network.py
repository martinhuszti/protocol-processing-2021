from typing import List
from bcolors import bcolors
from custom_packet import CustomPacket
from custom_router import CustomRouter
from custom_tcp_message import ETCP_MSG_TYPE, CustomTcpMessage
import re  # to check input syntax


class CustomNetwork:
    def __init__(self):
        self.routers: List[CustomRouter] = []
        self.links = []

    def add_router(self, new_router):
        if self.unique_IP(new_router):
            self.routers.append(new_router)
            print(bcolors.OKGREEN +
                  f'The router "{new_router.name}" - {new_router.ip_address}/{new_router.subnet} '
                  f'was added to the network!' + bcolors.ENDC)
        else:
            print(bcolors.FAIL + 'Error! There is already a router with the same IP in the network!' + bcolors.ENDC)

    def unique_IP(self, new_router):  # check if the IP of a new router has already been used
        for i in self.routers:
            if i.ip_address == new_router.ip_address:
                return False
        return True

    def get_network_size(self):
        return len(self.routers)

    # idx1 and idx2 are for testing purposes
    def add_link(self, idx1=None, idx2=None):
        print(bcolors.OKCYAN)
        self._printRouters()
        print(bcolors.ENDC)
        if not self.routers:
            return

        if idx1 != None and idx2 != None:
            first_router_idx = idx1
            second_router_idx = idx2
        else:
            first_router_idx = input('First router index:')
            second_router_idx = input('Second router index:')
            if second_router_idx.isdigit() and first_router_idx.isdigit():  # prevents crash if user types a letter
                if int(first_router_idx) >= self.get_network_size() or int(second_router_idx) >= self.get_network_size():
                    print(bcolors.FAIL + "Invalid indexes... returning" + bcolors.ENDC)
                    return
                elif first_router_idx == second_router_idx:
                    print(bcolors.WARNING + 'A router cannot create a link with itself!' + bcolors.ENDC)
                    return
            else:
                print(bcolors.FAIL + "Invalid indexes... returning" + bcolors.ENDC)
                return

        first_router = self.routers[int(first_router_idx)]
        second_router = self.routers[int(second_router_idx)]
        for pairs in self.links:
            if (pairs[0].ip_address == first_router.ip_address and pairs[1].ip_address == second_router.ip_address) or (pairs[0].ip_address == second_router.ip_address and pairs[1].ip_address == first_router.ip_address):
                ask = input('There already exists a link between these two routers, do you want to create a backup one? (y/n) ')
                if ask == 'y':
                    print(bcolors.WARNING + 'This content is under development!' + bcolors.ENDC)
                    # After having decided on a proper metric system we can add this :)
                    return
                elif ask == 'n':
                    print('Returning to main menu...')
                    return
                else:
                    print(bcolors.FAIL + "Invalid option!" + bcolors.ENDC)
                    return

        first_router.send_tcp_msg(
            _to=second_router, msg=CustomTcpMessage(type=ETCP_MSG_TYPE.SYN))
        self.links.append((first_router, second_router))
        print(bcolors.OKGREEN + 'Link created between the two router' + bcolors.ENDC)

    def remove_link(self):
        if not self.links:
            print('There are no more links to remove!')
            return

        print(bcolors.OKCYAN)
        self._printLinks()
        print(bcolors.ENDC)
        selected_idx = input('Link to remove: ')

        checkIdx = re.compile(r'\d(\d)?')  # allow only decimals
        if checkIdx.match(selected_idx):  # if the user inserted numbers
            selected_idx = int(selected_idx)  # we convert the string to int

            if selected_idx >= len(self.links):
                print(bcolors.FAIL + 'Wrong index!' + bcolors.ENDC)
                return
            else:
                selected_link = self.links[int(selected_idx)]
                router1: CustomRouter = selected_link[0]
                router2: CustomRouter = selected_link[1]
                router1.send_tcp_msg(
                    _to=router2, msg=CustomTcpMessage(type=ETCP_MSG_TYPE.FIN))
                self.links.pop(int(selected_idx))
                print(bcolors.OKGREEN + 'Link successfully removed!' + bcolors.ENDC)
        else:
            print(bcolors.FAIL + 'Insert only numbers!' + bcolors.ENDC)
            return

    def remove_router(self):
        if not self.routers:
            print('There are no more routers to remove!')
            return
        print(bcolors.OKCYAN)
        self._printRouters()
        print(bcolors.ENDC)
        # TODO: when removing a router, delete its links to other routers and the rows in the routing table
        sr = input('Select which router you want to remove (press a letter to exit): ')
        if sr.isdigit() and int(sr) >= 0 and int(sr) <= len(self.routers) - 1:
            self.routers.pop(int(sr))
            print(bcolors.OKGREEN + "The router was successfully removed!" + bcolors.ENDC)
        else:
            print(bcolors.FAIL + "The given index is not correct!" + bcolors.ENDC)

    def print_network(self):
        print(bcolors.OKCYAN + "Current network topology:\n")
        self._printRouters()
        self._printLinks()
        self._printTables()
        print(bcolors.ENDC)

    def _printRouters(self):
        print("Routers")
        if not self.routers:
            print("There are no routers, add one by selecting command 2!\n\n")
            return
        for i, r in enumerate(self.routers):
            print(f'\n{i}: {r.name} - {r.ip_address}')
            if not r.links:
                continue
            else:
                print(f'   Connected with:')
                for l in r.links:
                    print(f'     - {l.name}')
        print('\n')

    def _printLinks(self):
        print("Links")
        if not self.links:
            print("There are no links, create one by selecting command 4!\n\n")
            return
        for i, pairs in enumerate(self.links):
            print(f'{i}: {pairs[0].name} - {pairs[1].name}')
        print('\n')

    def _printTables(self):
        print("Routing Tables")
        if not self.routers:
            print("Without routers there can be none of these!\n")
            return
        for i, r in enumerate(self.routers):
            print(f'\n{r.name} - {r.ip_address}')
            r.print_tables()

    def send_packet(self):
        print("Sending packet from router to router")
        print(bcolors.OKCYAN)
        self._printRouters()
        print(bcolors.ENDC)

        inp = input("Index of the source router:")
        ip_to = input("Destination Ip address:")  # MAYBE WE CAN USE THE INDEX HERE TOO?
        if int(inp) >= 0 and int(inp) < len(self.routers):
            selected_router = self.routers[int(inp)]
            selected_router.send_packet(CustomPacket(selected_router.ip_address, ip_to))
        else:
            print(bcolors.FAIL + "The selected router index is not valid! Try again!" + bcolors.ENDC)

    def update_link_cost(self):
        #TODO using router.set_neighbor()
        pass
