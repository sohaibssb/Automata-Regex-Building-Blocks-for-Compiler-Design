import sys
import json
import copy

def convert_lists_to_tuples(obj):
    if isinstance(obj, list):
        return tuple(convert_lists_to_tuples(item) for item in obj)
    elif isinstance(obj, dict):
        return {convert_lists_to_tuples(key): convert_lists_to_tuples(value) for key, value in obj.items()}
    else:
        return obj

input_file = open(sys.argv[1], "r")
contents = input_file.read()
input_file.close()

file_obj = json.loads(contents, object_hook=convert_lists_to_tuples)

states = copy.deepcopy(file_obj["states"])
letters = copy.deepcopy(file_obj["letters"])
transition = copy.deepcopy(file_obj["transition_function"])
start_states = copy.deepcopy(file_obj["start_states"])
final_states = copy.deepcopy(file_obj["final_states"])

def check_string_dfa(input_string, states, letters, transition_function, start_state, final_states):
    current_state = start_state
    for char in input_string:
        for i in range(len(letters)):
            if letters[i] == char:
                current_state = transition_function[current_state][i]
                break
        else:
            return "reject"
    if current_state in final_states:
        return "accept"
    else:
        return "reject"

input_string = input("Enter the input string: ")
result = check_string_dfa(input_string, states, letters, transition, start_states[0][0], final_states)
print(result)
