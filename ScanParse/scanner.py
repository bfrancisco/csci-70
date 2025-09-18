class Transition:
    def __init__(self, next_state:int, is_other:bool = False, with_pushback = False, token:str = "", to_error:bool = False):
        self.is_other = is_other
        self.next_state = next_state
        self.with_pushback = with_pushback
        self.token = token
        self.to_error = to_error

class State:
    def __init__(self, description:str, error_mssg:str = "Unkown Error"):
        self.description = description
        self.error_mssg = error_mssg
        self.transitions = {}
    
    def get_transition(self, char:str):
        return self.transitions[""] if char not in self.transitions else self.transitions[char]


NO_OF_STATES = 16
States = [None for i in range(NO_OF_STATES)]
LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
DIGITS = "0123456789"
KEYWORDS = ["PRINT", "IF", "ELSE", "ENDIF", "SQRT", "AND", "OR", "NOT"]

def add_transition(state_i, next_state:int, char:str = "", is_other:bool = False, with_pushback:bool = False, token:str = "", to_error:str = False):
    States[state_i].transitions[char] = Transition(next_state=next_state, is_other=is_other, with_pushback=with_pushback, token=token, to_error=to_error)

def initialize_DFA():
    States[0] = State(description="Initial state", error_mssg="Illegal character/character sequence")
    add_transition(state_i=0, char='\n', next_state=0)
    add_transition(state_i=0, char='\t', next_state=0)
    add_transition(state_i=0, char=' ', next_state=0)
    add_transition(state_i=0, char='(', next_state=0, token="LeftParen")
    add_transition(state_i=0, char=')', next_state=0, token="RightParen")
    add_transition(state_i=0, char='+', next_state=0, token="Plus")
    add_transition(state_i=0, char='-', next_state=0, token="Minus")
    add_transition(state_i=0, char='=', next_state=0, token="Equal")
    add_transition(state_i=0, char=';', next_state=0, token="Semicolon")
    add_transition(state_i=0, char=',', next_state=0, token="Comma")
    add_transition(state_i=0, char='EOF', next_state=0, token="EndofFile")
    add_transition(state_i=0, char='/', next_state=1)
    for letter in LETTERS:  add_transition(state_i=0, char=letter, next_state=3)
    add_transition(state_i=0, char='_', next_state=3)
    for digit in DIGITS:    add_transition(state_i=0, char=digit, next_state=4)
    add_transition(state_i=0, char='"', next_state=10)
    add_transition(state_i=0, char=':', next_state=11)
    add_transition(state_i=0, char='*', next_state=12)
    add_transition(state_i=0, char='<', next_state=13)
    add_transition(state_i=0, char='>', next_state=14)
    add_transition(state_i=0, char='!', next_state=15)
    add_transition(state_i=0, is_other=True, next_state=0, to_error=True)

    States[1] = State("Slash")
    add_transition(state_i=1, char='/', next_state=2)
    add_transition(state_i=1, is_other=True, next_state=0, token="Divide", with_pushback=True)

    States[2] = State("Comement content")
    add_transition(state_i=2, char='\n', next_state=0)
    add_transition(state_i=2, is_other=True, next_state=2)

    States[3] = State("Identifier character")
    for letter in LETTERS:  add_transition(state_i=3, char=letter, next_state=3)
    for digit in DIGITS:    add_transition(state_i=3, char=digit, next_state=3)
    add_transition(state_i=3, char='_', next_state=3)
    add_transition(state_i=3, is_other=True, next_state=0, token="Identifier", with_pushback=True)

    States[4] = State("Number: Integer")
    for digit in DIGITS:    add_transition(state_i=4, char=digit, next_state=4)
    add_transition(state_i=4, char='.', next_state=5)
    add_transition(state_i=4, char='e', next_state=6)
    add_transition(state_i=4, char='E', next_state=6)
    add_transition(state_i=4, is_other=True, next_state=0, token="Number", with_pushback=True)

    States[5] = State("Number: ... dot", error_mssg="Invalid number format")
    for digit in DIGITS:    add_transition(state_i=5, char=digit, next_state=9)
    add_transition(state_i=5, is_other=True, next_state=0, to_error=True)

    States[6] = State("Number: ... e", error_mssg="Invalid number format")
    for digit in DIGITS:    add_transition(state_i=6, char=digit, next_state=8)
    add_transition(state_i=6, char='+', next_state=7)
    add_transition(state_i=6, char='-', next_state=7)
    add_transition(state_i=6, is_other=True, next_state=0, to_error=True)

    States[7] = State("Number: ... +-", error_mssg="Invalid number format")
    for digit in DIGITS:    add_transition(state_i=7, char=digit, next_state=8)
    add_transition(state_i=7, is_other=True, next_state=0, to_error=True)

    States[8] = State("Number: (Float + Exponent) | Exponent")
    for digit in DIGITS:    add_transition(state_i=8, char=digit, next_state=8)
    add_transition(state_i=8, is_other=True, next_state=0, token="Number", with_pushback=True)

    States[9] = State("Number: Float")
    for digit in DIGITS:    add_transition(state_i=9, char=digit, next_state=9)
    add_transition(state_i=9, char='e', next_state=6)
    add_transition(state_i=9, char='E', next_state=6)
    add_transition(state_i=9, is_other=True, next_state=0, token="Number", with_pushback=True)

    States[10] = State("String", error_mssg="Unterminated string")
    add_transition(state_i=10, char='"', next_state=0, token="String")
    add_transition(state_i=10, is_other=True, next_state=10)
    add_transition(state_i=10, char='\n', next_state=0, to_error=True)
    
    States[11] = State("Colon")
    add_transition(state_i=11, char='=', next_state=0, token="Assign")
    add_transition(state_i=11, is_other=True, next_state=0, token="Colon", with_pushback=True)

    States[12] = State("Asterisk")
    add_transition(state_i=12, char='*', next_state=0, token="Raise")
    add_transition(state_i=12, is_other=True, next_state=0, token="Multiply", with_pushback=True)

    States[13] = State("Less than")
    add_transition(state_i=13, char='=', next_state=0, token="LTEqual")
    add_transition(state_i=13, is_other=True, next_state=0, token="LessThan", with_pushback=True)

    States[14] = State("Greater than")
    add_transition(state_i=14, char='=', next_state=0, token="GTEqual")
    add_transition(state_i=14, is_other=True, next_state=0, token="GreaterThan", with_pushback=True)

    States[15] = State("Exclamation Point", error_mssg="Illegal character/character sequence")
    add_transition(state_i=15, char='=', next_state=0, token="NotEqual")
    add_transition(state_i=15, is_other=True, next_state=0, to_error=True)


def run(input_file):
    initialize_DFA()
    input_stream = "".join(input_file.readlines())

    i = 0
    cur_state = 0
    buffer = []
    while i <= len(input_stream):
        char = 'EOF' if i==len(input_stream) else input_stream[i]
        
        trnstn_data = States[cur_state].get_transition(char)
        
        if cur_state == 0:
            buffer.clear()
        buffer.append(char)
        if trnstn_data.with_pushback:
            i -= 1
            buffer.pop()

        token = trnstn_data.token
        if token == "Identifier" and "".join(buffer) in KEYWORDS:
            token = "".join(buffer).capitalize()
        
        if token:
            print(f'{token:<17}{"".join(buffer) if token != "EndofFile" else ""}')
            buffer.clear()

        elif trnstn_data.to_error:
            print(f'Lexical Error: {States[cur_state].error_mssg}')
            print("Error")
            buffer.clear()

        # print(f"CUR CHAR:\t{char}")
        # print(f"CUR STATE:\t{cur_state}\t{States[cur_state].description}")
        # print(f"NEXT STATE:\t{trnstn_data.next_state}\t{States[trnstn_data.next_state].description}")
        # print(f"Buffer:\t{buffer}")
        # print(f"TOKEN: {token}")
        # print(f"error: {trnstn_data.to_error}")
        # print()

        cur_state = trnstn_data.next_state
        i += 1


    return ""


# for testing
if __name__ == "__main__":
    FILE = "input.txt"
    with open(FILE, 'r') as input_file:
        run(input_file)
