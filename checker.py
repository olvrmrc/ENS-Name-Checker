import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from ens import ENS
import os
import random
import time
from time import sleep
import threading
import web3


checked = 0

lock = threading.Lock()

node = file = open('node.txt','r').readline()

w3 = web3.Web3(web3.HTTPProvider(node))
ns = ENS.fromWeb3(w3)


def clear():
  os.system('cls')


def check_random_domains(charset, length):
  random_string = ''.join(random.choice(charset) for i in range(int(length)))

  does_file_already_contain_string = open('available.txt', 'r').read().find(random_string) == -1

  domain_name = '{}{}'.format(random_string, '.eth')
  address = ns.address(domain_name)

  if address == None and ns.owner(domain_name) == '0x0000000000000000000000000000000000000000' and does_file_already_contain_string:

    with open('available.txt', 'a') as f:
      f.writelines(f'{domain_name}\n')


def generate_sorted_strings(charset, length, sorted_string = ''):

  if length == 0:

    lock.acquire()
    check_sorted_domains(sorted_string)
    lock.release()

  else:

    for letter in sorted(charset):
      generate_sorted_strings(charset, length - 1, sorted_string + letter)


def check_sorted_domains(sorted_string):
  
  does_file_already_contain_string = open('available.txt', 'r').read().find(sorted_string) == -1

  domain_name = '{}{}'.format(sorted_string, '.eth')
  address = ns.address(domain_name)
  
  if address == None and ns.owner(domain_name) == '0x0000000000000000000000000000000000000000' and does_file_already_contain_string:

    with open('available.txt', 'a') as f:
      f.writelines(f'{domain_name}\n')


def check_file(eth, line):
  domain_name = '{}{}'.format(line, eth)
  address = ns.address(domain_name)

  if address == None and ns.owner(domain_name) == '0x0000000000000000000000000000000000000000':

    with open('available.txt', 'a') as f:
      f.writelines(f'{domain_name}\n')


def setup_random_check():
  
  global checked

  length = int(input(f'Input the length of the domain name >>> '))

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

  start_time = time.time()

  sleep(0.000001)

  for i in range(number):

    time_difference = start_time - time.time()
    checks_per_second = checked / time_difference

    checked = checked + 1
    print('Checked ' + str(checked) + ' domain names! Average: ' + str(round(abs(checks_per_second))) + ' per second', end='\r')

    thread = threading.Thread(target=check_random_domains, args=(charset, length))
    thread.start()

  input('\ndone')


def setup_sorted_check():
  
  global checked

  length = int(input(f'Input the length of the domain name >>> '))

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

  start_time = time.time()

  sleep(0.000001)

  for i in range(number):

    time_difference = start_time - time.time()
    checks_per_second = checked / time_difference

    checked = checked + 1
    print('Checked ' + str(checked) + ' domain names! Average: ' + str(round(abs(checks_per_second))) + ' per second', end='\r')

    thread = threading.Thread(target=generate_sorted_strings, args=(charset, length))
    thread.start()
    
  input('\ndone')


def setup_file_check():

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

  start_time = time.time()

  sleep(0.000001)

  for line in file:

    time_difference = start_time - time.time()

    checks_per_second = checked / time_difference

    checked = checked + 1
    print('Checked ' + str(checked) + ' domain names! Average: ' + str(round(abs(checks_per_second))) + ' per second', end='\r')

    thread = threading.Thread(target=check_file, args=(eth, line))
    thread.start()

  input('\ndone')


clear()

print('[1] Check domain names based on random strings with a specific length and character set.')
print('[2] Check domain names based on alphabetically sorted strings with a specific length and character set.')
print('[3] Check domain names given in a specific text file.')
print('Note: In all cases, the available domain names are saved in a file called "available.txt".')
print()

option = int(input('Enter your option >>> '))

if option == 1:
  clear()
  setup_random_check()
elif option == 2:
  clear()
  setup_sorted_check()
elif option == 3:
  clear()
  setup_file_check()