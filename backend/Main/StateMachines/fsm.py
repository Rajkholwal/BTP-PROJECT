import random
import os
from graphviz import Digraph
import cairosvg

def get_svg_from_file(filepath):
    with open(filepath, "r") as f:
        return f.read()

def genearte_question_FSM(level):
    flag = random.randint(1, 4)
    if(flag==1):
        question_text, option, correct_answer, images = Nonoverlapping_MealyFSM()
    elif(flag==2):
        question_text, option, correct_answer, images = Overlapping_MealyFSM()
    elif(flag==3):
        question_text, option, correct_answer, images = Nonoverlapping_MooreFSM()
    elif(flag==4):
        question_text, option, correct_answer, images = Overlapping_MooreFSM()
    
    return (question_text, option, correct_answer, [get_svg_from_file(image) for image in images])

def get_random_filename():
    return f"sequence_img_{random.randint(1, 10000)}"

def Question_text_generator(seq,state,bit):
    question_text=f"The following state diagram is designed to detect the string '{seq}'. One of the transitions from State '{state}' on receiving bit '{bit}' is missing. Select the correct option that complete the state diagram(Assume start state is S0):-"
    return question_text

def generate_distractors(states, correct_next_state):
    # Start by adding the correct answer
    possible_answers = [correct_next_state]
    
    # Add unique distractors while avoiding the correct answer
    while len(possible_answers) < min(len(states) + 1, 4):  # Ensures no more than available states + 1 (correct answer)
        random_distractor = random.choice(states)
        
        # Add the distractor if it's not already in the possible_answers
        if random_distractor not in possible_answers:
            possible_answers.append(random_distractor)
    
    # Shuffle the possible answers so the correct one isn't always in the same position
    random.shuffle(possible_answers)
    
    return possible_answers

def Nonoverlapping_MealyFSM(image_dir="StateMachines/images"):
    # Define a list of sequences and choose one randomly
    sequences = ["101", "1010", "1101", "011", "0101", "010", "1001", "0110"]
    sequence = random.choice(sequences)

    # Create states and transitions
    n = len(sequence)
    states = [f'S{i}' for i in range(n+1)]
    transitions = {state: {} for state in states}

    # Build the FSM transitions
    for i in range(n):
        current_state = states[i]
        next_state = states[i+1]
        char = sequence[i]

        for symbol in '01':
            if symbol == char:
                transitions[current_state][symbol] = (next_state, '1' if i == n-1 else '0')
            else:
                fallback_state = find_fallback_state(sequence, i, symbol, states)
                transitions[current_state][symbol] = (fallback_state, '0')

    # Handle the final state transitions
    final_state = states[-1]
    for symbol in '01':
        transitions[final_state][symbol] = ("S0", '0')

    # Randomly remove a transition
    state, symbol, removed_transition = remove_random_transition(transitions, states)
    if not removed_transition:
        return None  # If no transition could be removed

    # Generate the question text
    question_text = Question_text_generator(sequence,state,symbol)

    # Define the correct answer
    next_state, output = removed_transition
    correct_answer = f"{next_state} / {output}"
    possible_answers = {correct_answer}

    # Randomly generate 3 more incorrect answers
    while len(possible_answers) < 4:
        random_next_state = random.choice(states)
        random_output = random.choice(['0', '1'])
        possible_answers.add(f"{random_next_state} / {random_output}")

    # Shuffle the possible answers
    possible_answers = list(possible_answers)
    random.shuffle(possible_answers)
    correct_answer_index = possible_answers.index(correct_answer)

    # Render the FSM diagram using Graphviz and return the generated question and answers
    os.makedirs(image_dir, exist_ok=True)
    graph_svg = print_mealyfsm_graphviz(states, transitions, image_dir, get_random_filename())

    # labeled_options = [f"{chr(65+i)}. {option}" for i, option in enumerate(possible_answers)]
    return (question_text, possible_answers, correct_answer, [graph_svg])

def find_fallback_state(sequence, index, symbol, states):
    for i in range(index, 0, -1):
        if sequence[:i] == sequence[index-i+1:index] + symbol:
            return states[i]
    return states[0]
def remove_random_transition(transitions, states):
    state = random.choice(states[:-1])  # Choose a random state, excluding the last one
    symbol = random.choice(['0', '1'])  # Randomly choose between '0' and '1'

    if symbol in transitions[state]:
        removed_transition = transitions[state].pop(symbol)
        return (state, symbol, removed_transition)
    
def print_mealyfsm_graphviz(states, transitions, image_dir, filename):
    dot = Digraph()

    # Add states to the graph
    for state in states:
        dot.node(state)
    
    # Add transitions to the graph
    for state, trans in transitions.items():
        for symbol, (next_state, output) in trans.items():
            label = f'{symbol}/{output}'
            dot.edge(state, next_state, label=label)

    filepath = os.path.join(image_dir, filename)
    dot.render(filepath, format="svg", cleanup=False)

    graph_svg = f"{filepath}.svg"
    # print(f"FSM graph generated as {graph_svg}")
    
    return graph_svg
def Overlapping_MealyFSM(image_dir="StateMachines/images"):
    # Define a list of sequences and choose one randomly
    sequences = ["101", "1010", "1101", "011", "0101", "010", "1001", "0110"]
    sequence = random.choice(sequences)

    # Create states and transitions
    n = len(sequence)
    states = [f'S{i}' for i in range(n+1)]
    transitions = {state: {} for state in states}

    # Build the FSM transitions
    for i in range(n):
        current_state = states[i]
        next_state = states[i+1]
        char = sequence[i]

        for symbol in '01':
            if symbol == char:
                transitions[current_state][symbol] = (next_state, '1' if i == n-1 else '0')
            else:
                fallback_state = find_fallback_state(sequence, i, symbol, states)
                transitions[current_state][symbol] = (fallback_state, '0')

    # Handle the final state transitions
    final_state = states[-1]
    for symbol in '01':
        fallback_state = find_fallback_state(sequence, n, symbol, states)
        transitions[final_state][symbol] = (fallback_state, '0')

    # Randomly remove a transition
    state, symbol, removed_transition = remove_random_transition(transitions, states)
    if not removed_transition:
        return None  # If no transition could be removed

    # Generate the question text
    question_text = Question_text_generator(sequence,state,symbol)
    # Define the correct answer
    next_state, output = removed_transition
    correct_answer = f"{next_state} / {output}"
    possible_answers = {correct_answer}

    # Randomly generate 3 more incorrect answers
    while len(possible_answers) < 4:
        random_next_state = random.choice(states)
        random_output = random.choice(['0', '1'])
        possible_answers.add(f"{random_next_state} / {random_output}")

    # Shuffle the possible answers
    possible_answers = list(possible_answers)
    random.shuffle(possible_answers)
    correct_answer_index = possible_answers.index(correct_answer)

    # Render the FSM diagram using Graphviz and return the generated question and answers
    os.makedirs(image_dir, exist_ok=True)
    graph_svg = print_mealyfsm_graphviz(states, transitions, image_dir, get_random_filename())


    # labeled_options = [f"{chr(65+i)}. {option}" for i, option in enumerate(possible_answers)]
    return (question_text, possible_answers, correct_answer, [graph_svg])
def Nonoverlapping_MooreFSM(image_dir="StateMachines/images"):
    sequences = ["101", "1010", "1101", "011", "0101", "010", "1001", "0110"]
    sequence = random.choice(sequences)
    os.makedirs(image_dir, exist_ok=True)
    
    # Build the FSM for the given sequence
    states, transitions, outputs = N_O_build_fsm(sequence)

    # Ask for the missing transition
    missing_transition = ask_for_completion(transitions, states)

    # Generate the FSM diagram
    fsm_graph_svg = print_moorefsm_graphviz(states, transitions, outputs, image_dir, filename=get_random_filename())
    

    state, symbol, correct_next_state = missing_transition

    # Create the question text
    question_text = Question_text_generator(sequence,state,symbol)
    # Generate multiple-choice options
    possible_answers=generate_distractors(states,correct_next_state)
    correct_answer_index = possible_answers.index(correct_next_state)
    correct_answer= possible_answers[correct_answer_index]
    # Return the question data
    # return {
    #     "question": question_text,
    #     "image": fsm_graph_svg,  # Path to the image
    #     "options": possible_answers,
    #     "correct_answer": correct_answer
    # }
    labeled_options = [f"{chr(65+i)}. {option}" for i, option in enumerate(possible_answers)]
    return question_text, labeled_options, correct_answer, [fsm_graph_svg]
def N_O_build_fsm(sequence):
    n = len(sequence)
    states = [f'S{i}' for i in range(n+1)]
    transitions = {state: {} for state in states}
    outputs = {state: '0' for state in states}
    
    # Set output for the final state
    outputs[states[-1]] = '1'

    for i in range(n):
        current_state = states[i]
        next_state = states[i+1]
        char = sequence[i]

        for symbol in '01':
            if symbol == char:
                transitions[current_state][symbol] = next_state
            else:
                fallback_state = find_fallback_state(sequence, i, symbol, states)
                transitions[current_state][symbol] = fallback_state

    # Non-overlapping behavior: after reaching the final state, reset to the start state
    final_state = states[-1]
    for symbol in '01':
        transitions[final_state][symbol] = states[0]

    return states, transitions, outputs
def print_moorefsm_graphviz(states, transitions, outputs, image_dir, filename):
    dot = Digraph()

    for state in states:
        dot.node(state, label=f"{state}/{outputs[state]}")
    
    for state, trans in transitions.items():
        for symbol, next_state in trans.items():
            dot.edge(state, next_state, label=symbol)

    filepath = os.path.join(image_dir, filename)
    dot.render(filepath, format="svg", cleanup=False)

    graph_svg_filename = f"{filepath}.svg"
    return graph_svg_filename
def O_build_fsm(sequence):
    n = len(sequence)
    states = [f'S{i}' for i in range(n+1)]
    transitions = {state: {} for state in states}
    outputs = {state: '0' for state in states}
    
    # Set output for the final state
    outputs[states[-1]] = '1'

    for i in range(n):
        current_state = states[i]
        next_state = states[i+1]
        char = sequence[i]

        for symbol in '01':
            if symbol == char:
                transitions[current_state][symbol] = next_state
            else:
                fallback_state = find_fallback_state(sequence, i, symbol, states)
                transitions[current_state][symbol] = fallback_state

    # Non-overlapping behavior: after reaching the final state, reset to the start state
    final_state = states[-1]
    for symbol in '01':
        fallback_state = find_fallback_state(sequence, n, symbol, states)
        transitions[final_state][symbol] = fallback_state
    return states, transitions, outputs
def Overlapping_MooreFSM(image_dir="StateMachines/images"):
    sequences = ["101", "1010", "1101", "011", "0101", "010", "1001", "0110"]
    sequence = random.choice(sequences)
    os.makedirs(image_dir, exist_ok=True)
    
    # Build the FSM for the given sequence
    states, transitions, outputs = O_build_fsm(sequence)

    # Ask for the missing transition
    missing_transition = ask_for_completion(transitions, states)

    # Generate the FSM diagram
    fsm_graph_svg = print_moorefsm_graphviz(states, transitions, outputs, image_dir, filename=get_random_filename())
    

    state, symbol, correct_next_state = missing_transition

    # Create the question text
    question_text = Question_text_generator(sequence,state,symbol)
    # Generate multiple-choice options
    possible_answers=generate_distractors(states,correct_next_state)
    random.shuffle(possible_answers)
    correct_answer_index = possible_answers.index(correct_next_state)
    correct_answer= possible_answers[correct_answer_index]
    # Return the question data
    # return {
    #     "question": question_text,
    #     "image": fsm_graph_svg,  # Path to the image
    #     "options": possible_answers,
    #     "correct_answer": correct_answer
    # }
    labeled_options = [f"{chr(65+i)}. {option}" for i, option in enumerate(possible_answers)]
    return question_text, labeled_options, correct_answer, [fsm_graph_svg]

def ask_for_completion(transitions, states):
    missing_transition = remove_random_transition(transitions, states)
    if missing_transition:
        state, symbol, correct_next_state = missing_transition
        return (state, symbol, correct_next_state)
    return None

def generate_state_table_NONOVER(a):
    n = len(a)  # Length of the input pattern
    statetable = {}
    c=''
    d=''
    # Initialize the states S0, S1, ..., S_n
    for i in range(n + 1):
        statetable[f'S{i}'] = {str(bit): f'S{i}' for bit in range(2)}
        statetable[f'S{i}']['output'] = '0'

    # Fill in the transitions based on the input sequence 'a'
    for i in range(n):
        current_state = f'S{i}'
        next_state = f'S{i+1}'
        if i > 0:
            Opp_char=str(1-int(a[i]))
            d=c+Opp_char
            e=is_left_substring_match_from_start(d,a)
            statetable[current_state][Opp_char]=f'S{e}'

        
        c=c+a[i]
        statetable[current_state][a[i]] = next_state

    statetable[f'S{n}']['0']=f'S{0}'
    statetable[f'S{n}']['1']=f'S{0}'
    
    statetable[f'S{n}']['output'] = '1'
    #print(c)
    return statetable

def generate_state_table_OVER(a):
    n = len(a)  # Length of the input pattern
    statetable = {}
    c=''
    d=''
    # Initialize the states S0, S1, ..., S_n
    for i in range(n + 1):
        statetable[f'S{i}'] = {str(bit): f'S{i}' for bit in range(2)}
        statetable[f'S{i}']['output'] = '0'

    # Fill in the transitions based on the input sequence 'a'
    for i in range(n):
        current_state = f'S{i}'
        next_state = f'S{i+1}'
        if i > 0:
            Opp_char=str(1-int(a[i]))
            d=c+Opp_char
            e=is_left_substring_match_from_start(d,a)
            statetable[current_state][Opp_char]=f'S{e}'

        
        c=c+a[i]
        statetable[current_state][a[i]] = next_state   
        
    
    d=c[1:]+'0'
    e=is_left_substring_match_from_start(d,a)
    statetable[f'S{n}']['0']=f'S{e}'
    d=c[1:]+'1'
    e=is_left_substring_match_from_start(d,a)
    statetable[f'S{n}']['1']=f'S{e}'
    



    statetable[f'S{n}']['output'] = '1'
    #print(c)
    return statetable

def is_left_substring_match_from_start(str1, str2):
    # Iterate through `str1`, generating substrings by removing characters from the left side
    for i in range(len(str1)):
        # Current substring of `str1` generated by removing left characters
        current_substring = str1[i:]
        
        # Check if `str2` starts with the current substring
        if str2.startswith(current_substring):
            return len(current_substring)
            
    return 0

