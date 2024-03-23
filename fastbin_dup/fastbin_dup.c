#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define CHUNK_SIZE 30

typedef struct
{
  int allocated;
  char *ptr;
} chunk;

void execute(char *cmd)
{
  system(cmd);
}

void init()
{
  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stderr, NULL, _IONBF, 0);
}

void do_nothing()
{
  puts("I literally do nothing.");
}

void do_something()
/* This would be cool to execute... */
{
  puts("WOAH... how did you do that??");
}

void print_menu()
{
  printf("1. malloc\n");
  printf("2. write to chunk\n");
  printf("3. do nothing\n");
  printf("4. free\n");
  printf("5. quit\n");
  printf("> ");
}

void allocate(chunk *chunks)
/* allocate a 256 byte chunk */
{
  char tmp[50];
  int ret, index;

  printf("Which chunk would you like to allocate?\n> ");
  fgets(tmp, 50, stdin);
  ret = sscanf(tmp, "%d", &index);  
  if (ret != 1) {
    printf("sscanf failure.\n");
    return;
  }

  if (index < 0 || index > 2) {
    printf("You can't write there.\n");
    return;
  }
  
  if (chunks[index].allocated) {
    printf("Chunks[%d] already allocated.\n", index);
    return;
  }
  
  chunks[index].allocated = 1;
  chunks[index].ptr = malloc(CHUNK_SIZE);

  printf("Chunk allocated with address: %p\n", chunks[index].ptr);
  return;
}

void write_chunk(chunk *chunks)
{
  char tmp[50];
  int ret, index;
  
  printf("Which chunk would you like to write to?\n> ");
  fgets(tmp, 50, stdin);
  ret = sscanf(tmp, "%d", &index);  
  if (ret != 1) {
    printf("sscanf failure.\n");
    return;
  }

  if (index < 0 || index > 2) {
    printf("You can't write there.\n");
    return;
  }

  printf("Now enter the data you want in your chunk.\n> ");
  fgets(chunks[index].ptr, CHUNK_SIZE-1, stdin);
}

void free_chunk(chunk *chunks)
{
  char tmp[50];
  int ret, index;
  
  printf("Which chunk would you like to free?\n> ");
  fgets(tmp, 50, stdin);
  ret = sscanf(tmp, "%d", &index);  
  if (ret != 1) {
    printf("sscanf failure.\n");
    return;
  }

  if (index < 0 || index > 2) {
    printf("You can't free there.\n");
    return;
  }

  chunks[index].allocated = 0;
  free(chunks[index].ptr);
}

/* Useful function pointer! (if I want to change it later) */
long long int tmp0 = 0x0000004f0000003f;
long long int tmp1 = 0x0000004f0000003f;
long long int tmp2 = 0x0000004f0000003f;
void (*func)() = &do_nothing;
long long int tmp3 = 0x0000004f0000004f;

int main(int argc, char *argv[])
{
  chunk chunks[3];
  char choice;
  int i;
  
  init();
  for (i=0; i<3; i++)
    memset(&chunks[i], 0, sizeof chunks[i]);
  
  puts("Hello, welcome to the malloc simulation.\n");
  puts("Please choose an option below.\n");

  do {
    print_menu();
    choice = getchar();
    getchar(); // clear newline
    switch (choice) {
    case '0': {
      puts("\nHmm... you weren't supposed to find this.");
      puts("I guess I'll give you something.");
      printf("do_nothing: %p\ndo_something: %p\n\n", &do_nothing, &do_something);
      break;
    }

    case '1': {
      allocate(chunks);
      break;
    }
      
    case '2': {
      write_chunk(chunks);
      break;
    }

    case '3': {
      func();
      break;
    }

    case '4': {
      free_chunk(chunks);
      break;
    }
      
    case '5': {
      puts("Exiting...");
      break;
    }

    default: {
      puts("Invalid choice. Try again.");
    }
      
    } // end switch
  } while (choice != '5');

  for (i=0; i<3; i++)
    if (chunks[i].allocated)
      free(chunks[i].ptr);
      
  return 0;
}
