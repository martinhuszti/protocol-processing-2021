from bcolors import bcolors

from custom_router import CustomRouter
import re  # to check input syntax


# Predefined name is for testing purposes. If it is given we do not ask the name from the user
def create_custom_router(predefined_name=None, addr=None, subn=None):
    print('Generating new router...')
    if predefined_name is not None and addr is not None and subn is not None:
        name = predefined_name
        ip_address = addr
        subnet = subn
    else:
        # user inserts the name of the router
        name = input('Router name:')

        # user inserts the IP of the router
        ip_address = input('Ip address:')
        valid_address = 0  # becomes 1 if IP is correct
        checkIP = re.compile(r'\d(\d)?(\d)?\.')  # allow only decimals and dot

        while valid_address == 0:
            if len(ip_address) < 7:
                print(bcolors.WARNING + 'IP address is too short! Please try again!' + bcolors.ENDC)
            # we can remove the check on the length if you want, the other one is enough to prevent wrong inputs
            elif len(ip_address) > 15:
                print(bcolors.WARNING + 'IP address is too long! Please try again!' + bcolors.ENDC)

            elif checkIP.match(ip_address):  # check if user inserted valid characters
                if ip_address.count(".") != 3:  # check number of dots (otherwise an IP like 1.2.3.4.5 was valid)
                    print(bcolors.WARNING + 'You inserted too many dots! Use only 3! ' + bcolors.OKBLUE +
                          'Example: 1.2.3.4' + bcolors.ENDC)
                else:
                    octets = ip_address.split(".")  # split the IP in different subsection i.e.['1','2','3','4']

                    for part in octets:  # check if the value in each part is valid
                        if not 0 <= int(part) <= 255:
                            print(bcolors.WARNING + 'You inserted an invalid IP!' + bcolors.ENDC)
                            valid_address = 0
                            break
                        else:
                            valid_address = 1
            else:
                print(bcolors.WARNING + 'You inserted wrong characters!'
                                        '\nUse only numbers and the dot (.) between them!' + bcolors.ENDC)
                print(bcolors.OKBLUE + 'Examples: 1.1.1.1 or 10.100.10.100' + bcolors.ENDC)

            if valid_address != 1:
                ip_address = input('Ip address:')

        # user inserts the subnet
        subnet = input('Subnet:')
        valid_subnet = 0  # becomes 1 if subnet is correct
        checkNet = re.compile(r'\d(\d)?')  # allow only decimals

        while valid_subnet == 0:
            if checkNet.match(subnet):  # if the user inserted numbers
                subnet = int(subnet)  # we convert the string to int
                if subnet < 0 or subnet > 32:  # and check the length
                    print(bcolors.WARNING + 'Subnet has to be between 0 and 32! Please try again!' + bcolors.ENDC)
                else:
                    # print(bcolors.OKGREEN + 'Well done' + bcolors.ENDC)
                    valid_subnet = 1
                    continue
            else:
                print(bcolors.WARNING + 'Use only numbers!' + bcolors.ENDC)

            subnet = input('Subnet:')

    return CustomRouter(name, ip_address, subnet)
