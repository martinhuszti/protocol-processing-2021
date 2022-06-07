import time

def send_OPEN_message(from_ip, to_ip, timer=3):
    return ("OPEN", timer)

def send_KEEPALIVE_message(from_ip, to_ip):
    return ("KEEPALIVE")

def send_UPDATE_message(from_ip, to_ip, type, route):
    return ("UPDATE", type, route)

def send_NOTIFICATION_message(from_ip, to_ip, notification):
    return (notification)




def start_connection_BGP(router1, router2):
    return True

def start_connection_BGP(router1, router2):
    answer, timer = send_OPEN_message(router1, router2)
    if answer == "OPEN":
        print("sending OPEN message from", router1.ip_address, "to", router2.ip_address)
        answer2, timer = send_OPEN_message(router2, router1)
        if answer2 == "OPEN":
            print("sending OPEN message from", router2.ip_address, "to", router1.ip_address)
            while True:
                time.sleep(timer)
                print("sending KEEPALIVE message between", router1.ip_address, "and", router2.ip_address)
                if(send_KEEPALIVE_message(router1, router2) == "KEEPALIVE" and send_KEEPALIVE_message(router2, router1) == "KEEPALIVE"):
                    print("connection is ALIVE")
                    continue
                else:
                    print("The connection is broken!")
                    break

    print("An issue happend between the two routers")
    return False

