from ens import ENS
import os
import random
from terminaltables import AsciiTable
import threading
import time
import web3

# Initializing the variables to store statistics of the domain name check
stats = {
    'checked': 0,
    'checks_per_second': 0,
    'failed_checks': 0,
    'time_difference': 0,
    'checked_strings': []
}

# Initializing the variables to store the table data
table_data = [["Successful", "Failed", "Average", "Running Time"], [0, 0, 0, 0]]
table = AsciiTable(table_data)

# Function to clear the console
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


class Checker:
    # Reading node url from 'node.txt' file, default setting is https://eth.llamarpc.com
    node = file = open('node.txt','r').readline()
    ns = ENS.fromWeb3(web3.Web3(web3.HTTPProvider(node)))

    # Method to check the availability of randomly generated domain names
    def random_check(self, charset, length):
        try:
            # Generating a random string of the given length from the given charset
            random_string = ''.join(random.choice(charset) for i in range(int(length)))
            domain_name = '{}{}'.format(random_string, '.eth')

            # Check if the domain name has already been checked or not and if the address and owner of the domain name are unset
            string_already_checked = random_string in stats['checked_strings']
            address_unset = self.ns.address(domain_name) == None
            owner_unset = self.ns.owner(domain_name) == '0x0000000000000000000000000000000000000000'

            # If the domain name is available, write it to the 'available.txt' file
            if address_unset and owner_unset and not string_already_checked:
                with open('available.txt', 'a') as f:
                    f.writelines(f'{domain_name}\n')

            # Updating statistics
            stats['checked_strings'].append(random_string)
            stats['checked'] += 1

        except:
            stats['failed_checks'] += 1

    # Method to check the availability of a given string (generated in redirect(mode=2)) as a domain name
    def sorted_check(self, sorted_string):
        try:
            domain_name = '{}{}'.format(sorted_string, '.eth')

            # Check if the domain name has already been checked or not and if the address and owner of the domain name are unset
            string_already_checked = sorted_string in stats['checked_strings']
            address = self.ns.address(domain_name) == None
            owner = self.ns.owner(domain_name) == '0x0000000000000000000000000000000000000000'
    
            # If the domain name is available, write it to the 'available.txt' file
            if address and owner and not string_already_checked:
                with open('available.txt', 'a') as f:
                    f.writelines(f'{domain_name}\n')
    
            # Updating statistics
            stats['checked_strings'].append(sorted_string)
            stats['checked'] += 1

        except:
            stats['failed_checks'] += 1

    # Method to check the availability of domain names from a given file
    def file_check(self, eth, file, start_time):
        for line in file:
            domain_name = '{}{}'.format(line, eth)

            # Check if the address and owner of the domain name are unset
            address = self.ns.address(domain_name)
            owner = self.ns.owner(domain_name) == '0x0000000000000000000000000000000000000000'

            # If the domain name is available, write it to the 'available.txt' file
            if address == None and owner:
                with open('available.txt', 'a') as f:
                    f.writelines(f'{domain_name}\n')
                
            # Updating statistics
            stats['checked'] += 1
            stats['time_difference'] = time.time() - start_time
            stats['checks_per_second'] = (stats['checked'] + stats['failed_checks']) / stats['time_difference']

            # Printing statistics to the console using a table
            table.table_data[1] = [stats['checked'], stats['failed_checks'], round(stats['checks_per_second'], 2), round(stats['time_difference'], 2)]
            print(table.table)

            print("\033[H\033[J", end="")


def redirect(charset, eth, file, length, mode, quantity_to_be_checked):
    start_time = time.time()
    time.sleep(0.00000001)

    # Mode 1 (randomly generated functions)
    if mode == 1:
        for i in range(quantity_to_be_checked):

            # Executing the random_check() function
            thread = threading.Thread(target=Checker().random_check, args=(charset, length))
            thread.start()

            # Updating statistics
            stats['time_difference'] = time.time() - start_time
            stats['checks_per_second'] = (stats['checked'] + stats['failed_checks']) / stats['time_difference']

            # Printing statistics to the console using a table
            table.table_data[1] = [stats['checked'], stats['failed_checks'], round(stats['checks_per_second'], 2), round(stats['time_difference'], 2)]
            print(table.table)

            # Delay is necessary due to node limitation
            time.sleep(0.085)

            print("\033[H\033[J", end="")

    # Mode 2 (alphabetically sorted, non-randomly generated domain names)
    elif mode == 2:
        output = []

        for i in range(quantity_to_be_checked):
            s = ''

            # Generating the strings
            for j in range(length):
                s += charset[i%len(charset)]
                i //= len(charset)
            output.append(s)

            sorted_string = output[i-1][::-1]

            # Executing the sorted_check() function
            Checker.sorted_check(Checker, sorted_string)

            # Updating statistics
            stats['time_difference'] = time.time() - start_time
            stats['checks_per_second'] = (stats['checked'] + stats['failed_checks']) / stats['time_difference']

            # Printing statistics to the console using a table
            table.table_data[1] = [stats['checked'], stats['failed_checks'], round(stats['checks_per_second'], 2), round(stats['time_difference'], 2)]
            print(table.table)

            print("\033[H\033[J", end="")

    # Mode 3 (checking domain names from a given file)
    elif mode == 3:
        # Executing the file_check() function
        Checker.file_check(Checker, eth, file, start_time)

    clear()

    # 
    end_time = time.time()
    checked = stats['checked']

    input(f'Done, checked {checked} domain names in {str(round(abs(end_time - start_time)))} seconds.')


# Setting up the variables
class Setup:

    # Variables for mode 1 or 2
    def settings_for_generating(mode):

        # Length of the domain names
        length = int(input(f'Enter the length of the domain name >>> '))

        clear()

        print('Select the character set:')
        print('[1] 0123456789')
        print('[2] abcdefghijklmnopqrstuvwxyz')
        print('[3] 0123456789abcdefghijklmnopqrstuvwxyz')
        print('[4] CUSTOM')
        print()

        select_character_set_option = int(input('Enter your option >>> '))

        clear()

        # Assignment of the appropriate character set based on user input
        if select_character_set_option == 1:
          charset = '0123456789'
        elif select_character_set_option == 2:
          charset = 'abcdefghijklmnopqrstuvwxyz'
        elif select_character_set_option == 3:
          charset = '0123456789abcdefghijklmnopqrstuvwxyz'
        elif select_character_set_option == 4:
          print('You can use numbers from 0 to 9 and lowercase letters. Use the following syntax: 123abc')
          print()

          charset = input('Custom character set >>> ')

        clear()

        # Quantity of domain names which will be checked
        quantity_to_be_checked = int(input('How many domain names should be checked? >>> '))

        clear()

        eth = None
        file = None

        # Redirecting
        redirect(charset, eth, file, length, mode, quantity_to_be_checked)

    # Variables for mode 3
    def settings_for_file(mode):

        # File name
        file_name = input('Enter the name of the file, e.g. file.txt >>> ')

        file = open(file_name,'r').read().splitlines()
        
        clear()
        
        # Ending of the given strings
        ending = input(f'Do the strings in {file_name} end with ".eth"? Y/N >>> ')
        
        if ending == 'Y' or ending == 'y':
          eth = ''
        elif ending == 'N' or ending == 'n':
          eth = '.eth'
        
        clear()

        charset = None
        length = None
        quantity_to_be_checked = None
        
        # Redirecting
        redirect(charset, eth, file, length, mode, quantity_to_be_checked)

    # Start
    def start():
        clear()

        # Selection of the mode
        print('[1] Check domain names based on random strings with a specific length and character set.')
        print('[2] Check domain names based on alphabetically sorted strings with a specific length and character set.')
        print('[3] Check domain names given in a specific text file.')
        print('Note: In all cases, the available domain names are saved in a file called "available.txt".')
        print()

        mode = int(input('Enter your option >>> '))

        clear()

        if mode == 1 or mode == 2:
            Setup.settings_for_generating(mode)

        elif mode == 3:
            Setup.settings_for_file(mode)

Setup.start()