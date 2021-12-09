from bcolors import bcolors


def print_line():
    print("______________________________\n")


def welcome():
    print(bcolors.BOLD + bcolors.UNDERLINE +
          "Turku - 2021 The program made by:"+bcolors.ENDC)
    print(bcolors.OKBLUE + "- Marco Bertolino ")
    print("- Martin Huszti 🌵 ")
    print("- Mirko Ioris")
    print("- Francesco Pavanello")
    print("- Victor Schmit"+bcolors.ENDC)
    print_line()


def control_panel():
    print(bcolors.BOLD + bcolors.HEADER +
        'Moi! Welcome to our network simulator for Protocol Processing 2021! 🔥 \n' + bcolors.ENDC)
    print(bcolors.UNDERLINE+"Choose what you want to do: \n" + bcolors.ENDC)
    print("- 1. Show topology")
    print("- 2. Add router")
    print("- 3. Add link")
    print("- 4. Remove router")
    print("- 5. Remove link\n")
    print("- 9. Exit\n")

def goodbye():
    
    print(bcolors.BOLD + bcolors.UNDERLINE +
          "Thank you for using our program!"+bcolors.ENDC)
