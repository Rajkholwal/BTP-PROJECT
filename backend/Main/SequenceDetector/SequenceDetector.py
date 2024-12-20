from graphviz import Digraph
import random
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

def process_sequence_OVER(a, b):
    statetable = generate_state_table_OVER(a)
    #print(statetable)
    out=''
    state='S0'
    for char in b:
        state = statetable[state][char]
        out+=str(statetable[state]['output'])
       # print(f"Current state: {state}, Output: {statetable[state]['output']}")
    
    #print(f"Final state: {state}, Output: {statetable[state]['output']}")
    # Generate the FSM PDF after processing
    print(f'Output: {out}')
    return out
    # generate_fsm_pdf(statetable)

def process_sequence_NONOVER(a, b):
    statetable = generate_state_table_NONOVER(a)
    #print(statetable)
    out=''
    state='S0'
    for char in b:
        state = statetable[state][char]
        out+=str(statetable[state]['output'])
       # print(f"Current state: {state}, Output: {statetable[state]['output']}")
    
    #print(f"Final state: {state}, Output: {statetable[state]['output']}")
    # Generate the FSM PDF after processing
    print(f'Output: {out}')
    return out
    # generate_fsm_pdf(statetable)

def flip_bit(input_seq):
    seq_list = list(input_seq)
    while True:
        flip_idx = random.randint(2, len(seq_list) - 1)
        
        original_bit = seq_list[flip_idx]
        seq_list[flip_idx] = '1' if seq_list[flip_idx] == '0' else '0'
        
        
        if (flip_idx > 0 and seq_list[flip_idx] == '1' and seq_list[flip_idx - 1] == '1') or \
           (flip_idx < len(seq_list) - 1 and seq_list[flip_idx] == '1' and seq_list[flip_idx + 1] == '1'):
            
            seq_list[flip_idx] = original_bit
        else:
            break
    
    return ''.join(seq_list)

def generate_unique_flip(correct_answer, possible_answers):
    while True:
        flipped = flip_bit(correct_answer)
        if flipped not in possible_answers:
            return flipped

def generate_questions(level):
    sequences = ["101", "1010", "0101", "1101", "010","011","110","0110","1001","1011"]
    sequence = random.choice(sequences)
    strings = ["101101101010", "011011010101", "011011010110", "011010100101", "010101001011", "011010110110", "100110010101", "110110101011","101101101101","110101011101"]
    string=random.choice(strings)
    # while True:
    #     string1= random.choice(strings)
    #     string2=random.choice(strings)
    #     if (string1!=string2):
    #         break
    
    
    machine_types=["Overlapping","Nonoverlapping"]
    machine_type=random.choice(machine_types)
    
    correct_answer= process_sequence_OVER(sequence,string) if machine_type=="Overlapping" else process_sequence_NONOVER(sequence,string)
    option1 = generate_unique_flip(correct_answer, [correct_answer])
    option2 = generate_unique_flip(correct_answer, [correct_answer, option1])
    option3 = generate_unique_flip(correct_answer, [correct_answer, option1, option2])
    possible_answer = [correct_answer, option1, option2, option3]
    random.shuffle(possible_answer)
    # correct_answer_index = possible_answer.index(correct_answer)
    # labeled_options = [f"{chr(65+i)}. {option}" for i, option in enumerate(possible_answer)]
    question_text=f"For the input sequence {sequence} and the input string {string}, what is the output string for {machine_type}?"
    return (question_text, possible_answer, correct_answer)