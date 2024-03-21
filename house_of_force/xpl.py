#!/usr/bin/env python3
from pwn import *
exe = context.binary = ELF('./house_of_force')

def menu(r, choice):
    r.recvuntil(b'> ')
    r.sendline(str(choice).encode())

def leak(r):
    menu(r, 0)
    r.recvuntil(b'something.\n')
    leak = []
    r.recvuntil(b'do_nothing: ')
    leak.append(int(r.recvline().decode(), base=16))
    r.recvuntil(b'do_something: ')
    leak.append(int(r.recvline().decode(), base=16))
    return leak

def malloc(r):
    menu(r, 1)
    r.recvuntil(b'Chunk address: ')
    chunk = int(r.recvline().decode(), base=16)
    return chunk
    
def write(r, data):
    menu(r, 2)
    r.sendline(data)

def do_nothing(r):
    menu(r, 3)
    resp = r.recvline()
    print(f'Do nothing output: \"{resp}\"')

def quit(r):
    menu(r, 4)

io = exe.process()
print(leak(io))
print(malloc(io))
write(io, b'joe')
do_nothing(io)
quit(io)
