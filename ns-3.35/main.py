
from typing import Match

import ns.applications
import ns.core
import ns.dsdv
import ns.internet
import ns.network
import ns.point_to_point
from custom_network import CustomNetwork

import user_interface
from generate_network import generate_network
from keyboard_interpreter import read_command

network = CustomNetwork()

# Welcome the user
user_interface.welcome()
# Show the possible commands
user_interface.control_panel()
sc = 0

while True:
    sc = read_command()
    if sc == 1:
        network.print_network()
    if sc == 2:
        network.add_router(generate_network())
    # if we recieve a number 9, exit
    if sc == 9:
        break

user_interface.goodbye()
