def reduceAutomata( state_transition_table: "dict[str, list(list(str, str), list(str, str))]" ):
    stateMissing: bool = False

    for key in state_transition_table:
        # If both next state and output symbol is present, convert output symbol to integer
        try:
            if(state_transition_table[key][0][0] != '-' and state_transition_table[key][0][1] != '-'):
                state_transition_table[key][0][1] = int(state_transition_table[key][0][1])
            if(state_transition_table[key][1][0] != '-' and state_transition_table[key][1][1] != '-'):
                state_transition_table[key][1][1] = int(state_transition_table[key][1][1])
        except:
            raise Exception("Invalid output symbol provided")

        # If only output symbol is missing
        if(state_transition_table[key][0][0] != '-' and state_transition_table[key][0][1] == '-'):
            state_transition_table[key][0][1] = 0
        if(state_transition_table[key][1][0] != '-' and state_transition_table[key][1][1] == '-'):
            state_transition_table[key][1][1] = 0

        # If only next state is missing
        if(state_transition_table[key][0][0] == '-' and state_transition_table[key][0][1] != '-'):
            state_transition_table[key][0][0] = 'T'
            stateMissing = True
        if(state_transition_table[key][1][0] == '-' and state_transition_table[key][1][1] != '-'):
            state_transition_table[key][1][0] = 'T'
            stateMissing = True

        # If both next state and output symbol is missing
        if(state_transition_table[key][0][0] == '-' and state_transition_table[key][0][1] == '-'):
            state_transition_table[key][0][0] = 'T'
            state_transition_table[key][0][1] = 0
            stateMissing = True
        if(state_transition_table[key][1][0] == '-' and state_transition_table[key][1][1]):
            state_transition_table[key][1][0] = 'T'
            state_transition_table[key][1][1] = 0
            stateMissing = True
    
    if(stateMissing == True):
        state_transition_table['T'] = [ ['T', 0], ['T', 0] ]
    
    print(state_transition_table)
    return performMooreReduction(state_transition_table)



# The following function will accept a state transition table of a finite state automata which is completely
# specified. It is assumed that this automata will have it's states labelled as A, B, C, D, etc and the input
# and output symbols will comprise only of '0' and '1'.

# This function accepts the table, reduces it to a state in which the finite automata has the minimum number
# of states, that is, it performs Moore Reduction. Finally, it returns the reduced state transition table
# in Standard Form.

# The structure of the data structure containing the table is as follows:
#       dict[ str, tuple( tuple(str, int), tuple(str, int) ) ]
#
# In the dictionary, "Present State" will be the key; and the "Next States" will be the value
# The value (or "Next States") is represented as a tuple.
# The first element of this tuple is the "Next State" and "Output Symbol" for input symbol = 0
# Similarly, the second element is the "Next State" and "Output Symbol" for input symbol = 1
# These two are also tuples by themselves as they are both containing 2 ordered values each.

def performMooreReduction( state_transition_table: "dict[str, list(list(str, int), list(str, int))]" ):
    # Check whether input data is valid or not. If not, throw AssertionError
    data_correct = transitionTableValidator(state_transition_table)
    assert(data_correct == 'Valid'), data_correct

    # Initially, for input strings of length 0, no states are distinguishable. So, all the states together
    # constitute a single group. Here, we extract all the states and form such a group.
    all_states = ''
    for key in state_transition_table:
        all_states += key

    # This represents the initial group which is just one group consisting of all the states
    previous_groups = [ all_states ]
    # Initially we start with input strings of length = 1 and keep on incrementing by 1 until we get two
    # successive strings which give the same groups
    input_string_length: int = 1

    while(True):
        # Generate all possible strings with the current length
        input_strings = generateInputStrings(input_string_length)
        largest_groups = []

        # For each possible input string of current length, get the groups
        # Keep the group which has the largest number of distinct outputs
        for input_string in input_strings:
            groups = getOutputGroups(state_transition_table, input_string)
            if(len(groups) > len(largest_groups)):
                largest_groups = groups
        
        # If we get 2 identical groups with strings of 2 successive lengths, then we know that the
        # reduction process is complete. Else, we move on to strings of length incremented by 1
        if(previous_groups == largest_groups):
            break
        else:
            input_string_length += 1
            previous_groups = largest_groups
    

    # Remove the redundant states
    for group in previous_groups:
        if(len(group) > 1):
            for extra_state in range(1, len(group)):
                # Remove the entry corresponding to the extra state
                state_transition_table.pop(group[extra_state])

                # Replace all the next states with the first state in the group
                for key in state_transition_table:
                    if(state_transition_table[key][0][0] == group[extra_state]):
                        state_transition_table[key][0][0] = group[0]
                    if(state_transition_table[key][1][0] == group[extra_state]):
                        state_transition_table[key][1][0] = group[0]
    


    # For standardizing the states, we first temporarily give them numeric names in order
    temp_numeric_states = []
    temp_dictionary = {}

    for key in state_transition_table:
        # If key has not already been encountered, then add it to list
        if key not in temp_numeric_states:
            temp_numeric_states.append(key)
        
        # Replace the key first in the dictionary
        temp_dictionary[temp_numeric_states.index(key)] = state_transition_table[key]

        # Check the next states in dictionary and replace them as necessary
        if temp_dictionary[temp_numeric_states.index(key)][0][0] not in temp_numeric_states:
            temp_numeric_states.append(temp_dictionary[temp_numeric_states.index(key)][0][0])
        
        temp_dictionary[temp_numeric_states.index(key)][0][0] = temp_numeric_states.index(state_transition_table[key][0][0])

        if temp_dictionary[temp_numeric_states.index(key)][1][0] not in temp_numeric_states:
            temp_numeric_states.append(temp_dictionary[temp_numeric_states.index(key)][1][0])
        
        temp_dictionary[temp_numeric_states.index(key)][1][0] = temp_numeric_states.index(state_transition_table[key][1][0])
    


    # Now replace all the numeric values with alphabets in lexicographic order
    state_transition_table = {}

    for key in sorted(temp_dictionary):
        new_key = chr(ord('A') + key)
        state_transition_table[new_key] = temp_dictionary[key]
        state_transition_table[new_key][0][0] = chr(ord('A') + temp_dictionary[key][0][0])
        state_transition_table[new_key][1][0] = chr(ord('A') + temp_dictionary[key][1][0])
    
    return state_transition_table
                    




# Function accpets the length of the input string
# Generates all possible combinations of bit strings with the given length and returns a list containing them

def generateInputStrings(string_length: int) -> list:
    total_combinations = pow(2, string_length)
    combinations = []

    for value in range(0, total_combinations):
        combinations.append(bin(value).replace('0b', '').zfill(string_length))
    
    return combinations




# Function accepts the input string and the state transition table.
# Generates the corresponding output string

def getOutputGroups( state_transition_table, input_string: str ) -> str:
    groups = {}

    # Output string is generated starting from every state
    present_state: str = ''
    for key in state_transition_table:
        present_state = key
        output_string = ''

        # All symbols in the input string are traversed and output is generated
        for symbol in input_string:
            output_symbol: int = state_transition_table[present_state][int(symbol)][1]
            present_state = state_transition_table[present_state][int(symbol)][0]
            output_string += str(output_symbol)
        
        # If the generated output string has been encountered before, add the current key to the group
        # Else, create a new group and the current key.
        if(output_string in groups):
            groups[output_string] += key
        else:
            groups[output_string] = key
    
    # Prepare a list of the groups and return it
    groups_list = []
    for key in groups:
        groups_list.append(groups[key])
    
    return groups_list




# Validate each state in the state transition table. Each state should be a string containing only
# a single alphabet.

def stateValidator( state: str ) -> str:
    valid = 'Valid'

    # Every state should be a string
    if(type(state) != str):
        valid = 'Invalid: Every key in the dictionary should be a string'
    
    # Every state should have only one character
    elif(len(state) != 1):
        valid = 'Invalid: Every state should have just one character'
    
    # The only character present in each state should be an alphabet
    elif(state.isalpha() == False):
        valid = 'Invalid: Every state should have just one alphabet representing it'
    
    return valid



# Validate the state transition table. The table should be in the format specified. Each state in the table
# should be a string with a single alphabet in it and each output symbol should be a integer which can be
# either 0 or 1. The table can have only 2 types of input symbols - 0 and 1.

def transitionTableValidator( state_transition_table: "dict[str, list(list(str, int), list(str, int))]" ) -> str:
    valid: str = 'Valid'

    # The base structure should be a dictionary
    if(type(state_transition_table) != dict):
        valid = 'Invalid: The entire structure of the table should be a dictionary'
        return valid
    
    for key in state_transition_table:
        # Every key should be a string
        valid = stateValidator(key)
        if(valid != 'Valid'):
            return valid
        
        # Each value corresponding to every key should be a tuple
        if(type(state_transition_table[key]) != list):
            valid = 'Invalid: Every value corresponding to each key should be a tuple'
            return valid
        
        # Every tuple representing the values should contain 2 tuples - first for input = 0 and the second for input = 1
        if( type(state_transition_table[key][0]) != list or type(state_transition_table[key][1]) != list ):
            valid = 'Invalid: Every tuple representing the next states should contain 2 tuples in turn. First one for input = 1 and the second one for input = 1'
            return valid
        
        # Each next state should have a string and a number representing the next state and the output respectively
        valid = stateValidator(state_transition_table[key][0][0])
        if(valid != 'Valid'):
            return valid
        valid = stateValidator(state_transition_table[key][1][0])
        if valid != 'Valid':
            return valid
        
        # Each output should be a number and should be either 0 or 1
        if(type(state_transition_table[key][0][1]) != int or type(state_transition_table[key][1][1]) != int):
            valid = 'Invalid: Output symbol should be either 0 or 1 and it should be a number'
            return valid
        
        if((state_transition_table[key][0][1] != 0 and state_transition_table[key][1][1] != 1) or 
            state_transition_table[key][0][1] != 0 and state_transition_table[key][1][1] != 1):
            valid = 'Invalid: Output symbol can only be either 0 or 1'
            return valid
    
    return valid



# Print a state transition table

def printStateTransitionTable(state_transition_table: "dict[str, list(list(str, int), list(str, int))]"):
    print("PS |   Input Symbols")
    print("   |    0    |    1")
    print("   | NS | OS | NS | OS")
    print("----------------------")

    for key in state_transition_table:
        ns0 = state_transition_table[key][0][0]
        os0 = state_transition_table[key][0][1]
        ns1 = state_transition_table[key][1][0]
        os1 = state_transition_table[key][1][1]

        print(f" {key} |  {ns0} |  {os0} |  {ns1} |  {os1}")

    print("")
    print("PS: Present State")
    print("NS: Next State")
    print("OS: Output Symbol")
