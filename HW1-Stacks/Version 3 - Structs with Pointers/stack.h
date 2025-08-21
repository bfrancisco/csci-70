#define MAX 100

struct stack{
    int top;
    char Store[MAX];
};

void initstack(struct stack *s);
void push(struct stack *s, char x);
char pop(struct stack *s);
