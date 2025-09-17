class Transition:
    def __init__(self, to_state: int, is_other: bool = False, with_pushback = False, token=""):
        self.is_other = is_other
        self.to_state = to_state
        self.with_pushback = with_pushback

class State:
    def __init__(self, description, error_mssg="no error", transitions={}):
        self.description = description
        self.error_mssg = error_mssg

States = [None for i in range(17)]
LETTERS = "abcdefghijklmnopqrstuvwxyz"
DIGITS = "0123456789"

def add_transition(state_i, to_state: int, char : str = "", is_other: bool = False, with_pushback = False, token : str = ""):
    States[0].transitions[char] = Transition(to_state, is_other, with_pushback, token)

def initialize():
    States[0] = State(description="Initial state", error_mssg="Lexical Error: Illegal character/character sequence")
    add_transition(state_i=0, char='\n', to_state=0)
    add_transition(state_i=0, char='\t', to_state=0)
    add_transition(state_i=0, char=' ', to_state=0)
    add_transition(state_i=0, char='(', to_state=0, token="left_paren")
    add_transition(state_i=0, char=')', to_state=0, token="right_paren")
    add_transition(state_i=0, char='+', to_state=0, token="plus")
    add_transition(state_i=0, char='-', to_state=0, token="minus")
    add_transition(state_i=0, char='=', to_state=0, token="equal")
    add_transition(state_i=0, char=':', to_state=0, token="colon")
    add_transition(state_i=0, char=',', to_state=0, token="comma")
    add_transition(state_i=0, char='EOF', to_state=0, token="end_of_file")
    add_transition(state_i=0, char='/', to_state=1)
    for letter in LETTERS:  add_transition(state_i=0, char=letter, to_state=3)
    add_transition(state_i=0, char='_', to_state=3)
    for digit in DIGITS:    add_transition(state_i=0, char=digit, to_state=4)
    add_transition(state_i=0, char='"', to_state=10)
    add_transition(state_i=0, char=':', to_state=11)
    add_transition(state_i=0, char='*', to_state=12)
    add_transition(state_i=0, char='<', to_state=13)
    add_transition(state_i=0, char='>', to_state=14)
    add_transition(state_i=0, char='!', to_state=15)
    add_transition(state_i=0, is_other=True, to_state=-1)

    States[1] = State("First slash character for divide and comment.")
    add_transition(state_i=1, char='/', to_state=2)
    add_transition(state_i=1, is_other=True, to_state=0, token="divide", with_pushback=True)

    States[2] = State("Comement content")
    add_transition(state_i=2, char='\n', to_state=0)
    add_transition(state_i=2, is_other=True, to_state=2)

    States[3] = State("Identifier character")
    for letter in LETTERS:  add_transition(state_i=3, char=letter, to_state=3)
    for digit in DIGITS:    add_transition(state_i=3, char=digit, to_state=3)
    add_transition(state_i=3, char='_', to_state=3)

    States[4] = State("Number: first digitdigit*")
    for digit in DIGITS:    add_transition(state_i=4, char=digit, to_state=4)
    add_transition(state_i=4, is_other=True, to_state=0, token="number", with_pushback=True)

    States[5] = State("Number: post dot")
    for digit in DIGITS:    add_transition(state_i=5, char=digit, to_state=9)
    add_transition(state_i=5, is_other=True, to_state=-1)

def run(input_file):
    for line in input_file.readlines():
        print(":", end='')
        for c in line:
            print("\\n" if c=="\n" else c, end='')
        print()   

    return ""


# for testing
if __name__ == "__main__":
    FILE = "input.txt"
    with open(FILE, 'r') as input_file:
        run(input_file)

