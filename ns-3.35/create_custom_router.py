from ns.network import Node
from bcolors import bcolors

from custom_router import CustomRouter


# Predefined name is for testing purposes. If it is given we do not ask the name from the user
def create_custom_router(predefined_name = None):
    print('Generating new router...')
    if(predefined_name != None):
      name = predefined_name
    else:
      name = input('Router name:')

    print(bcolors.OKGREEN +
          f'..."{name}" router added to the network!' + bcolors.ENDC)
    return CustomRouter(name=name)
