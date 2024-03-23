# Heap Exploitation
This repo has two binaries that are intended to teach the House of Force and Fastbin Dup exploits for Capture the Flag (CTF).

## House of Force
The House of Force attack involves exploiting a heap overflow to overwrite the size of the topmost chunk (aka wilderness). From here, the user has to be able to allocate a second chunk of a user-specified amount. Since `malloc` will see that the user has a large amount of memory left to allocate, our next allocation will allow us to advance where the topmost chunk is. A subsequent allocation and write gives us an arbitrary write. There are some good resources on the House of Force [here](https://mohamed-fakroud.gitbook.io/red-teamings-dojo/binary-exploitation/heap-house-of-force), [here](https://ctf-wiki.mahaloz.re/pwn/linux/glibc-heap/house_of_force/), [here](https://heap-exploitation.dhavalkapil.com/attacks/house_of_force), and [here](https://trustie.medium.com/shakti-ctf-house-of-force-97d656a70886). [This](https://github.com/ctf-wiki/ctf-challenges/tree/master/pwn/heap/house-of-force) repo also has a few examples.

## Fastbin Dup
The Fastbin Dup attack involves using a double free to corrupt the linked list in the fastbin. Writing to a double free'd pointer allow us to manipulate the pointer in the fasbin list, giving us an arbitrary write. Some good writeups are [here](https://github.com/Mithreindeir/ctf-writeups/blob/master/pico-ctf2018/contacts/ReadMe.md), and [here](https://trustie.medium.com/glacierctf-2022-heap-fastbin-dup-78e7b1224715).

## General Heap Resources:
- Read up on malloc [here](https://sploitfun.wordpress.com/2015/02/10/understanding-glibc-malloc/).
- [Heap](https://guyinatuxedo.github.io/25-heap/index.html) guyinatuxedo book, their website is a great CTF reference in general.
- My favorite heap implementation articles [here](https://azeria-labs.com/heap-exploitation-part-1-understanding-the-glibc-heap-implementation/).