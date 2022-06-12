from bcolors import bcolors


def print_line():
    print("______________________________\n")


def welcome():
    print(bcolors.BOLD + bcolors.UNDERLINE +
          "Turku - 2021 The program made by:"+bcolors.ENDC)
    print(bcolors.OKBLUE + "- Marco Bertolino 🦄 ")
    print("- Martin Huszti 🌵 ")
    print("- Mirko Ioris 🪐 ")
    print("- Francesco Pavanello 👾 ")
    print("- Victor Schmit ✊ "+bcolors.ENDC)
    print_line()
    print(bcolors.BOLD + bcolors.HEADER +
        'Moi! Welcome to our network simulator for Protocol Processing 2021! 🔥 \n' + bcolors.ENDC)

def control_panel():
    print(bcolors.UNDERLINE+"Choose what you want to do: \n" + bcolors.ENDC)
    print("- 1. Show topology")
    print("- 2. Add router")
    print("- 3. Remove router")
    print("- 4. Add link")
    print("- 5. Remove link")
    print("- 6. Send packet from router to router")
    print("- 7. Update link cost")
    print("- 8. Show commands")
    print("- 9. Start simulation")
    print("- 10. Reset current network\n")
    print("- 11. Exit\n")

def goodbye():
    
    print(bcolors.BOLD + bcolors.UNDERLINE +
          "Thank you for using our program!"+bcolors.ENDC)
