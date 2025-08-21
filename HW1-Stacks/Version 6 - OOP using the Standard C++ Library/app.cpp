#include <stack>
#include <iostream>

void application(){
    std::stack<char> s0, s1;
    s0.push('x');
    s1.push('y');
    s1.push('z');
    s0.push('a');
    char ans = s1.top();        // this gets us the top value of the stack
    s1.pop();                   // using top() was necessary because in the stack header, pop only removes the highest element, but does not return it
    std::cout << "Popped from s1: " << ans << "\n";
}

int main(){
    application();
    return 0;
}