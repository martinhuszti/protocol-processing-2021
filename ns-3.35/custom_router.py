from custom_tcp_message import ETCP_MSG_TYPE, CustomTcpMessage

from random import random


class CustomRouter:
    def __init__(self, name='No name given'):
        self.name = name
        self.links = []

    def print(self):
        print(self.name)

    def send_tcp_msg(self, _to, msg: CustomTcpMessage):
        self.current_seq_num = random()
        # If syn, generate seq number
        if(msg.type == ETCP_MSG_TYPE.SYN):
            msg.seq_num = self.current_seq_num
            print(f'{self.name}: sending SYN message to {_to.name}')
        _to.receive_tcp_msg(self, msg)

    # Need to add _from router to be able to call back
    def receive_tcp_msg(self, _from, tcp_message: CustomTcpMessage):
        print(f'{self.name}: TCP message arrived: {tcp_message.type.name}')
        _type = tcp_message.type

        if _type == ETCP_MSG_TYPE.SYN:
            print(f'{self.name}: sending back syn-ack with ')
            self.send_tcp_msg(_to=_from, msg=CustomTcpMessage(
                type=ETCP_MSG_TYPE.SYN_ACK, seq_num=tcp_message.seq_num))

        if _type == ETCP_MSG_TYPE.SYN_ACK:
            if(tcp_message.seq_num == self.current_seq_num):
                print(f"{self.name}: The sequence number is correct, initalizing connection")
                self.send_tcp_msg(_from,CustomTcpMessage(type=ETCP_MSG_TYPE.ACK))
                self.current_seq_num = 0
                self.links.append(_from)
        
        if _type == ETCP_MSG_TYPE.ACK:
            print(f"{self.name}: Initializing connection")
            self.links.append(_from)

        if _type == ETCP_MSG_TYPE.FIN:
            self.links.remove(_from)
