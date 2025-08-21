class Stack{
    private:
        static const int MAX = 100;
        char Store[MAX];
        int top;
    public:
        Stack();
        void push (char x);
        char pop();
};