from enum import Enum
import string

class BGP_MSG_TYPE(Enum):
    OPEN = 1
    KEEP_ALIVE = 2
    UPDATE = 3
    ERROR = 4


class BgpMessage:
    def __init__(self) -> None:
        pass

class OpenBgpMessage(BgpMessage):
    def __init__(self, ASNumber: int, HoldTime: int, RouterID: string, ) -> None:
        self.ASNumber = ASNumber
        self.HoldTime = HoldTime
        self.RouterID = RouterID
        self.type = BGP_MSG_TYPE.OPEN
        pass
    
class KeepAliveBgpMessage(BgpMessage):
    def __init__(self, is_open_response: bool=False) -> None:
        self.type = BGP_MSG_TYPE.KEEP_ALIVE
        pass

class UpdateBgpMessage(BgpMessage):
    """
    withdrown routes are now unreachable
    an update is sent for each new route
    Origin: Mandatory attribute that defines the origin of the path information
    AS Path: Mandatory attribute composed of a sequence of autonomous system path segments
    Next Hop: Mandatory attribute that defines the IP address of the border router that should be used as the next hop to destinations listed in the network layer reachability information field
    """
    def __init__(self, WithdrawnRoutes: list, Origin: string, ASPath: list, NextHop: string, NLRIPrefix: string, NLRILegth: string ) -> None:
        
        
        self.WithdrawnRoutes = WithdrawnRoutes
        self.Origin = Origin
        self.ASPath = ASPath
        self.NextHop = NextHop
        self.NLRIPrefix = NLRIPrefix
        self.NLRILegth = NLRILegth
        self.type = BGP_MSG_TYPE.UPDATE
        pass
    

class BGP_ERROR_TYPE(Enum):
    HEADER_ERROR = 1
    OPEN_ERROR = 2
    UPDATE_ERROR = 3
    HOLD_TIME_EXPIRED = 4
    FINITE_STATE_MACHINE_ERROR = 5
    CEASE = 6



class NotificationBgpMessage(BgpMessage):
    """
    """
    def __init__(self, ErrorType: BGP_ERROR_TYPE, ErrorSubcode: int, ErrorData: string) -> None:
        self.ErrorType = ErrorType
        self.ErrorSubcode = ErrorSubcode
        self.ErrorData = ErrorData
        self.type = BGP_MSG_TYPE.ERROR
        pass