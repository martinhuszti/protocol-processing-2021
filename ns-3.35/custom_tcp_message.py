from enum import Enum


class ETCP_MSG_TYPE(Enum):
    SYN = 1
    ACK = 2
    SYN_ACK = 3
    FIN = 4


class CustomTcpMessage:
    seq_num = 0

    def __init__(self, type: ETCP_MSG_TYPE, seq_num = -1) -> None:
        self.type = type
        self.seq_num = seq_num
        pass
