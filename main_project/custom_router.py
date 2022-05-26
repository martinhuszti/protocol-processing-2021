from queue import Empty
from custom_packet import CustomPacket
from custom_tcp_message import ETCP_MSG_TYPE, CustomTcpMessage
from bcolors import bcolors
import ipaddress
from random import random
from prettytable import PrettyTable  # to print routing tables in a cute way


class CustomRouter:
    def __init__(self, AS_id='No AS_id given', ip_address="255.255.255.255", subnet=32):
        self.AS_id = AS_id
        self.routing_table = []  # List of dictionaries with destination_network, subnet_mask, AS_PATH, next_hop, cost
        self.neighbor_table = [] # List of dictionaries with AS_id, ip_address, cost, reference
        self.bgp_table = [] # List of dictionaries with destination_network, subnet_mask, AS_PATH, next_hop, cost
        self.ip_address = ip_address
        self.subnet = subnet

    def print(self):
        print(self.AS_id)

    ############################
    #TODO UPDATE WITH THE NEW STRUCTURE

    def print_tables(self): 
        t = PrettyTable(['Destination', 'Gateway', 'Netmask', 'Cost'])
        if not self.routing_table:
            print('This table is currently empty!')
            return
        for r in self.routing_table:
            t.add_row([r[0], r[1], r[2], r[3]])
        print(t)

    ########################

    def send_tcp_msg(self, _to, msg: CustomTcpMessage):
        self.current_seq_num = random()
        # If syn, generate seq number otherwise it is containing already
        if msg.type == ETCP_MSG_TYPE.SYN or msg.type == ETCP_MSG_TYPE.FIN:
            msg.seq_num = self.current_seq_num
            print(f'{self.AS_id}: sending {msg.type.name} message to {_to.AS_id}')
        # Simulate that the message is arrived to the router
        _to.receive_tcp_msg(self, msg)

    def receive_tcp_msg(self, _from, tcp_message: CustomTcpMessage):
        print(f'{self.AS_id}: TCP message arrived: {tcp_message.type.name}')
        _type = tcp_message.type

        # 1. Start with SYN
        if _type == ETCP_MSG_TYPE.SYN:
            print(f'{self.AS_id}: sending back syn-ack with ')
            self.send_tcp_msg(_to=_from, msg=CustomTcpMessage(
                type=ETCP_MSG_TYPE.SYN_ACK, seq_num=tcp_message.seq_num, ip_address=self.ip_address,
                subnet=self.subnet))

        # 2. Answer with SYN-ACK and send the ip range
        if _type == ETCP_MSG_TYPE.SYN_ACK:
            if tcp_message.seq_num == self.current_seq_num:
                print(f"{self.AS_id}: The sequence number is correct, initializing connection")
                self.send_tcp_msg(_from, CustomTcpMessage(type=ETCP_MSG_TYPE.ACK))
                self.current_seq_num = 0
                self.set_neighbor(_from, 1)
                # TODO: create a better function to determine metrics

        if _type == ETCP_MSG_TYPE.ACK:
            if tcp_message.is_fin_ack_response:
                print(
                    f"{self.AS_id}: ACK arrived to the FIN_ACK message. Removing the link...")
            else:
                print(f"{self.AS_id}: Initializing connection")
                self.set_neighbor(_from, 1)
                # TODO: create a better function to determine metrics

        if _type == ETCP_MSG_TYPE.FIN_ACK:
            print(
                f"{self.AS_id}: Sending back ACK with is_fin_ack_response true flag")
            self.send_tcp_msg(
                _from,
                CustomTcpMessage(type=ETCP_MSG_TYPE.ACK,
                                 is_fin_ack_response=True)
            )

        if _type == ETCP_MSG_TYPE.FIN:
            # Only if ACK arrives remove from the list
            print(f"{self.AS_id}: Sending back FIN_ACK")
            self.send_tcp_msg(_from, CustomTcpMessage(
                type=ETCP_MSG_TYPE.FIN_ACK))

    def send_packet(self, packet: CustomPacket):
        if packet.ip_from == self.ip_address:
            print(f"{self.AS_id}: I'm sending a packet to: {packet.ip_to}")
        else:
            print(f"{self.AS_id}: A new packet arrived.")

        if packet.ip_to == self.ip_address:
            print(
                f"{self.AS_id}:" + bcolors.OKGREEN +
                f" I am the destination of the packet! It's arrived to the destination! {self.ip_address}"
                + bcolors.ENDC)
            return

        found_router = self.select_next_hop(packet.ip_to)
        if found_router:
            found_router.reference.send_packet(packet)
        else:
            print(f'{bcolors.FAIL}Error: no possible route found{bcolors.ENDC}')

    def set_neighbor(self, neighbor, cost):
        tmp = False
        for _as in self.neighbor_table:
            if _as['AS_id'] == neighbor.AS_id:
                _as['cost'] = cost
                tmp = True
                break
        if not tmp:
            self.neighbor_table.append({'AS_id': neighbor.AS_id, 'ip_address': neighbor.ip_address, 'cost': cost})

    def select_next_hop(self, ip_address):
        for neighbor in self.neighbor_table:
            if ip_address == neighbor['ip_address']:
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
            if next_hop == neighbor[1]: 
                cost += neighbor[2]
                tmp = True
                break
        if not tmp:
            return f'{bcolors.FAIL}Error: unknwon next hop{bcolors.ENDC}'
        
        already_in_bgp_table = False
        pos = 0
        for elem in self.bgp_table:
            if network == elem['destination_network'] and subnet_mask == elem['subnet_mask'] and AS_path == elem['AS_path'] and next_hop == elem['next_hop']:
                already_in_bgp_table = True
                break
            pos += 1
        if not already_in_bgp_table:
            self.bgp_table.append({'destination_network': network, 'subnet_mask': subnet_mask, 'AS_path': AS_path, 'next_hop': next_hop, 'cost': cost})
        else:
            self.routing_table[pos]['cost'] = cost
        
        already_in_routing_table = False
        pos = 0
        for elem in self.routing_table:
            if network == elem['destination_network'] and subnet_mask == elem['subnet_mask']:
                already_in_routing_table = True
                break
            pos += 1
        if not already_in_routing_table:
            self.routing_table.append({'destination_network': network, 'subnet_mask': subnet_mask, 'AS_path': AS_path, 'next_hop': next_hop, 'cost': cost})
        else:
            if self.routing_table[pos]['cost'] > cost or (self.routing_table[pos]['cost'] == cost and len(self.routing_table[pos]['AS_path']) > len(AS_path)):
                self.routing_table[pos]['cost'] = cost
                self.routing_table[pos]['next_hop'] = next_hop
                self.routing_table[pos]['AS_path'] = AS_path
