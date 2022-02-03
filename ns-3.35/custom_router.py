from queue import Empty
from custom_packet import CustomPacket
from custom_tcp_message import ETCP_MSG_TYPE, CustomTcpMessage
from bcolors import bcolors

from random import random
from prettytable import PrettyTable  # to print routing tables in a cute way


class CustomRouter:
    def __init__(self, name='No name given', ip_address="255.255.255.255", subnet=32):
        self.name = name
        self.links = []  # the link and the routing table index are matching
        self.routing_table = []  # Tuple with destination ip_address, subnet mask, metric
        self.ip_address = ip_address
        self.subnet = subnet

    def print(self):
        print(self.name)

    def print_tables(self):
        t = PrettyTable(['Destination', 'Netmask', 'Metric'])
        if not self.routing_table:
            print('This table is currently empty!')
            return
        for r in self.routing_table:
            t.add_row([r[0], r[1], r[2]])
        print(t)

    def send_tcp_msg(self, _to, msg: CustomTcpMessage):
        self.current_seq_num = random()
        # If syn, generate seq number otherwise it is containing already
        if msg.type == ETCP_MSG_TYPE.SYN or msg.type == ETCP_MSG_TYPE.FIN:
            msg.seq_num = self.current_seq_num
            print(f'{self.name}: sending {msg.type.name} message to {_to.name}')
        # Simulate that the message is arrived to the router
        _to.receive_tcp_msg(self, msg)

    def receive_tcp_msg(self, _from, tcp_message: CustomTcpMessage):
        print(f'{self.name}: TCP message arrived: {tcp_message.type.name}')
        _type = tcp_message.type

        # 1. Start with SYN
        if _type == ETCP_MSG_TYPE.SYN:
            print(f'{self.name}: sending back syn-ack with ')
            self.send_tcp_msg(_to=_from, msg=CustomTcpMessage(
                type=ETCP_MSG_TYPE.SYN_ACK, seq_num=tcp_message.seq_num, ip_address=self.ip_address,
                subnet=self.subnet))

        # 2. Answer with SYN-ACK and send the ip range
        if _type == ETCP_MSG_TYPE.SYN_ACK:
            if tcp_message.seq_num == self.current_seq_num:
                print(
                    f"{self.name}: The sequence number is correct, initializing connection")
                self.send_tcp_msg(
                    _from, CustomTcpMessage(type=ETCP_MSG_TYPE.ACK))
                self.current_seq_num = 0
                self.links.append(_from)
                self.routing_table.append((_from.ip_address, _from.subnet, 1))  # 1 is the hop ->
                # TO DO: create a better function to determine metrics

        if _type == ETCP_MSG_TYPE.ACK:
            if tcp_message.is_fin_ack_response:
                print(
                    f"{self.name}: ACK arrived to the FIN_ACK message. Removing the link...")
                self.links.remove(_from)
            else:
                print(f"{self.name}: Initializing connection")
                self.links.append(_from)
                self.routing_table.append((_from.ip_address, _from.subnet, 1))  # 1 is the hop ->
                # TO DO: create a better function to determine metrics

        if _type == ETCP_MSG_TYPE.FIN_ACK:
            self.links.remove(_from)
            print(
                f"{self.name}: Sending back ACK with is_fin_ack_response true flag")
            self.send_tcp_msg(
                _from,
                CustomTcpMessage(type=ETCP_MSG_TYPE.ACK,
                                 is_fin_ack_response=True)
            )

        if _type == ETCP_MSG_TYPE.FIN:
            # Only if ACK arrives remove from the list
            print(f"{self.name}: Sending back FIN_ACK")
            self.send_tcp_msg(_from, CustomTcpMessage(
                type=ETCP_MSG_TYPE.FIN_ACK))

    def send_packet(self, packet: CustomPacket):
        if packet.ip_from == self.ip_address:
            print(f"{self.name}: I'm sending a packet to: {packet.ip_to}")
        else:
            print(f"{self.name}: A new packet arrived.")

        if packet.ip_to == self.ip_address:
            print(
                f"{self.name}:" + bcolors.OKGREEN +
                f" The destination of the packet is me! It's arrived to the destination! {self.ip_address}"
                + bcolors.ENDC)
            return

        found_router = Empty
        for link in self.links:
            if link.ip_address == packet.ip_to:
                found_router = link
                break

        if found_router != Empty:
            found_router.send_packet(packet)
        else:
            print(f"{self.name}:" + bcolors.FAIL + " Error! The destination is unreachable!" + bcolors.ENDC)
