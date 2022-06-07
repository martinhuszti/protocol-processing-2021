from bcolors import bcolors


# Read command from user. Also check the validity of the given number
def read_command():
    while True:
        userinput = input('Select command (8 for help):')
        if not userinput.isdigit():
            print(bcolors.FAIL +
                  "The input is not a number! Please try again!" + bcolors.ENDC)
            continue

        userinput_num = int(userinput)
        if userinput_num < 1 or userinput_num > 10:
            print(
                bcolors.FAIL + "The selected command is out of range! Please try again!" + bcolors.ENDC)
            continue

        print(bcolors.OKBLUE + 'Thank you! The selected command is: ' + str(userinput_num) + '\n' + bcolors.ENDC)
        return userinput_num
