import sys
import json


def minus(states,final_states):
    arr=[]
    #print(states)
    for st in states:
        if st not in final_states:
            arr.append(st)
    #print(arr)        
    return arr

def trans(state,alph,transition):
    for tr in transition:
        if tr[0]==state and tr[1] ==alph:
            return tr[2]

def update(states,transition,start_states):
    #print(transition)

    states_set=set()
    states_set=states_set.union(states)
    #states_set = states_set.union([tuple(state) for state in states])

    #print(states_set)
    reachable_states=set()
    reachable_states=reachable_states.union(start_states)
    new_states=set()
    new_states=new_states.union(start_states)
    co=0
    while len(new_states)!=0:
        co+=1
        temp=set()
        for q in new_states:
            for c in letters:
                dest=trans(q,c,transition)
                temp=temp.union({dest})

        new_states=temp.difference(reachable_states)
        reachable_states=reachable_states.union(new_states)
       
    unreachable_states=set()
    unreachable_states=states_set.difference(reachable_states)
    #print(states_set)
    #print("unreachablestates are", unreachable_states)
    #return reachable_states
    return list(reachable_states)



def destination(dest,states):
    for st in states:
        for ev in st:
            if ev==dest:
                return st

class minimize_dfa:
    def __init__(self,states,letters,transition,start_states,final_states):
        
        self.startstates=[]
        self.allstates=[]
        self.finalstates=[]
        self.letters=letters
        self.transition=[]
        self.minimize(states,letters,transition,start_states,final_states)

    def minimize(self,states,letters,transition,start_states,final_states):
        #print(states)
        states=update(states,transition,start_states) 
        #print(states)
        has=states
        #print(has)
        p0=[]
        p0.append(final_states)
        p0.append(minus(states,final_states)) 
        pnow=p0
        iter=0
        state_matrix=[[0 for i in range(len(states))]for j in range(len(states))]
        for i1 in states:
            for i2 in states:
                if (i1 not in final_states and i2 in final_states) or (i2 not in final_states and i1 in final_states):
                    state_matrix[has.index(i1)][has.index(i2)]=1
                    #print("updated",i1,i2)

        #print(state_matrix)
        updates=1
        iter=0
        while(updates):
            iter+=1
            #print(iter)
            # if(iter>10):
            #     break
            updates=0
            for i1 in states:
                for i2 in states:
                    for le in letters:
                        dest1=trans(i1,le,transition)
                        dest2=trans(i2,le,transition)
                        if state_matrix[has.index(dest1)][has.index(dest2)]==1:
                            if state_matrix[has.index(i1)][has.index(i2)]==0: 
                                updates=1
                                #print("updated",i1, has.index(i1),i2,has.index(i2))
                            state_matrix[has.index(i1)][has.index(i2)]=1
                            #state_matrix[has.index(i2)][has.index(i1)]=1
                                             
        new_states=[]
        for each in state_matrix:
            arr1=[]
            for st in range(len(each)):
                if each[st]==0:
                    stat=has[st]
                    arr1.append(stat)
            if arr1 not in new_states:
                new_states.append(arr1)

        self.make_min_dfa(new_states,letters,transition,start_states,final_states)

    def make_min_dfa(self,states,letters,transition,start_states,final_states):
        self.allstates=states
        for allposs in states:
            for every in allposs:
                if every in start_states:
                    if allposs not in self.startstates:
                        self.startstates.append(allposs) 
                    
        for allposs in states:
            for every in allposs:
                if every in final_states:
                    if allposs not in self.finalstates:
                        self.finalstates.append(allposs)
                    
        for st in states:
            for alph in letters:
                dest=trans(st[0],alph,transition) 
                destset=destination(dest,states) 
                self.transition.append([st,alph,destset])
        self.prints()

    def prints(self):
        out={
            "states":self.allstates,
            "letters":self.letters,
            "transition_function":self.transition,
            "start_states":self.startstates,
            "final_states":self.finalstates
        }
       
        with open (sys.argv[2],'w') as outfile:
            json.dump(dict(out),outfile,indent=4)


import sys
import json
import copy
if(len(sys.argv) == 3):
        

    def convert_lists_to_tuples(data):
        if isinstance(data, list):
            return tuple(convert_lists_to_tuples(item) for item in data)
        elif isinstance(data, dict):
            return {convert_lists_to_tuples(key): convert_lists_to_tuples(value) for key, value in data.items()}
        else:
            return data

    input_file = open(sys.argv[1], "r")
    contents = input_file.read()
    input_file.close()

    file_obj = json.loads(contents, object_hook=convert_lists_to_tuples)

    states = copy.deepcopy(file_obj["states"])
    letters = copy.deepcopy(file_obj["letters"])
    transition = copy.deepcopy(file_obj["transition_function"])
    start_states = copy.deepcopy(file_obj["start_states"])
    final_states = copy.deepcopy(file_obj["final_states"])


    output_file = open(sys.argv[2], "w")

    m_dfa=minimize_dfa(states,letters,transition,start_states,final_states)

    print("------------------------------\n")
    print("             DFAM              \n")
    print("------------------------------\n")
    print("DFAM states:", m_dfa.allstates)
    print("\nDFAM alphabets:", m_dfa.letters)
    print("\nDFAM transitions:", m_dfa.transition)
    print("\nDFAM start state:", m_dfa.startstates)
    print("\nDFAM final states:", m_dfa.finalstates)
    print("\n------------------------------\n")

else:
    print("Usage: python3 MinimizeDFA.py <inputfile> <outputfile>")

    #python3 MinimizeDFA.py outputDFA.json outputDFAM.json 



