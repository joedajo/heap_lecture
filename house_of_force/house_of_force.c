#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define CHUNK_SIZE 20

typedef struct
{
  int allocated;
  char *ptr;
} chunk;

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
  printf("4. quit\n");
  printf("> ");
}

void allocate(chunk *chunks)
/* allocate a 256 byte chunk */
{
  char tmp[50];
  int ret, index;
  int chunk_size = 0;

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
  
  printf("What size do you want your chunk to be?\n> ");
  fgets(tmp, 50, stdin);
  ret = sscanf(tmp, "%d", &chunk_size);

  if (ret != 1) {
    printf("sscanf failure.\n");
    return;
  }

  chunks[index].allocated = 1;
  chunks[index].ptr = malloc(chunk_size);

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

  if (!chunks[index].allocated) {
    printf("Chunk not allocated yet.\n");
    return;
  }
  
  printf("Now enter the data you want in your chunk.\n> ");
  fgets(chunks[index].ptr, 100, stdin);
}

/* Useful function pointer! (if I want to change it later) */
void (*func)() = &do_nothing;

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
      puts("Exiting...");
      break;
    }

    default: {
      puts("Invalid choice. Try again.");
    }
      
    } // end switch
  } while (choice != '4');

  for (i=0; i<3; i++)
    if (chunks[i].allocated)
      free(chunks[i].ptr);

  return 0;
}
