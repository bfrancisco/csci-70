#include <stdio.h>
#include "stack.h"
#define MAX 100

static char Store[MAX];
int top = 0;

void push(char x){
    if(top < MAX){
        Store[top++] = x;
    }else{
        printf("Stack full \n");
    }
}

char pop(){
    if(top > 0){
        return Store[--top];
    }else{
        printf("Stack empty \n");
        return 0; //Make sure something is returned regardless
    }
}
