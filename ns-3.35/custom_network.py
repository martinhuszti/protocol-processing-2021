from bcolors import bcolors
from user_interface import print_line


class CustomNetwork:
    def __init__(self):
        self.routers = []

    def add_router(self, router):
        self.routers.append(router)

    def add_link(self, router):
        first_router = input('First router:')
        second_router = input('Second router:')


    def remove_router(self):
        self.print_network()
        sr = input('Which router you want to remove: ')
        if(sr.isdigit() and int(sr) >= 0 and int(sr) <= len(self.routers)-1):
            self.routers.pop(int(sr))
            print(bcolors.OKGREEN + "The router successfully removed!" + bcolors.ENDC)
        else:
            print(bcolors.FAIL + "The given index is not correct!" + bcolors.ENDC)

    def print_network(self):
        print(bcolors.OKCYAN+"Current network topology:")
        for i, r in enumerate(self.routers):
            print(f'{i}: {r.name}')
        print_line()
        print(bcolors.ENDC)
