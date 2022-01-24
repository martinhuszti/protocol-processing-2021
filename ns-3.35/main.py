
from typing import Match

import ns.applications
import ns.core
import ns.dsdv
import ns.internet
import ns.network
import ns.point_to_point
from custom_network import CustomNetwork

import user_interface
from create_custom_router import create_custom_router
from keyboard_interpreter import read_command

network = CustomNetwork()

# Welcome the user
user_interface.welcome()
# Show the possible commands
user_interface.control_panel()

#Tasks to be implemented:

network.add_router(create_custom_router('Test_router_1',"100.0.0.0",8))
network.add_router(create_custom_router('Test_router_2',"110.0.0.0",8))
network.add_link(0,1)
# Each router has router table
# Create suitable IP packets (need header field)
# Error conditions (router offline, link dropped)
# Voting
#

# BGP Messages: OPEN, UPDATE, NOTIFICATION, KEEP_ALIVE
while True:
    sc = read_command()
    if sc == 1:
        network.print_network()
        continue
    if sc == 2:
        network.add_router(create_custom_router())
        continue
    if sc == 3:
        network.remove_router()
        continue
    if sc == 4:
        network.add_link()
        continue
    if sc == 5:
        network.remove_link()
        continue
    if sc == 6:
        network.send_packet()
        continue
    if sc == 8:
        user_interface.control_panel()
        continue
    if sc == 9:
        break

user_interface.goodbye()
