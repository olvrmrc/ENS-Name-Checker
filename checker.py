import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import os
import random
import colorama
import web3
from ens import ENS

node = file = open('node.txt','r').readline()

w3 = web3.Web3(web3.HTTPProvider(node))
ns = ENS.fromWeb3(w3)


def clear():
  os.system('cls')


def check_random_domains():
  checked = 0

  length = int(input(f'Input the lenght of the domain name >>> '))

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

  number = int(input('How many domain names should be checked? >>> '))

  clear()

  for i in range(number):

    random_string = ''.join(random.choice(charset) for i in range(int(length)))
    eth = '.eth'

    all_names = open('available.txt', 'r').read()

    domain_name = '{}{}'.format(random_string, eth)
    address = ns.address(domain_name)

    if address == None and ns.owner(domain_name) == '0x0000000000000000000000000000000000000000' and all_names.find(random_string) == -1:

      with open('available.txt', 'a') as f:
        f.writelines(f'{domain_name}\n')

      color = colorama.Fore.GREEN

    else:

      color = colorama.Fore.RED

    checked = checked + 1

    print('Checked', color + colorama.Style.BRIGHT + str(checked) + colorama.Style.RESET_ALL, 'domain names!', end='\r')

  input('\ndone')


def check_file():

  checked = 0

  file_name = input('Enter the name of the file, e.g. file.txt >>> ')
  file = open(file_name,'r').read().splitlines()
  
  clear()

  ending = input(f'Do the strings in {file_name} end with ".eth"? Y/N >>> ')

  if ending == 'Y' or ending == 'y':
    eth = ''
  elif ending == 'N' or ending == 'n':
    eth = '.eth'

  clear()

  for line in file:
    
    domain_name = '{}{}'.format(line, eth)
    address = ns.address(domain_name)

    if address == None and ns.owner(domain_name) == '0x0000000000000000000000000000000000000000':

      with open('available.txt', 'a') as f:
        f.writelines(f'{domain_name}\n')

      color = colorama.Fore.GREEN

    else:

      color = colorama.Fore.RED

    checked = checked + 1

    print('Checked', color + colorama.Style.BRIGHT + str(checked) + colorama.Style.RESET_ALL, 'domain names!', end='\r')

  input('\ndone')


clear()

print('[1] Check domain names based on random strings with a specific length and character set.')
print('[2] Check domain names given in a specific text file.')
print('Note: In both cases, the available domain names are saved in a file called "available.txt".')
print()

option = int(input('Enter your option >>> '))

if option == 1:
  clear()
  check_random_domains()
elif option == 2:
  clear()
  check_file()