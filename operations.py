
import os


# UTILITY FOR GETTING THE SIZE OF COMMAND PROMPT TO MAKE THINGS LOOK PRETTY
class SizeOfTerminal:
    def __init__(self, columns):
        self.columns = columns

try:
    size = os.get_terminal_size()
except:
    size = SizeOfTerminal(60)

# PRINTS HEADER
def print_header():
    print("#"*size.columns)
    print("E - C O M M E R C E   M A N A G E M E N T   S Y S T E M".center(size.columns))
    print("#"*size.columns)

# CLEARS THE CONSOLE/TERMINAL
def clear_console():
    try:
        os.system("cls")
    except:
        print("\n" * 50)
    print_header()

def print_details(data):
    clear_console()
    
    print("\n")
    print("Customer Details".center(size.columns))
    
    print(right_align("Logged in as: {}".format(data[1])))
    
    print("\n\n\tFirst Name: ", data[2])
    print("\n\tLast Name: ", data[3])
    print("\n\tEmail: ", data[4])
    print("\n\tAddress: ", data[6])
    print("\n\tPostal Code: ", data[7])
    print("\n\tCity: ", data[8])
    print("\n\tPhone: ", data[9])
    
    print("\n\n\n\tPress Enter to return...")
    input("")
    
def right_align(txt):
    spaces = int(size.columns - 4 - len(txt))
    return " "*spaces + txt