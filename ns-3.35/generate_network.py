from ns.network import Node
from bcolors import bcolors

from custom_router import CustomRouter


def generate_network():
    print('Generating new router...')
    name = input('Router name:')
    print(bcolors.OKGREEN +
          f'..."{name}" router added to the network!' + bcolors.ENDC)
    return CustomRouter(name=name)
