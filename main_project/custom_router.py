from queue import Empty
import time
from custom_packet import CustomPacket
from custom_tcp_message import ETCP_MSG_TYPE, CustomTcpMessage
from bcolors import bcolors
import ipaddress
import threading
import random
from prettytable import PrettyTable
import string

from custom_bgp_message import BGP_MSG_TYPE, KeepAliveBgpMessage, OpenBgpMessage, UpdateBgpMessage  # to print routing tables in a cute way

# TODO: add missing input params when sending tcp messages

class CustomRouter:
 
    def __init__(self, AS_id='No AS_id given', ip_address="255.255.255.255", subnet=32):
        self.AS_id = AS_id
        self.routing_table = []  # List of dictionaries with destination_network, subnet_mask, AS_PATH, next_hop, cost, reference
        self.neighbor_table = [] # List of dictionaries with AS_id, ip_address, cost, reference
        self.bgp_table = [] # List of dictionaries with destination_network, subnet_mask, AS_PATH, next_hop, cost
        self.links = []  # the link and the routing table index are matching
        self.ip_address = ip_address
        self.subnet = subnet
        self.keep_alive_thread = None
        self.thread_life = 3

    def send_keep_alive(self):
        while self.thread_life>0:
            self.thread_life -= 1
            print("sending keep alive")
            time.sleep(2)
        return

    def set_network(self, network):
        self.network = network

    def print(self):
        print(self.AS_id)

    ############################

    def print_tables(self): 
        t = PrettyTable()
        if not self.routing_table:
            print('This table is currently empty!')
            return
        for c in ['Destination', 'Netmask', 'Gateway' ,'Cost']:
            t.add_column(c, [])
        for dct in self.routing_table:
            t.add_row([dct.get(c, "") for c in ['destination_network', 'subnet_mask', "next_hop" ,'cost']])
        print(t)

    ########################

    def send_tcp_msg(self, _to, msg: CustomTcpMessage):
        self.current_seq_num = random.random()
        # If syn, generate seq number otherwise it is containing already
        if msg.type == ETCP_MSG_TYPE.SYN or msg.type == ETCP_MSG_TYPE.FIN:
            msg.seq_num = self.current_seq_num
            print(f'{self.ip_address}: sending {msg.type.name} message to {_to.ip_address}')
        # Simulate that the message is arrived to the router
        _to.receive_tcp_msg(self, msg)

    def receive_tcp_msg(self, _from, tcp_message: CustomTcpMessage):
        print(f'{self.ip_address}: TCP message arrived: {tcp_message.type.name}')
        _type = tcp_message.type

        # 1. Start with SYN
        if _type == ETCP_MSG_TYPE.SYN:
            print(f'{self.ip_address}: sending back syn-ack with ')
            self.send_tcp_msg(_to=_from, msg=CustomTcpMessage(
                type=ETCP_MSG_TYPE.SYN_ACK, seq_num=tcp_message.seq_num, ip_address=self.ip_address,
                subnet=self.subnet))

        # 2. Answer with SYN-ACK and send the ip range
        if _type == ETCP_MSG_TYPE.SYN_ACK:
            if tcp_message.seq_num == self.current_seq_num:
                print(f"{self.ip_address}: The sequence number is correct, initializing connection")
                self.send_tcp_msg(_from, CustomTcpMessage(type=ETCP_MSG_TYPE.ACK))
                self.current_seq_num = 0
                self.send_tcp_msg(_from, CustomTcpMessage(ETCP_MSG_TYPE.NONE, content=OpenBgpMessage(-1, 60, self.ip_address)))

                
        if _type == ETCP_MSG_TYPE.ACK:
            if tcp_message.is_fin_ack_response:
                print(f"{self.ip_address}: ACK arrived to the FIN_ACK message")
            else:
                print(f"{self.ip_address}: Initializing connection")
                self.send_tcp_msg(_from, CustomTcpMessage(ETCP_MSG_TYPE.NONE, content=OpenBgpMessage(-1, 60, self.ip_address)))

        if _type == ETCP_MSG_TYPE.FIN_ACK:
            print(
                f"{self.ip_address}: Sending back ACK with is_fin_ack_response true flag")
            self.send_tcp_msg(
                _from,
                CustomTcpMessage(type=ETCP_MSG_TYPE.ACK,
                                 is_fin_ack_response=True)
            )

        if _type == ETCP_MSG_TYPE.FIN:
            # Only if ACK arrives remove from the list
            print(f"{self.ip_address}: Sending back FIN_ACK")
            self.send_tcp_msg(_from, CustomTcpMessage(
                type=ETCP_MSG_TYPE.FIN_ACK))

        if _type == ETCP_MSG_TYPE.NONE:
            #assuming its a BGP MESSAGE
            bgp_message = tcp_message.content
            _bgptype = bgp_message.type
            if _bgptype == BGP_MSG_TYPE.OPEN:
                self.send_tcp_msg(_from, CustomTcpMessage(
                    ETCP_MSG_TYPE.NONE, tcp_message.seq_num+1, content=KeepAliveBgpMessage(is_open_response=True)))
                if not self.keep_alive_thread:
                    self.keep_alive_thread = threading.Thread(
                        target=self.send_keep_alive)
                    self.keep_alive_thread.start()
   
            if _bgptype == BGP_MSG_TYPE.UPDATE:
                print(f'{self.ip_address}: BGP message arrived: UPDATE')
                if bgp_message.WithdrawnRoutes:
                    for route in bgp_message.WithdrawnRoutes:
                        self.remove_route(route)
                bgp_message.ASPath.append(self.AS_id)
                for nlri in bgp_message.NLRI:
                    if nlri[0] != self.ip_address:
                        self.update_routing_table(nlri[0], nlri[1], bgp_message.ASPath, _from.ip_address, nlri[2])
                for entry in self.neighbor_table:
                    if entry['AS_id'] not in bgp_message.ASPath:
                        self.send_tcp_msg(entry['reference'], CustomTcpMessage(ETCP_MSG_TYPE.NONE, content=UpdateBgpMessage(bgp_message.WithdrawnRoutes, bgp_message.ASPath, bgp_message.NextHop, bgp_message.NLRI)))

    def send_packet(self, packet: CustomPacket):
        # If the router initializing the sending
        if packet.ip_from == self.ip_address:
            print(f"{self.ip_address}: I'm sending a packet to: {packet.ip_to}")
        # If the router is not the initialization router then it can be the destination router or in-between router
        else:
            print(f"{self.ip_address}: A new packet arrived.")
        # Check if packet arrived to the destination
        if packet.ip_to == self.ip_address or ipaddress.ip_address(packet.ip_to) in ipaddress.ip_network(self.ip_address+"/"+str(self.subnet)):
            print(
                f"{self.ip_address}:" + bcolors.OKGREEN +
                f" I am the destination of the packet! It's arrived to the destination! {self.ip_address}"
                + bcolors.ENDC)
            return
        # Check where to forward the packet
        found_router = self.select_next_hop(packet.ip_to)
        if found_router:
            found_router['reference'].send_packet(packet)
        else:
            print(f'{bcolors.FAIL}Error: no possible route found{bcolors.ENDC}')

    # neighbor is the router that we need to set
    def set_neighbor(self, neighbor, cost):
        tmp = False
        for entry in self.neighbor_table:
            if entry['ip_address'] == neighbor.ip_address:
                entry['cost'] = cost #chosen randomly to assign different costs
                tmp = True
                break
        if not tmp: 
            print(f"{self.ip_address}-set_neighbor: New neighbor added to the neighbor_table")
            self.neighbor_table.append({'AS_id': neighbor.AS_id, 'ip_address': neighbor.ip_address, 'cost': cost, 'reference' : neighbor})

    def remove_neighbor(self, neighbor):
        for entry in self.neighbor_table:
            if entry['ip_address'] == neighbor.ip_address:
                self.neighbor_table.remove(entry)

    def select_next_hop(self, ip_address):
        for neighbor in self.neighbor_table:
            if ip_address == neighbor['ip_address']:
                print(f"{self.ip_address}-select_next-hop: router found in neighbouring table!")
                return neighbor
        for elem in self.routing_table:
            if ipaddress.ip_address(ip_address) in ipaddress.ip_network(f"{elem['destination_network']}/{elem['subnet_mask']}"):
                for neighbor in self.neighbor_table:
                    if elem['next_hop'] == neighbor['ip_address']:
                        return neighbor
        return None 

    def update_routing_table(self, network, subnet_mask, AS_path, next_hop, cost):

        tmp = False
        for neighbor in self.neighbor_table:
            if next_hop == neighbor['ip_address']:
                if ipaddress.ip_address(neighbor['ip_address']) not in ipaddress.ip_network(network+"/"+str(subnet_mask)): 
                    cost += neighbor['cost']
                tmp = True
                break
        if not tmp:
            print(f'{bcolors.FAIL}Error: unknwon next hop{bcolors.ENDC}')
        else:
            ###bgp_table###
            already_in_bgp_table = False
            pos = 0
            for elem in self.bgp_table:
                if network == elem['destination_network'] and subnet_mask == elem['subnet_mask'] and AS_path == elem['AS_path'] and next_hop == elem['next_hop']:
                    already_in_bgp_table = True
                    print("Already in BGP table")
                    break
                pos += 1
            if not already_in_bgp_table:
                self.bgp_table.append({'destination_network': network, 'subnet_mask': subnet_mask, 'AS_path': AS_path, 'next_hop': next_hop, 'cost': cost})
            else:
                self.routing_table[pos]['cost'] = cost


            ###routing_table###
            already_in_routing_table = False
            pos = 0
            for elem in self.routing_table:
                if network == elem['destination_network'] and subnet_mask == elem['subnet_mask']:
                    already_in_routing_table = True
                    print("Already in routing table")
                    break
                pos += 1
            if not already_in_routing_table:
                self.routing_table.append({'destination_network': network, 'subnet_mask': subnet_mask, 'AS_path': AS_path, 'next_hop': next_hop, 'cost': cost})
            else:
                if self.routing_table[pos]['cost'] > cost or (self.routing_table[pos]['cost'] == cost and len(self.routing_table[pos]['AS_path']) > len(AS_path)):
                    self.routing_table[pos]['cost'] = cost
                    self.routing_table[pos]['next_hop'] = next_hop
                    self.routing_table[pos]['AS_path'] = AS_path

    def remove_route(self, route):
        for entry in self.routing_table:
            if route.network == entry["destination_network"] and route.subnet == entry['subnet_mask'] and route.AS_path == entry["AS_path"]:
                self.routing_table.remove(entry)
        for entry in self.bgp_table:
            if route.network == entry["destination_network"] and route.subnet == entry['subnet_mask'] and route.AS_path == entry["AS_path"]:
                self.bgp_table.remove(entry)

        new_route = None
        for entry in self.bgp_table:
            if route.network == entry["destination_network"] and route.subnet == entry['subnet_mask']:
                if not new_route:
                    new_route = entry
                elif entry["cost"] < new_route["cost"]:
                    new_route = entry
        
        if new_route:
            self.routing_table.append(new_route)

    def routers_handshake(self, router2):
        self.send_tcp_msg(router2, CustomTcpMessage(ETCP_MSG_TYPE.SYN))
        router2.receive_tcp_msg(self, CustomTcpMessage(ETCP_MSG_TYPE.SYN))
        self.receive_tcp_msg(router2, CustomTcpMessage(ETCP_MSG_TYPE.SYN_ACK))
        router2.receive_tcp_msg(self, CustomTcpMessage(ETCP_MSG_TYPE.ACK))
        return