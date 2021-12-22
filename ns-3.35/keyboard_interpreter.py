from bcolors import bcolors

# Read command from user. Also check the validity of the given number
def read_command():
    while True:
        userinput = input('Selected command number then enter:')
        if not userinput.isdigit():
            print(bcolors.FAIL +
                  "The input is not number! Please try again!" + bcolors.ENDC)
            continue

        userinput_num = int(userinput)
        if (userinput_num < 1 or userinput_num > 9):
            print(
                bcolors.FAIL + "The selected command is out of range! Please try again!" + bcolors.ENDC)
            continue

        print('Thank you! The selected command is: ' + str(userinput_num)+'\n')
        return userinput_num
