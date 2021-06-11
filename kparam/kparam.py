#!/usr/bin/env python3

import os
import fileinput
import argparse

grub_fname='/etc/default/grub'
key='GRUB_CMDLINE_LINUX_DEFAULT'

if os.getuid()!=0:
    print('you need to be root!')
    exit(2)

# global data
try:
    grub_file=open(grub_fname,'r')
except OSError:
    print('Can\'t open grub configuration')
    print('Do you want to try to restore from backup?[Y/n]')
    if str(input()).startswith('Y'):
        if os.system('cp ' + grub_fname + '.bak ' + grub_fname):
            print('failed to recover from backup')
            exit(2)
    else:
        print('Abort') 
        exit(2)
    grub_file=open(grub_fname,'r')

params=''
to_replace=''
for line in grub_file.readlines():
    if line.startswith(key):
        params=line[len(key)+1:-1]
        to_replace=str(line)

param_list=params[1:-1].split(sep=' ')
grub_file.close()

# options
def show():
    print(*param_list)
    return

def write_param():
    file=fileinput.FileInput(grub_fname,inplace=True,backup='.bak')
    replacement=key + '="' + ' '.join(param_list) + '"' + "\n"
    for line in file:
        print(line.replace(to_replace,replacement), end='')
    file.close()

def add(arg):
    try: index=param_list.index(arg)
    except ValueError: param_list.append(arg)
    write_param()
    os.system('update-grub')

def delete(arg):
    try: 
        index=param_list.index(arg)
        param_list.pop(index)    
    except ValueError: pass
    write_param()
    os.system('update-grub')
    
# argument parsing
parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument("-s", "--show",action='store_true',help='shows kernel parameter')
group.add_argument("-a", "--add", type=str, help='adds kernel parameter')
group.add_argument("-d", "--delete", type=str, help='removes kernel parameter')
group.add_argument("-r", "--restore",action='store_true',help='restores grub configuration from backup file')
args=parser.parse_args()

if args.add: add(args.add)
elif args.delete: delete(args.delete)
elif args.show: show()
elif args.restore: os.system('cp ' + grub_fname + '.bak ' + grub_fname)
else: print(parser.print_help())
