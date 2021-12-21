
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

network.add_router(create_custom_router('predefined router 1'))
network.add_router(create_custom_router('predefined router 2'))
network.add_link(0,1)
# Keepalive messages needed when an iteration is running
# Set up TCP con between the routers
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
    if sc == 2:
        network.add_router(create_custom_router())
    if sc == 3:
        network.add_link()
    if sc == 4:
        network.remove_router()
    # if we recieve a number 9, exit
    if sc == 9:
        break

user_interface.goodbye()
