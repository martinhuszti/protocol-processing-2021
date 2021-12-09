from ns.network import Node

from custom_router import CustomRouter

def generate_network():
    print('Generating new router...')
    name = input('Router name:')
    print(f'..."{name}" router added to the network!')
    return CustomRouter(name=name)
