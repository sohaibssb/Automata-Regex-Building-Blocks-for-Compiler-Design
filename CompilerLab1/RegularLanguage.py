'''
Task - 5:
takes a regular expression as input
and converts it directly to a DFA using 
the subset construction algorithm, 
followed by DFA minimization using the 
algorithm based on pairs of distinguishable states:
'''
#Example a*b|c+d

import re 

#Define the regular expression input
regex = input("\nВведите регулярное выражение:\n")
#Define the input alphabet
alphabet = set(re.findall(r'\w', regex))
#Define the DFA Starting state and transition function
start_state = frozenset({0})
transition_function = {}
#Define the state index counter
state_index = 1
#Define the stack for processing subsets
stack = [start_state]
#use the subset construction alogrithm to generate the DFA
while stack:
    current_state = stack.pop()
    for symbol in alphabet:
        next_state = frozenset({i+1 for i in range(len(regex)) if regex[i] == symbol and i})
        if next_state:
            if next_state not in transition_function:
                transition_function[current_state]= {}
            transition_function[current_state][symbol] = next_state
            if next_state not in transition_function:
                stack.append(next_state)
                state_index += 1
#Define the final states
final_states = set()
for state in transition_function:
    for index in state:
        if index == len(regex)-1:
            final_states.add(state)
#Define the pairs of distinguishable states and their initial partition
partition = [final_states, set(start_state) - final_states]
pairs = [(final_states, set(start_state) - final_states)]
#Use the O(n^2) algorithm to minimize the DFA
while pairs:
    p1, p2 = pairs.pop(0)
    for symbol in alphabet:
        x = set()
        for state in p1:
            if state in transition_function and symbol in transition_function[state]:
                x.add(transition_function[state][symbol])
        y = set()
        for state in p2:
            if state in transition_function and symbol in transition_function[state]:
                y.add(transition_function[state][symbol])
        if x and y:
            if x in partition and y in partition:
                pairs.append((x,y))
            else:
                partition.append(x)
                partition.append(y)
                pairs += [(x,p) for p in partition if p != x and p != y]
                pairs += [(y,p) for p in partition if p != x and p != y]
                partition.remove(p1)
                partition.remove(p2)
#Combine the non-distinguishable states into a single state
new_states = {}
for state in transition_function:
    new_state = None
    for p in partition:
        if state.issubset(p):
            new_state = p
            break
    if new_state not in new_states:
        new_states[new_state] = {}
    for symbol in transition_function[state]:
        next_state = transition_function[state][symbol]
        for p in partition:
            if next_state.issubset(p):
                next_state = p 
                break
        new_states[new_state][symbol] = next_state
start_state = frozenset({s for s in new_states.keys() if 0 in s})
final_states = set([s for s in new_states.keys() if len(regex)-1 in s])
#print the minimized DFA
print("Свернутый DFE:")
print("Начальное состояние: ", start_state)
print("Конечное состояние: ", final_states)
for state in new_states:
    print("Состояние: ", state)
    for symbol in alphabet:
        if symbol in new_states[state]:
            print(symbol, " -> ", new_states[state][symbol])



'''

#Конструкция НКА из регулярного выражения. С использованием алгоритма Томпсона
#1) По регулярному выражению строит НКА
class State:
    def __init__(self, label=None, edges=None):
        self.label = label
        self.edges = edges or []

class NFA:
    def __init__(self, start=None, end=None):
        self.start = start or State()
        self.end = end or State()
    
    def connect(self, state1, state2, edge=None):
        state1.edges.append((edge, state2))
    
    def match(self, string):
        current_states = self.follow_epsilon([self.start])
        for char in string:
            next_states = []
            for state in current_states:
                for edge in state.edges:
                    if edge[0] == char:
                        next_states.append(edge[1])
            current_states = self.follow_epsilon(next_states)
        return self.end in current_states
    
    def follow_epsilon(self, states):
        followed_states = set(states)
        for state in states:
            if state.label is None:
                for edge in state.edges:
                    if edge[0] is None:
                        followed_states.add(edge[1])
                        followed_states |= self.follow_epsilon([edge[1]])
        return followed_states

def compile(regexp):
    stack = []
    nfa = None
    for char in regexp:
        if char == '|':
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            start = State(edges=[(None, nfa1.start), (None, nfa2.start)])
            end = State()
            nfa1.end.edges.append((None, end))
            nfa2.end.edges.append((None, end))
            nfa = NFA(start=start, end=end)
        elif char == '*':
            nfa1 = stack.pop()
            start = State(edges=[(None, nfa1.start), (None, None)])
            end = State()
            nfa1.end.edges.append((None, nfa1.start))
            nfa1.end.edges.append((None, end))
            start.edges.append((None, end))
            nfa = NFA(start=start, end=end)
        elif char == '+':
            nfa1 = stack.pop()
            start = nfa1.start
            end = State()
            nfa1.end.edges.append((None, nfa1.start))
            nfa1.end.edges.append((None, end))
            nfa = NFA(start=start, end=end)
        elif char == '.':
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            nfa1.end.edges.append((None, nfa2.start))
            nfa = NFA(start=nfa1.start, end=nfa2.end)
        else:
            start = State()
            end = State()
            start.edges.append((char, end))
            nfa = NFA(start=start, end=end)
        stack.append(nfa)
    return stack.pop()

regexp = input("Введите регулярное выражение: ")
nfa = compile(regexp)

def print_nfa(nfa):
    print("NFA start={}, end={}".format(id(nfa.start), id(nfa.end)))
    for state in nfa.follow_epsilon([nfa.start]):
        for edge in state.edges:
            if edge[0] is not None:
                print("  {} --{}--> {}".format(id(state), edge[0], id(edge[1])))
            else:
                print("  {} --ε--> {}".format(id(state), id(edge[1])))

print_nfa(nfa)
#Example a*b|c+d

#2) По НКА строит эквивалентный ему ДКА

from collections import deque

class DFA:
    def __init__(self, start_state, states):
        self.start_state = start_state
        self.states = states

class DFAState:
    def __init__(self, nfa_states):
        self.nfa_states = nfa_states
        self.edges = {}

def nfa_to_dfa(nfa):
    start_states = nfa.follow_epsilon([nfa.start])
    dfa_states = {}
    queue = deque()

    start_dfa_state = DFAState(start_states)
    dfa_states[frozenset(start_states)] = start_dfa_state
    queue.append(start_dfa_state)

    while queue:
        dfa_state = queue.popleft()
        for symbol in nfa.symbols:
            next_nfa_states = nfa.follow_symbol(dfa_state.nfa_states, symbol)
            next_dfa_states_set = frozenset(nfa.follow_epsilon(next_nfa_states))
            if next_dfa_states_set not in dfa_states:
                next_dfa_state = DFAState(next_nfa_states)
                dfa_states[next_dfa_states_set] = next_dfa_state
                queue.append(next_dfa_state)
            else:
                next_dfa_state = dfa_states[next_dfa_states_set]
            dfa_state.edges[symbol] = next_dfa_state

    dfa_states = list(dfa_states.values())
    return DFA(start_state=start_dfa_state, states=dfa_states)

nfa = parse_regex("a*b|c+d")
dfa = nfa_to_dfa(nfa)
print("DFA start={}".format(id(dfa.start_state)))
for state in dfa.states:
    print("  {} ({})".format(id(state), state.nfa_states))
    for symbol, target in state.edges.items():
        print("    {} -> {}".format(symbol, id(target)))
'''
