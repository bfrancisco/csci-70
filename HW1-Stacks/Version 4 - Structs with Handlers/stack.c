#include <stdio.h>
#include "stack.h"

#define MAX_STACKS 10
#define MAX 100

static struct{
    int top;
    char Store [MAX];
}stacks[MAX_STACKS];

void push ( int stacknum , char x ) {
    if(stacknum >= 0 && stacknum < MAX_STACKS){
        if(stacks[stacknum].top < MAX ){
            stacks[stacknum].Store[stacks[stacknum].top++] = x;
        }else{
            printf ("Stack %d full \n", stacknum);
        }
    }else{
    printf ("Invalid stack number %d \n", stacknum);
    }
}

char pop(int stacknum){
    if(stacknum >= 0 && stacknum < MAX_STACKS){
        if(stacks[stacknum].top > 0){
            return stacks[stacknum].Store[--stacks[stacknum].top];
        }else{
            printf("Stack %d empty\n", stacknum);
            return 0;
        }
    }else{
        printf("Invalid stack number %d\n", stacknum);
        return 0;
    }
}

