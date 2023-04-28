import json
import sys
from itertools import combinations


 #////////// Regex to NFA //////////////////////////////////////

import subprocess
import json

data = {"regex": input(" Введите регулярное выражение: ")}

with open('regex.json', 'w') as f:
     json.dump(data, f)

input_file = "regex.json"
output_file = "outputNFA.json"

subprocess.run(["python3", "regtodfa.py", input_file, output_file], check=True)

#///////////////////////////////////////////////////////////////


def check(arr,pos):
    for tup in arr:
        if set(tup)==set(pos):
            return 0
    return 1


def check1(arr,pos):
    for tup in arr:
        if tup==pos:
            return 0
    return 1

class nfa_to_dfa:
    def __init__(self,states,letters,transition,start_states,final_states):
        
        self.startstates=self.get_startstates(start_states,transition)
        self.allstates=self.powerset(states)
        self.final_states=self.get_finalstates(final_states)
        self.letters=letters
        self.transition=self.main_matrix(transition)
        self.prints()

    def prints(self):
        out={
            "states":self.allstates,
            "letters":self.letters,
            "transition_function":self.transition,
            "start_states":self.startstates,
            "final_states":self.final_states
        }
       
        with open (sys.argv[2],'w') as outfile:
            json.dump(dict(out),outfile,indent=4)


    def main_matrix(self,transition):
        #write separately for empty
        trans_matrix=[]
        for state in self.allstates:            
            for alph in self.letters:
                dest_arr=[]
                found=0        #if alphabet not found put phi
                for st in state:
                    #check through tranisition matrix and append states ,if nothing is found append to phi
                    for tran in transition:
                        if tran[0]==st and tran[1]==alph and st!="" and check1(dest_arr,tran[2]):
                            dest_arr.append(tran[2])
                            found=1
                trans_matrix.append([state,alph,dest_arr])
        # for alph in self.letters:
        #     trans_matrix.append([[],alph,[]])
        return trans_matrix


    def get_finalstates(self,finalstates):
        finalarr=[]
        for state in final_states:
            for pos in self.allstates:
                for each_state in pos:
                    if each_state==state and check(finalarr,pos):
                        finalarr.append(pos)
        return finalarr                



    def powerset(self,states):
        all_arr=[]
        for i in range(1,len(states)+1):
            for element in combinations(states,i):
                all_arr.append(list(element))
        all_arr.append([])        
        return all_arr


    def get_startstates(self,startstates,transition):
        start_arr=[]
        for start in startstates:
            arr=[]
            arr.append(start)  
            for tup in transition:
                if tup[0]==start and tup[1]=="$":
                    arr.append(tup[2])
            start_arr.append(arr)     
        return start_arr            



if(len(sys.argv) == 3):
        
        input_file = open(sys.argv[1],"r")    
        file_obj = json.load(input_file)
        states = file_obj['states']
        letters=file_obj['letters']
        transition=file_obj['transition_function']
        start_states=file_obj['start_states']
        final_states=file_obj['final_states']
        dfa=nfa_to_dfa(states,letters,transition,start_states,final_states)
        print("------------------------------\n")
        print("             DFA              \n")
        print("------------------------------\n")
        print("DFA states:", dfa.allstates)
        print("\nDFA alphabets:", dfa.letters)
        print("\nDFA transitions:", dfa.transition)
        print("\nDFA start state:", dfa.startstates)
        print("\nDFA final states:", dfa.final_states)
        print("\n------------------------------\n")

else: 
        print("Error")
        print("Usage: python3 NFAtoDFA.py <inputfile> <outputfile>")
        # python3 NFAtoDFA.py outputNFA.json outputDFA.json 
     

