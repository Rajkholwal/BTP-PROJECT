# import random

# questions = [
#     {
#         "question": " RTL is primarily concerned with defining the flow of signals between",
#         "options": ["A. Registers", "B. Clock", "C. Inverters", "D. None of the above"],
#         "correct_answer": "A. Registers",
#     },
#     {
#         "question": " RTL Design only contains combinational circuits and does not include any sequential component",
#         "options": ["A. True", "B. False"],
#         "correct_answer": "B. False",
#     },
#     {
#         "question": " Maximum clock frequency is independent of critical path",
#         "options": ["A. True", "B. False"],
#         "correct_answer": "B. False",
#     },
#     {
#         "question": "32-bit IEEE 754 floating point representation adds a bias of",
#         "options": ["A. 127 to mantissa", "B. 127 to exponent", "C. 128 to mantissa", "D. 128 to exponent"],
#         "correct_answer": "B. 127 to exponent",
#     },
#     {
#         "question": "The smallest and largest number that can be represented by IEEE single precision format is",
#         "options": ["A. 10^-126 and 10^127", "B. 10^-127 and 10^127", "C. 2^-126 and 2^127", "D. 2^-127 and 2^127"],
#         "correct_answer": "C. 2^-126 and 2^127",
#     },
#     {
#         "question": "A register capable of increasing or decreasing it's contents is",
#         "options": ["A. Counter", "B. Decoder", "C. Multiplexer", "D. Demultiplexer"],
#         "correct_answer": "A. Counter",
#     },
#     {
#         "question": "What type of number syste is represented by base 8",
#         "options": ["A. Decimal", "B. Binary", "C. Octal", "D. Hexadecimal"],
#         "correct_answer": "C. Octal",
#     },
#     {
#         "question": "Which coding scheme is used in computer to represent data internally",
#         "options": ["A. Decimal", "B. Integral", "C. Binary", "D. None"],
#         "correct_answer": "C. Binary",
#     },
#     {
#         "question": "Which among the following is not a logic gate",
#         "options": ["A. XOR", "B. AND", "C. OR", "D. NOT"],
#         "correct_answer": "A. XOR",
#     },
#     {
#         "question": "A register capable of increasing or decreasing it's contents is",
#         "options": ["A. Counter", "B. Decoder", "C. Multiplexer", "D. Demultiplexer"],
#         "correct_answer": "A. Counter"
#     },
#     {
#         "question": "For a particular design of multiplication unit with 6 bit multiplicand and 3 bit multiplier What is the worst case number of adders required for the design and what would be the size of those adders ?",
#         "options": ["A. 9 Adders; Size 3 bits", "B. 3 Adders; Size 9 bits", "C. 6 Adders; Size 6 bits", "D. 3 Adders; Size 6 bits"],
#         "correct_answer": "B. 3 Adders; Size 9 bits"
#     },
#     {
#         "question": "How many 4 bit adders are required to design a 16 bit carry select adder? Assume equal groups of sizes of 4 bit adder. Inputs are A[15:0], B[15:0] and C0.",
#         "options": ["A. 8", "B. 16", "C. 15", "D. 17"],
#         "correct_answer": "A. 8"
#     },
#     {
#         "question": "Which of the following represents the characteristic equations",
#         "options": ["A. AQ’ + B’Q", "B. AB’ + Q’", "C. A’B’ + ,Q’", "D. A’Q + B’Q"],
#         "correct_answer": "A. AQ’ + B’Q"
#     }
    
# ]
# # returns a question statement and answer option
# def generate_question_theory(level):

#     # if level == 1:
#     #     filtered_question = list(filter(lambda questions: questions[level] == 1, questions))
#     #     selected_question = random.choice(questions)
#     # else:
#     #     selected_question = random.choice(questions)
#     #     filtered_question = list(filter(lambda questions: questions.level == "2", questions))
#     selected_question = random.choice(questions)

#     question_text = selected_question["question"]
#     options = selected_question["options"]
#     correct_answer = selected_question["correct_answer"]
#     return question_text, options, correct_answer

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

def generate_questions():
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