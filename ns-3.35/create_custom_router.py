from bcolors import bcolors

from custom_router import CustomRouter
import re # to check input syntax

# Predefined name is for testing purposes. If it is given we do not ask the name from the user
def create_custom_router(predefined_name=None, addr=None, subn=None):
    print('Generating new router...')
    if(predefined_name != None and addr != None and subn != None):
        name = predefined_name
        ip_address = addr
        subnet = subn
    else:
        #user inserts the name of the router
        name = input('Router name:')

        #user inserts the IP of the router
        ip_address = input('Ip address:')
        valid_address = 0 #becomes 1 if IP is correct
        checkIP = re.compile(r'\d(\d)?(\d)?\.') #allow only decimals and dot

        while (valid_address == 0):
            if len(ip_address) < 7:
                print('IP address is too short! Please try again!')

            elif len(ip_address) > 15:
                print('IP address is too long! Please try again!')

            elif checkIP.match(ip_address): #check if user inserted valid characters
                if ip_address.count(".") == 3: #check number of dots (otherwise an IP like 1.2.3.4.5 was valid)
                    print('The IP you inserted is correct!')
                    #TO DO: check if the inserted IP already exist!
                    valid_address = 1
                    continue
                else:
                    print('You inserted too many dots! Use only 3! xxx.xxx.xxx.xxx')
            else:
                print('You inserted wrong characters! Use only numbers and the dot (.) between them!')
                print('Examples: 1.1.1.1 or 10.100.10.100')

            ip_address = input('Ip address:')

        #user inserts the subnet
        subnet = input('Subnet:')
        valid_subnet = 0 #becomes 1 if subnet is correct
        checkNet = re.compile(r'\d(\d)?') #allow only decimals

        while valid_subnet == 0:
            if checkNet.match(subnet):          #if the user inserted numbers
                subnet = int(subnet)            #we convert the string to int
                if subnet < 0 or subnet > 32:   #and check the length
                    print('Subnet has to be between 0 and 32! Please try again!')
                else:
                    print('Well done')
                    valid_subnet = 1
                    continue
            else:
                print('Use only numbers!')

            subnet = input('Subnet:')

    print(bcolors.OKGREEN +
          f'..."{name}" {ip_address}/{subnet} router added to the network!' + bcolors.ENDC)
    return CustomRouter(name, ip_address, subnet)
