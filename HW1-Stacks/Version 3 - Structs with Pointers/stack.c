#include <stdio.h>
#include "stack.h"

void initstack(struct stack *s){
    s->top = 0;
}

void push(struct stack *s, char x){
    if (s->top < MAX){
        s->Store[s->top++] = x;
    }else{
        printf("Stack full\n");
    }
}

char pop(struct stack *s){
    if(s->top > 0){
        return s->Store[--s->top];
    }else{
        printf("Stack empty \n");
        return 0; // Make sure something is returned regardless
    }
}