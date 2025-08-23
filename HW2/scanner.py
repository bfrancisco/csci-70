import os

# transition matrix: stores operations for all state->state transitions. 
# format: transition[state][next_state] = {operations}
# operations: add to stream, flush stream, lexical error, unknown error
# states: start | digit | plus | minus | equal1 | equal2 | white | other
TRANSITION = {
    "start" : {
        "start" : [],
        "digit" : ["add"], 
        "plus" : ["add"], 
        "minus" : ["add"], 
        "equal1" : ["add"],
        "equal2" : ["unk_error"],
        "white" : [],
        "other" : ["lex_error"],
    },
    "digit" : {
        "start" : [],
        "digit" : ["add"], 
        "plus" : ["flush", "add"], 
        "minus" : ["flush", "add"], 
        "equal1" : ["flush", "add"],
        "equal2" : ["unk_error"],
        "white" : ["flush"],
        "other" : ["lex_error"],
    },
    "plus" : {
        "start" : [],
        "digit" : ["flush", "add"],
        "plus" : ["flush", "add"], 
        "minus" : ["flush", "add"],
        "equal1" : ["flush", "add"],
        "equal2" : ["unk_error"],
        "white" : ["flush"],
        "other" : ["lex_error"],
    },
    "minus" : {
        "start" : [],
        "digit" : ["flush", "add"],
        "plus" : ["flush", "add"], 
        "minus" : ["flush", "add"],
        "equal1" : ["flush", "add"],
        "equal2" : ["unk_error"],
        "white" : ["flush"],
        "other" : ["lex_error"],
    },
    "equal1" : {
        "start" : ["lex_error"],
        "digit" : ["lex_error"],
        "plus" : ["lex_error"], 
        "minus" : ["lex_error"],
        "equal1" : ["lex_error"],
        "equal2" : ["add"],
        "white" : ["lex_error"],
        "other" : ["lex_error"],
    },
    "equal2" : {
        "start" : [],
        "digit" : ["flush", "add"],
        "plus" : ["flush", "add"], 
        "minus" : ["flush", "add"],
        "equal1" : ["flush", "add"],
        "equal2" : ["unk_error"],
        "white" : ["flush"],
        "other" : ["lex_error"],
    },
    "white" : {
        "start" : [],
        "digit" : ["flush", "add"],
        "plus" : ["flush", "add"], 
        "minus" : ["flush", "add"],
        "equal1" : ["flush"],
        "equal2" : ["unk_error"],
        "white" : [],
        "other" : ["lex_error"],
    },
}

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

def flush_stream(output_stream, ostream_state, output_file_str):
    if not output_stream:
        return
    with open(output_file_str, "a") as f:
        if ostream_state == "digit":
            f.write("NUM " + "".join(output_stream) + "\n")
        elif ostream_state == "plus":
            f.write("PLUS\t+\n")
        elif ostream_state == "minus":
            f.write("MINUS\t-\n")
        elif ostream_state == "equal2":
            f.write("ASSIGN\t==\n")
        output_stream.clear()

def add_to_stream(output_stream, c):
    output_stream.append(c)

def lex_error(error_char, output_file_str):
    with open(output_file_str, "a") as f:
        f.write(f'Lexical Error reading character "{error_char}"\n')

def unknown_error(i, output_file_str):
    with open(output_file_str, "a") as f:
        f.write(f'Error at index {i}')

def run_scanner(input_file, output_file_str):
    output_stream = []      # stores characters that are going to be printed
    ostream_state = ""      # state when output stream was last populated; used for flushing stream
    s = input_file.read() + "\n"  # add "\n" to conveniently flush output stream at the end
    n = len(s)

    state = "start"

    # iterate through characters, do necessary operations per state transition
    for i in range(n):
        next_state = get_next_state(s[i], state)
        # valid transition, do operations of state transition
        for oper in TRANSITION[state][next_state]:
            if oper == "add":
                add_to_stream(output_stream, s[i])
                ostream_state = next_state
            elif oper == "flush":
                flush_stream(output_stream, ostream_state, output_file_str)
            elif oper == "lex_error":
                if state in DEPENDENT_STATES:
                    lex_error(output_stream[-1], output_file_str) # incomplete/invalid token
                else:
                    lex_error(s[i], output_file_str)
                break
            elif oper == "unk_error":
                unknown_error(i, output_file_str)
                break
        state = next_state
        
if __name__ == "__main__":
    # get all txt files with "input" in the filename within the same dir
    input_files = [file_name for file_name in os.listdir() if file_name.endswith('.txt') and 'input' in file_name]

    for input_file_str in input_files:
        with open(input_file_str, 'r') as input_file:
            output_file_str = input_file_str.replace("input", "output")
            open(output_file_str, 'w').close() # create/clear output_file

            run_scanner(input_file, output_file_str)
                    