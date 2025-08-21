# stores operations for all state->state transitions. 
# only stores all valid next states for each state. if the next state is not valid, it should be an error
# format: transition[state][next_state] = {operations}
# operations: add - add_to_stream(), flush - flush_output()
transition = {
    "start" : {
        "digit" : ["add"], 
        "plus" : ["add"], 
        "minus" : ["add"], 
        "equal1" : ["add"],
        "white" : [],
    },
    "digit" : {
        "digit" : ["add"], 
        "plus" : ["flush", "add"], 
        "minus" : ["flush", "add"], 
        "equal1" : ["flush", "add"],
        "white" : ["flush"],
    },
    "plus" : {
        "digit" : ["flush", "add"],
        "plus" : ["flush", "add"], 
        "minus" : ["flush", "add"],
        "equal1" : ["flush", "add"],
        "white" : ["flush"],
    },
    "minus" : {
        "digit" : ["flush", "add"],
        "plus" : ["flush", "add"], 
        "minus" : ["flush", "add"],
        "equal1" : ["flush", "add"],
        "white" : ["flush"],
    },
    "equal1" : {
        "equal2" : ["add"],
    },
    "equal2" : {
        "digit" : ["flush", "add"],
        "plus" : ["flush", "add"], 
        "minus" : ["flush", "add"],
        "white" : ["flush"],
        "equal1" : ["flush", "add"],
    },
    "white" : {
        "digit" : ["flush", "add"],
        "plus" : ["flush", "add"], 
        "minus" : ["flush", "add"],
        "equal1" : ["flush"],
        "white" : [],
    },
}

DIGITS = set([str(x) for x in range(1, 10)])
def isDigit(c):
    return c in DIGITS

def getState(c):
    "returns state name"
    if isDigit(c):
        return "digit"
    elif c == "+":
        return "plus"
    elif c == "-":
        return "minus"
    elif c == "=":
        if output_stream and output_stream[-1] == '=':
            return "equal2"
        return "equal1"
    elif c in [" ", "\t", "\n"]:
        return "white"
    return "other"

def print_error(error_char):
    print(f'Lexical Error reading character "{error_char}"')

def flush_stream():
    if not output_stream:
        return
    if ostream_state == "digit":
        print("NUM " + "".join(output_stream))
    elif ostream_state == "plus":
        print("PLUS\t+")
    elif ostream_state == "minus":
        print("MINUS\t-")
    elif ostream_state == "equal2":
        print("ASSIGN\t==")
    output_stream.clear()

def add_to_stream(c):
    output_stream.append(c)

if __name__ == "__main__":
    output_stream = []      # stores characters that are going to be printed
    ostream_state = ""      # state when ouput stream was last populated; used for flushing stream
    s = input() + "\n"      # add "\n" to output stream at the end
    n = len(s)

    state = "start"

    # iterate through characters, do necessary operations per state transition
    for i in range(n):
        next_state = getState(s[i])
        
        # invalid transition
        if next_state not in transition[state]:
            flush_stream()
            print_error(s[i])
            break
        
        for oper in transition[state][next_state]:
            if oper == "add":
                add_to_stream(s[i])
                ostream_state = next_state
            elif oper == "flush":
                flush_stream()
        
        state = next_state
