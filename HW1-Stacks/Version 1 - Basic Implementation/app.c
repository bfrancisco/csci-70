#include <stdio.h>
#define MAX 100

char Store[MAX];
int top = 0;

void push(char x){
    if (top < MAX )
        Store[top++] = x ;
    else
        printf("Stack full \n") ;
}

char pop(){
    if(top > 0)
        return Store[--top];
    else{
        printf("Stack empty \n") ;
        return 0; /* Make sure something is returned regardless */
    }
}

void application(){
    // push('x');
    // push('y');
    // push('z');
    // char ans = pop();
    // printf("Popped : %c \n", ans);
    // printf(Store);
    // printf("\n");

    push('a');
    push('b');
    push('c');
    push('d');
    push('e');
    for (int i = 0; i < 4; i++) pop();
    push('f');
    push('g');
    
    printf(Store);
    printf("\n");
    
}

int main(){
    application();
    return 0;
}