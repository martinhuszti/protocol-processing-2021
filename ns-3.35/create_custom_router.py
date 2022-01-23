from ns.network import Node
from bcolors import bcolors

from custom_router import CustomRouter


# Predefined name is for testing purposes. If it is given we do not ask the name from the user
def create_custom_router(predefined_name=None, addr=None, subn=None):
    print('Generating new router...')
    if(predefined_name != None and addr != None and subn != None):
        name = predefined_name
        ip_address = addr
        subnet = subn
    else:
        name = input('Router name:')
        ip_address = input('Ip address:')
        while (len(ip_address) != (3+1 + 3+1 + 3+1 + 3)):
            print('Ip address format is not xxx.xxx.xxx.xxx! Please try again!')
            ip_address = input('Ip address:')

        subnet = int(input('Subnet:'))
        while (subnet < 0 and subnet > 32):
            print('Subnet has to be between 0 and 32! Please try again!')
            subnet = int(input('Subnet:'))



    print(bcolors.OKGREEN +
          f'..."{name}" {ip_address}/{subnet} router added to the network!' + bcolors.ENDC)
    return CustomRouter(name, ip_address, subnet)
