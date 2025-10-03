import json
import scanner

class Terminal:
    def __init__(self, symbol, token):
        self.symbol = symbol
        self.token = token
    
    def call(self):
        return self.token == self
    
    def get_error_mssg(self):
        return f"Parse Error: {self.token} expected."

class Procedure:
    def __init__(self, inc_mssg="", out_mssg="", error_mssg=""):
        self.transitions = [] # [(Procedure | Terminal)*]
        self.inc_mssg = inc_mssg
        self.out_mssg = out_mssg
        self.error_mssg = error_mssg

    def call(self):
        global cur_token
        global error_done

        if self.inc_mssg: print(self.inc_mssg)

        # LL(1) functionality
        # if there is a matching terminal on the firsts of the immediate transitions -> transition there
        # else, transition to the first-placed transition.
        #   GUARANTEED:
        #       - all productions has at most 1 transition having a nonterminal first      
        #       - all first-placed transition has a nonterminal first
        #   hence, transition_i = 0 if there is no matching terminal symbol       
        transition_i = 0
        for i in len(self.transitions):
            transition = self.transitions[i]
            first = transition[0]
            if isinstance(first, Terminal) and first.token == cur_token:
                transition_i = i
                break
        
        for term_or_proc in self.transitions[transition_i]:
            if term_or_proc.call() == False:
                if not error_done: 
                    print(term_or_proc.get_error_mssg())
                    break
                error_done = True

        if not error_done and self.out_mssg: print(self.out_mssg)
        return error_done==False

class Grammar:
    def __init__(self, grmr_data):
        self.tree = {}
        self.root = grmr_data["root"]
        self.terminals = {}     # terminal name : Terminal instance
        self.procedures = {}    # procedure name : Procedure instance
        self.build_tree(grmr_data)
    
    def build_tree(self, grmr_data):
        # create Terminal instances
        for terminal in grmr_data["terminals"]:
            self.terminals[terminal] = Terminal(terminal.symbol, terminal.token)
        
        # create Procedure isntances
        for prod in grmr_data.productions:
            self.procedures[prod] = Procedure()
            
        

def initialize_grammar():
    global cur_token
    global error_done

    cur_token = scanner.gettoken()
    error_done = False
    grammar = Grammar()
    with open('grammar.json', 'r') as file:
        grmr_data = json.load(file)


if __name__ == "__main__":
    initialize_grammar()
    