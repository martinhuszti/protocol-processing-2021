from custom_network import CustomNetwork

import user_interface
from create_custom_router import create_custom_router
from keyboard_interpreter import read_command
from simulation import start_simulation

network = CustomNetwork()

# Welcome the user
user_interface.welcome()
# Show the possible commands
user_interface.control_panel()

# Tasks to be implemented:

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
        network.add_link(network)
        continue
    if sc == 5:
        network.remove_link()
        continue
    if sc == 6:
        network.send_packet()
        continue
    if sc == 7:
        network.update_link_cost()
        continue
    if sc == 8:
        user_interface.control_panel()
        continue
    if sc == 9:
        network = start_simulation()
    if sc == 10:
        break

user_interface.goodbye()
