#include <stdlib.h>
#include <stdio.h>

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
  puts("1. malloc");
  puts("2. write to chunk");
  puts("3. do nothing");
  puts("4. quit");
  printf("> ");
}

int allocate(char **ptr)
/* allocate a 256 byte chunk */
{
  puts("Allocating 256 byte chunk...");
  *ptr = malloc(256);
  return 1;
}

/* Useful function pointer! (if I want to change it later) */
void (*func)() = &do_nothing;


int main(int argc, char *argv[])
{
  int chunk_allocated = 0;
  char *chunk, choice;

  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stderr, NULL, _IONBF, 0);
  
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
      if (chunk_allocated) 
	puts("Chunk already allocated.");
      else
	chunk_allocated = allocate(&chunk);
      printf("Chunk address: %p\n", chunk);
      break;
    }
      
    case '2': {
      if (chunk_allocated) 
	gets(chunk);
      else
	puts("You haven't allocated anything yet!");
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

  if (chunk_allocated)
    free(chunk);
  
  return 0;
}
