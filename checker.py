import warnings
warnings.simplefilter(action = 'ignore', category = FutureWarning)

from concurrent.futures import ThreadPoolExecutor
from ens import ENS
import os
import random
import threading
import web3


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


class Checker:
    # declaration of variables
    checked = 0
    lock = threading.Lock()
    node = file = open('node.txt','r').readline() # default setting is https://eth.llamarpc.com
    pool = ThreadPoolExecutor(max_workers=200)
    w3 = web3.Web3(web3.HTTPProvider(node))
    ns = ENS.fromWeb3(w3)

    # general check function, mode is specified in Setup.start()
    def check(self, charset, eth, file, length, mode, quantity_to_be_checked):
        checked = self.checked

        # checking randomly generated domain names
        if mode == 1:
            for i in range(quantity_to_be_checked):
                random_string = ''.join(random.choice(charset) for i in range(int(length)))

                does_file_already_contain_string = open('available.txt', 'r').read().find(random_string) != -1
                domain_name = '{}{}'.format(random_string, '.eth')
                address = self.ns.address(domain_name) == None
                owner = self.ns.owner(domain_name) == '0x0000000000000000000000000000000000000000'

                if address and owner and not does_file_already_contain_string:
                    with open('available.txt', 'a') as f:
                        f.writelines(f'{domain_name}\n')

                checked += 1
                print('Checked ' + str(checked) + ' domain names!', end='\r')

        # checking alphabetically generated domain names
        elif mode == 2:
            output = []

            for i in range(quantity_to_be_checked):
                s = ""
                for j in range(length):
                    s += charset[i%len(charset)]
                    i //= len(charset)
                output.append(s)

                sorted_string = output[i-1][::-1]

                does_file_already_contain_string = open('available.txt', 'r').read().find(sorted_string) != -1
                domain_name = '{}{}'.format(sorted_string, '.eth')
                address = self.ns.address(domain_name) == None
                owner = self.ns.owner(domain_name) == '0x0000000000000000000000000000000000000000'

                if address and owner and not does_file_already_contain_string:
                    with open('available.txt', 'a') as f:
                        f.writelines(f'{domain_name}\n')

                checked += 1
                print('Checked ' + str(checked) + ' domain names!', end='\r')

        # checking domain names given in a specific file
        elif mode == 3:
            for line in file:
                domain_name = '{}{}'.format(line, eth)
                address = self.ns.address(domain_name)
                owner = self.ns.owner(domain_name) == '0x0000000000000000000000000000000000000000'

                if address == None and owner:
                  with open('available.txt', 'a') as f:
                    f.writelines(f'{domain_name}\n')
                
                checked += 1
                print('Checked ' + str(checked) + ' domain names!', end='\r')

        clear()
        input(f'Done, checked {checked} domain names.')


# setting up the variables
class Setup:
    # variables for mode 1 or 2
    def settings_for_generating(mode):
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

        if select_character_set_option == 1:
          charset = "1","2","3","4","5","6","7","8","9","0"
        elif select_character_set_option == 2:
          charset = "a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"
        elif select_character_set_option == 3:
          charset = "1","2","3","4","5","6","7","8","9","0","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"
        elif select_character_set_option == 4:
          print('You can use numbers from 0 to 9 and lowercase letters. Use the following syntax: 123abc')
          print()

          charset = input('Custom character set >>> ')

        clear()

        quantity_to_be_checked = int(input('How many domain names should be checked? >>> '))

        clear()

        eth = None
        file = None

        Checker.pool.submit(Checker().check(charset, eth, file, length, mode, quantity_to_be_checked))

    # variables for mode 3
    def settings_for_file(mode):
        file_name = input('Enter the name of the file, e.g. file.txt >>> ')

        file = open(file_name,'r').read().splitlines()
        
        clear()
        
        ending = input(f'Do the strings in {file_name} end with ".eth"? Y/N >>> ')
        
        if ending == 'Y' or ending == 'y':
          eth = ''
        elif ending == 'N' or ending == 'n':
          eth = '.eth'
        
        clear()

        charset = None
        length = None
        quantity_to_be_checked = None
        
        Checker.pool.submit(Checker().check(charset, eth, file, length, mode, quantity_to_be_checked))

    # start of the program
    def start():
        clear()

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