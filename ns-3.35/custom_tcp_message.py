from enum import Enum


class ETCP_MSG_TYPE(Enum):
    SYN = 1
    ACK = 2
    SYN_ACK = 3
    FIN = 4
    FIN_ACK = 5


class CustomTcpMessage:
    seq_num = 0

    def __init__(self, type: ETCP_MSG_TYPE, seq_num=-1, is_fin_ack_response=False, ip_address="0.0.0.0", subnet=32) -> None:
        self.type = type
        self.seq_num = seq_num
        self.ip_address = ip_address
        self.subnet = subnet
        # Meaning that the router is ack the finack request (need the router to not create new connection)
        self.is_fin_ack_response = is_fin_ack_response
        pass
