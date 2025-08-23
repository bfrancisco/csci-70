import os

# stores operations for all state->state transitions. 
# only stores all valid next states for each state. if the next state is not valid, it should be an error
# format: transition[state][next_state] = {operations}
# operations: add - add_to_stream(), flush - flush_output()
TRANSITION = {
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

# dependent/unfinished states
DEPENDENT_STATES = set(["equal1"])

DIGITS = set([str(x) for x in range(1, 10)])
def is_digit(c):
    return c in DIGITS

def get_next_state(c, cur_state):
    if is_digit(c):
        return "digit"
    elif c == "+":
        return "plus"
    elif c == "-":
        return "minus"
    elif c == "=":
        if cur_state == "equal1":
            return "equal2"
        return "equal1"
    elif c in [" ", "\t", "\n"]:
        return "white"
    return "other"

def print_error(error_char, output_file):
    with open(output_file, "a") as f:
        f.write(f'Lexical Error reading character "{error_char}"\n')

def flush_stream(output_file):
    if not output_stream:
        return
    
    with open(output_file, "a") as f:
        if ostream_state == "digit":
            f.write("NUM " + "".join(output_stream) + "\n")
        elif ostream_state == "plus":
            f.write("PLUS\t+\n")
        elif ostream_state == "minus":
            f.write("MINUS\t-\n")
        elif ostream_state == "equal2":
            f.write("ASSIGN\t==\n")
        output_stream.clear()

def add_to_stream(c):
    output_stream.append(c)

if __name__ == "__main__":
    # Get all txt files with "input" in their name within the same directory
    input_files = [file_name for file_name in os.listdir() if file_name.endswith('.txt') and 'input' in file_name]

    for input_file in input_files:
        with open(input_file, 'r') as file:
            output_file = input_file.replace("input", "output")
            open(output_file, 'w').close() # clear content of output_file if it exists
            
            output_stream = []      # stores characters that are going to be printed
            ostream_state = ""      # state when output stream was last populated; used for flushing stream
            s = file.read() + "\n"  # add "\n" to conveniently flush output stream at the end
            n = len(s)

            state = "start"

            # iterate through characters, do necessary operations per state transition
            for i in range(n):
                next_state = get_next_state(s[i], state)

                # invalid transition.
                if next_state not in TRANSITION[state]:                  
                    # handles dependent/unfinished state.
                    if state in DEPENDENT_STATES:
                        print_error(output_stream[-1], output_file)
                    # handles lexical error for 'other' characters
                    else:
                        flush_stream(output_file)
                        print_error(s[i], output_file)
                    break
                
                # valid transition, do operations of state transition
                for oper in TRANSITION[state][next_state]:
                    if oper == "add":
                        add_to_stream(s[i])
                        ostream_state = next_state
                    elif oper == "flush":
                        flush_stream(output_file)

                state = next_state
        