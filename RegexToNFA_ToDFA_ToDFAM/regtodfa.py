import sys
import json
class Regex:

    def __init__(self, regex):
        self.star = '*'
        self.union = '+'
        self.concat = '?'
        self.openb = '('
        self.closeb = ')'
        self.operators = [self.union, self.concat]
        self.regex = regex
        self.postfixregex=self.to_postfix(regex)
        self.prints()

    def prints(self):
        print(self.postfixregex) 
        pass   

    def top(self,arr):
        if len(arr)==0:
            return "fail"
        #print(len(arr))
        #print(arr[-1])
        return arr[-1]    

    def oper(self,ch):
        if ch==self.star or ch==self.union or ch==self.openb or ch==self.closeb or ch==self.concat:
            return 0 #operator
        return 1 #aplhabet  

    def prec(self,ops):
        if ops=="*":
            return 5
        elif ops=="?":
            return 4
        elif ops=="+":
            return 3
        elif ops=="(":
            return 2   
        elif ops=="fail":
            return 0     

    def to_postfix(self, regex):
        regex1=[i for i in regex]
        prop_regex=[]
        prev=0
        type0="Sym"
        for j in range(len(regex1)):
            if regex1[j]!=self.star and regex1[j]!=self.union  and regex1[j]!=self.openb and regex1[j]!=self.closeb:
                this="Alph"
                if prev=="Alph":
                    prop_regex.append(self.concat)
                prop_regex.append(regex1[j])

            elif regex1[j]==self.openb:
                this="Sym"
                if prev=="Alph":
                    prop_regex.append(self.concat)
                prop_regex.append(regex1[j])

            elif regex1[j]==self.closeb and j!=len(regex1)-1:
                this="Sym"
                prop_regex.append(regex1[j])   #here1
                if regex1[j+1]!=self.star :
                    prop_regex.append(self.concat)
                  

            elif regex1[j]==self.star and j!=len(regex1)-1:
                this="Sym"
                prop_regex.append(regex1[j]) 
                if regex1[j+1]!=self.closeb:   #here2
                    prop_regex.append(self.concat)
                   
            else:
                this="Sym"        
                prop_regex.append(regex1[j])  
            prev=this
        print(prop_regex)
        #added concat symbol
        #convert prop_regex to postfix
        op_stack=[]
        out_queue=[]
        for i in range(len(prop_regex)):
            
            op=self.oper(prop_regex[i])
            if op==1: #alphabet
                out_queue.append(prop_regex[i])
            else:
                if len(op_stack)==0:
                    #print(len(op_stack),i)
                    op_stack.append(prop_regex[i])
                else:
                    if prop_regex[i]!=")":
                        if prop_regex[i]=="(":
                            op_stack.append(prop_regex[i]) #push
                        else:    
                            while len(op_stack)>=0 and self.prec(self.top(op_stack))>=self.prec(prop_regex[i]):  
                                #print("problem at ",i)
                                out_queue.append(self.top(op_stack))
                                op_stack=op_stack[:-1] #pop
                            op_stack.append(prop_regex[i]) #push
                    else:
                        #print("end of iter ",i,"stack is ",op_stack)  
                        if prop_regex[i]==")":
                            while self.top(op_stack)!="(":
                                #print("end of iter ",i,"stack is ",op_stack)  
                                out_queue.append(self.top(op_stack))
                                op_stack=op_stack[:-1]
                            op_stack=op_stack[:-1]     #discard brackets
            #print("end of iter ",i,"stack is ",op_stack)            
        if len(op_stack)!=0:
            while len(op_stack)!=0:
                out_queue.append(self.top(op_stack))
                op_stack=op_stack[:-1]                        

        return out_queue


class NFA:
    def __init__(self):
        super().__init__()
        self.states=[]
        self.alphabets=[]
        self.trans_f=[]
        self.start_states=[]
        self.final_states=[]
       


    def set_state(self, state):
        f=0
        for i in range(len(self.states)):
            if self.states[i]==state:
                f=1
        if f==0:        
            self.states.append(state)    

    def set_alphabets(self,alph):
        f=0
        for i in range(len(self.alphabets)):
            if self.alphabets[i]==alph:
                f=1
        if f==0: 
            self.alphabets.append(alph)  

    def transition(self,arr):
        self.trans_f.append(arr)  

    def set_startstates(self,state):
        f=0
        for i in range(len(self.start_states)):
            if self.start_states[i]==state:
                f=1
        if f==0: 
            self.start_states.append(state) 

    def set_endstates(self,state):
        f=0
        for i in range(len(self.final_states)):
            if self.final_states[i]==state:
                f=1
        if f==0: 
            self.final_states.append(state)

def ispresent(alph):
    palphabet = [chr(i) for i in range(65,91)]
    palphabet.extend([chr(i) for i in range(97,123)])
    palphabet.extend([chr(i) for i in range(48,58)])
    for i in palphabet:
        if alph==i:
            return 1
    return 0

def regex_to_nfa(regex):
    c_state=0
    nfa_stack=[]
    for op in regex:
        if  ispresent(op):
            nfa1=NFA()
            S1=c_state
            nfa1.set_startstates(S1)
            S2=c_state+1
            nfa1.set_endstates(S2)
            nfa1.transition([S1,op,S2])
            nfa1.set_alphabets(op)
            nfa1.set_state(S1)
            nfa1.set_state(S2)
            nfa_stack.append(nfa1)
            c_state+=2

        elif op=="$":
            nfa=NFA()
            nfa.set_state(c_state)
            nfa.set_endstates(c_state)
            nfa.set_startstates(c_state)
            nfa_stack.append(nfa)
            c_state+=1
        
        elif op=="+":
            nfa2=nfa_stack.pop()
            nfa1=nfa_stack.pop()
            nfa=NFA()
            nfa.set_startstates(c_state)
            for sta in nfa1.final_states:
                nfa.set_endstates(sta)
            for sta in nfa2.final_states:
                nfa.set_endstates(sta)
            for st in nfa2.start_states:
                nfa.transition([c_state,"$",st]) #to all start states
            for st in nfa1.start_states:
                nfa.transition([c_state,"$",st]) #to all start states
            for tr in nfa1.trans_f:    
                nfa.transition(tr)
            for tr in nfa2.trans_f:    
                nfa.transition(tr)
            for st in nfa2.states:
                nfa.set_state(st)
                #print(st)
            for st1 in nfa1.states:
                nfa.set_state(st1)
                #print(st1)
            nfa.set_state(c_state)    
            for al in nfa1.alphabets:
                nfa.set_alphabets(al)
            for al in nfa2.alphabets:
                nfa.set_alphabets(al) 

            c_state+=1
            nfa_stack.append(nfa)

        elif op=="?":

            nfa2=nfa_stack.pop()
            nfa1=nfa_stack.pop()
            nfa=NFA()
            for st in nfa1.start_states:
                nfa.set_startstates(st)
            for st in nfa2.final_states:
                nfa.set_endstates(st) 
            for fs in nfa1.final_states:
                nfa.transition([fs,"$",nfa2.start_states[0]])
                #print([fs,"$",nfa2.start_states[0]])
            for st in nfa2.states:
                nfa.set_state(st)
            for st in nfa1.states:
                nfa.set_state(st)  
            for al in nfa1.alphabets:
                nfa.set_alphabets(al)
            for al in nfa2.alphabets:
                nfa.set_alphabets(al)
            for tr in nfa1.trans_f:    
                nfa.transition(tr)
            for tr in nfa2.trans_f:    
                nfa.transition(tr)

            nfa_stack.append(nfa)

        elif op=="*":
            nfa1=nfa_stack.pop()
            nfa = NFA()
            nfa.set_startstates(c_state)
            for st in nfa1.states:
                nfa.set_state(st) 
            nfa.set_state(c_state)
            for st in nfa1.final_states:
                nfa.set_endstates(st)
            for al in nfa1.alphabets:
                nfa.set_alphabets(al)
            nfa.set_endstates(c_state)
            for tr in nfa1.trans_f:    
                nfa.transition(tr)

            nfa.transition([c_state,"$",nfa1.start_states[0]])  
        
            for st in nfa1.final_states:
                nfa.transition([st,"$",nfa1.start_states[0]]) 

            nfa_stack.append(nfa) 
            c_state+=1

        else:
            print("ambiguous symbol")    
    return nfa_stack[0]





if(len(sys.argv) == 3):
        
    input_file = open(sys.argv[1],"r")    
    output_file = open(sys.argv[2],"w")
    file_obj = json.load(input_file)
    regex = file_obj['regex']
    exp=Regex(regex)
    nfa= regex_to_nfa(exp.postfixregex)
    sts=[]
    for i in range(len(nfa.start_states)):
        sts.append("q"+str(nfa.start_states[i]))
    ends=[]
    for i in range(len(nfa.final_states)):
        ends.append("q"+str(nfa.final_states[i]))
    st=[]
    for i in range(len(nfa.states)):
        st.append("q"+str(nfa.states[i]))
    transition_new=[]
    for transi in nfa.trans_f:
        #print(transi[2])
        transition_new.append(["q"+str(transi[0]),transi[1],"q"+str(transi[2])])

    out={
            "states":st,
            "letters":nfa.alphabets,
            "transition_function":transition_new,
            "start_states":sts,
            "final_states":ends
        }

    # Print the NFA results on the screen
    print("------------------------------\n")
    print("             NFA              \n")
    print("------------------------------\n")
    print("NFA States: ", st)
    print("\nNFA Alphabets: ", nfa.alphabets)
    print("\nNFA Transition Function: ", transition_new)
    print("\nNFA Start States: ", sts)
    print("\nNFA Final States: ", ends)
    print("\n------------------------------\n")

    with open(sys.argv[2],'w') as outfile:
        json.dump(dict(out),outfile,indent=4)

else:
    print("Usage: python3 regtodfa.py <inputfile> <outputfile>")

