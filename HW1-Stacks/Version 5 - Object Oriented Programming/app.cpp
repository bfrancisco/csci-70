#include "stack.h"
#include <iostream>

void application(){
    Stack s0,s1;
    s0.push('x');
    s1.push('y');
    s1.push('z');
    char ans = s1.pop();
    std::cout << "Popped: " << ans << "\n";
}

int main(){
    application();
    return 0;
}