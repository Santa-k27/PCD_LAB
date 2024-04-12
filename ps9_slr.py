'''
    To-Do:
    NOTE: If a table has 2 entry, the latest entry will be filled replacing the previously stored entry as conflicts are not handled
    NOTE: Check whether parsing works correctly
'''

from collections import deque

def stateExists(states_list, item_set):
    for state in states_list:
        if state.item_set==item_set:
            return True
    return False
        
def findLabel(states_list, item_set):
    for state in states_list:
        if state.item_set==item_set:
            return state.label

class SLR_state:
    def __init__(self, label, item_set):
        self.label = label
        self.item_set = item_set    

    def __eq__(self, other):
        return set(self.item_set) == other

class LR0_item:
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def __eq__(self, other):
        return self.lhs == other.lhs and self.rhs == other.rhs
    
    def __hash__(self):
        return hash((self.lhs, self.rhs))
    
class Grammar:
    def __init__(self, non_terminals, terminals, start_symbol, productions, aug):
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.start_symbol = start_symbol
        self.productions = productions
        self.aug_start_symbol = aug
        self.first_dict = dict()
        self.follow_dict = dict()

    # NOTE: Find first from last level production to first level production (for ease)
    def findFirst(self, symbol):
        if symbol in self.terminals:
            return {symbol}
        else:
            res = set()

            for production in self.productions[symbol]:
                # If first character of a production is terminal, then nothing in that production can contribute to FIRST
                if production[0] in self.terminals:
                    res.add(production[0])

                else:
                    if symbol==production[0] and symbol not in self.first_dict.keys():
                        continue
                    index=0
                    # Until the first occuring NT has '?' in it's production, add the FIRST of NT to res
                    while index<len(production) and production[index] in self.non_terminals:
                        if '?' in self.first_dict[production[index]]:
                            res.add(self.first_dict[production[index]])
                            index += 1

                            # If an NT has epsilon in its first and is followed by a terminal, then add that terminal and stop
                            if production[index] in self.non_terminals:
                                res.add(production[index])
                                break
                        else:
                            res.update(self.first_dict[production[index]])
                            break

                    if index<len(production) and production[index] in self.terminals:
                        res.update(self.first_dict[production[index]])
            
            #self.first_dict[symbol] = res
            return res

    # NOTE: Find follow only after FIRST has been found for all NT
    def findFollow(self, non_terminal):
        res = set()

        if non_terminal == self.start_symbol:
            res.add('$')

        for nt in self.productions.keys():
            for production in self.productions[nt]:
                if non_terminal in production:
                    # Finding all positions where non_terminal occurs in RHS
                    positions = [i for i,c in enumerate(production) if c==non_terminal]

                    # non_terminal followed by nothing
                    if positions==[len(production)-1]:
                        # Checking whether LHS and input symbol to FOLLOW function() is same
                        if non_terminal == nt:
                            return res
                        else:
                            res.update(self.follow_dict[nt])

                    for pos in positions:
                        index = pos + 1
                        
                        while index<len(production):
                            # If NT followed by terminal
                            if production[index] in self.terminals:
                                res.add(production[index])
                                break
                            # NT followed by another NT
                            elif production[index] in self.non_terminals:
                                first_of_next_nt = self.first_dict[production[index]]
                                res.update({elem for elem in first_of_next_nt if elem != '?'})
                                
                                if '?' in first_of_next_nt:
                                    index += 1
                                else:
                                    break
                        
                        if index==len(production):
                            res.update(self.follow_dict[nt])

        #self.follow_dict[non_terminal] = res
        return res
    

    def findClosure(self, items_set: set):
        old = set()
        for item in items_set:
            old.add(LR0_item(item.lhs, item.rhs))
        res = set()

        # Every item in I is in CLOSURE(I)
        for item in old:
            res.add(item)
        
        while len(old):
            item = old.pop()
            if '.' in item.rhs:
                dot_index = item.rhs.index('.')
                if dot_index + 1 < len(item.rhs) and item.rhs[dot_index + 1] in self.productions.keys():
                    for prod in self.productions[item.rhs[dot_index + 1]]:
                        new_item = LR0_item(item.rhs[dot_index + 1], '.'+prod)
                        res.add(new_item)

                        if prod[0]==item.rhs[dot_index + 1]:
                            continue
                        else:
                            old.add(new_item)
                        
        return res

    def findGoto(self, kernel):
        kernel_copy = set()
        for item in kernel:
            kernel_copy.add(LR0_item(item.lhs, item.rhs))
        dot_moved_kernel = set()

        for item in kernel_copy:
            dot_index = item.rhs.index('.')
            # After moving, dot is at last
            if dot_index==len(item.rhs)-2:
                item.rhs = item.rhs[:dot_index] + item.rhs[dot_index+1] + '.'
            # After moving, dot is in between
            else:
                item.rhs = item.rhs[:dot_index] + item.rhs[dot_index+1] + '.' + item.rhs[dot_index+2:]
            dot_moved_kernel.add(item)

        return self.findClosure(dot_moved_kernel)


start_sym = input('Enter start symbol: ')
non_terms = list(input('Enter space separated NT: ').split())
terms = input('Enter space-separated terminals (use ? for epsilon): ').split()

prods = {}

print('Enter space-separated RHS of each NT')
for nt in non_terms:
    prods[nt] = list(input(nt + '-> ').split())

# Augmented grammar. Assumption: Augmented NT is 2 after the NT
augmented_start_sym = chr(ord(start_sym) + 2)
G = Grammar(non_terms, terms, start_sym, prods, augmented_start_sym)

# Finding FIRST for terminals first
for terminal in G.terminals:
    res = G.findFirst(terminal)
    G.first_dict[terminal] = res # Storing back to FIRST dictionary for future reference by other FIRST calculations

# Finding FIRST for NT in reverse
for nt in reversed(G.non_terminals):
    res = G.findFirst(nt)
    G.first_dict[nt] = res

# Finding FOLLOW for NT in forward
for nt in G.non_terminals:
    res = G.findFollow(nt)
    G.follow_dict[nt] = res

print('FIRST table :-')
print(G.first_dict)

print('FOLLOW table :-')
print(G.follow_dict)


G.non_terminals.append(augmented_start_sym)
G.first_dict[augmented_start_sym] = set(G.first_dict[G.start_symbol])
G.follow_dict[augmented_start_sym] = set(G.follow_dict[G.start_symbol])
G.productions[augmented_start_sym] = start_sym

# Prereqs for states processing
states_queue = deque()
states_list = []
slr_table = {}
goto_table = {}

# State construction starts here
initial_item = LR0_item(G.aug_start_symbol, '.' + G.start_symbol)
initial_set = set()
initial_set.add(initial_item)

initial_closure = G.findClosure(initial_set)
initial_state = SLR_state('0', initial_closure)
states_queue.append(initial_state)
states_list.append(initial_state)

while states_queue:
    state = states_queue.popleft()

    # SLR table filling
    for item in state.item_set:
        if item.rhs[-1]=='.':
            # SLR table filling rule 3
            if item.lhs==G.aug_start_symbol and item.rhs==G.start_symbol + '.':
                slr_table[(state.label, '$')] = 'Accept'
            # SLR table filling rule 2
            else:
                for term in G.follow_dict[item.lhs]:
                    slr_table[(state.label, term)] = 'Reduce ' + item.lhs + ' -> ' + item.rhs[:-1]

    # Finding NT GOTOs
    for nt in G.non_terminals:
        kernel = set()
        for item in state.item_set:
            dot_index = item.rhs.index('.')
            if dot_index+1<len(item.rhs) and item.rhs[dot_index+1]==nt:
                kernel.add(item)

        if not len(kernel):
            continue
        goto = G.findGoto(kernel)

        next_label = ''

        if stateExists(states_list, goto):
            next_label = findLabel(states_list, goto)
        else:
            next_label = str(int(states_list[-1].label) + 1)
            new_state = SLR_state(next_label, goto)
            states_list.append(new_state)
            states_queue.append(new_state)

        goto_table[(state.label, nt)] = next_label

        # SLR table filling rule 4
        slr_table[(state.label, nt)] = next_label

    # Finding terminal GOTOs
    for t in G.terminals:
        kernel = set()
        for item in state.item_set:
            dot_index = item.rhs.index('.')
            if dot_index+1<len(item.rhs) and item.rhs[dot_index+1]==t:
                kernel.add(item)

        if not len(kernel):
            continue
        goto = G.findGoto(kernel)

        next_label = ''

        if stateExists(states_list, goto):
            next_label = findLabel(states_list, goto)
        else:
            next_label = str(int(states_list[-1].label) + 1)
            new_state = SLR_state(next_label, goto)
            states_list.append(new_state)
            states_queue.append(new_state)

        goto_table[(state.label, t)] = next_label

        # SLR table filling rule 1
        slr_table[(state.label, t)] = 'S ' + next_label

grammar_symbols = [term for term in G.terminals]
grammar_symbols.extend(G.non_terminals)
grammar_symbols.remove(G.aug_start_symbol)
print('Grammar symbols: ', grammar_symbols)

# Filling invalid entries in slr table
for state in range(int(states_list[-1].label)+1):
    for symbol in grammar_symbols:
        if (str(state), symbol) not in slr_table.keys():
            slr_table[(str(state), symbol)] = '-'

# Printing the table
print('SLR parser table :-')
row_headers = [str(key) for key in range(int(states_list[-1].label)+1)]
col_headers = grammar_symbols

print('\t' + '\t'.join(col_headers))
for row_header in row_headers:
    print(row_header, end='\t')
    for col_header in col_headers:
        cell_value = slr_table.get((str(row_header), col_header), '')
        print(cell_value, end='\t')
    print()

# Parsing the input string
stack = '$' + str(0)
input_str = input('Enter input string to parse: ')
str_index = 0

while True:
    # Accept case
    if input_str[str_index]=='$' and stack[-1]=='1':
        print('Stack: ', stack, end='\t')
        print('Buffer: ', input_str[str_index:], end='\t')
        print('ACCEPT')
        break

    # Table lookup case
    if stack[-1] in row_headers and input_str[str_index] in G.terminals:
        print('Stack: ', stack, end='\t')
        print('Buffer: ', input_str[str_index:], end='\t')

        if slr_table[(stack[-1], input_str[str_index])] == '-':
            print('ERROR !')
            break

        # SHIFT case
        elif slr_table[(stack[-1], input_str[str_index])].split()[0] == 'S':
            print(slr_table[(stack[-1], input_str[str_index])])
            next_state = slr_table[(stack[-1], input_str[str_index])].split()[1]
            stack += input_str[str_index]
            stack += next_state
            str_index += 1

        # REDUCE case
        else:
            # Matching stack content with production rhs and replacing
            print(slr_table[(stack[-1], input_str[str_index])])
            # Leaving the last character 
            next_lhs = slr_table[(stack[-1], input_str[str_index])].split()[1]
            rhs_len = len(slr_table[(stack[-1], input_str[str_index])].split()[3])
            stack = stack[:-1]
            stack = stack[:-((2*rhs_len) - 1)]
            stack += next_lhs

    # Once reduction is done, check for pushing new state number to stack
    elif stack[-1] in grammar_symbols and stack[-2] in row_headers:
        print('Stack: ', stack, end='\t')
        print('Buffer: ', input_str[str_index:], end='\t')
        print(slr_table[(stack[-2], stack[-1])])

        stack += slr_table[(stack[-2], stack[-1])]

    else:
        print('ERROR !')
        break
