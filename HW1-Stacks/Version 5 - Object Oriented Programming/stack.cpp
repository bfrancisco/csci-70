#include "stack.h"
#include <iostream>

Stack::Stack():top(0){}

void Stack::push(char x){
    if(top < MAX){
        Store[top++] = x;
    }else{
        std::cout << "Stack full \n";
    }
}

char Stack::pop(){
    if(top > 0){
        return Store[--top];
    }else{
        std::cout << "Stack empty \n";
        return 0;
    }
}