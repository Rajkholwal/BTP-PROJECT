import random

questions = [
    {
        "question": " RTL is primarily concerned with defining the flow of signals between",
        "options": ["A. Registers", "B. Clock", "C. Inverters", "D. None of the above"],
        "correct_answer": "A. Registers",
    },
    {
        "question": " RTL Design only contains combinational circuits and does not include any sequential component",
        "options": ["A. True", "B. False"],
        "correct_answer": "B. False",
    },
    {
        "question": " Maximum clock frequency is independent of critical path",
        "options": ["A. True", "B. False"],
        "correct_answer": "B. False",
    },
    {
        "question": "32-bit IEEE 754 floating point representation adds a bias of",
        "options": ["A. 127 to mantissa", "B. 127 to exponent", "C. 128 to mantissa", "D. 128 to exponent"],
        "correct_answer": "B. 127 to exponent",
    },
    {
        "question": "The smallest and largest number that can be represented by IEEE single precision format is",
        "options": ["A. 10^-126 and 10^127", "B. 10^-127 and 10^127", "C. 2^-126 and 2^127", "D. 2^-127 and 2^127"],
        "correct_answer": "C. 2^-126 and 2^127",
    },
    {
        "question": "A register capable of increasing or decreasing it's contents is",
        "options": ["A. Counter", "B. Decoder", "C. Multiplexer", "D. Demultiplexer"],
        "correct_answer": "A. Counter",
    },
    {
        "question": "What type of number syste is represented by base 8",
        "options": ["A. Decimal", "B. Binary", "C. Octal", "D. Hexadecimal"],
        "correct_answer": "C. Octal",
    },
    {
        "question": "Which coding scheme is used in computer to represent data internally",
        "options": ["A. Decimal", "B. Integral", "C. Binary", "D. None"],
        "correct_answer": "C. Binary",
    },
    {
        "question": "Which among the following is not a logic gate",
        "options": ["A. XOR", "B. AND", "C. OR", "D. NOT"],
        "correct_answer": "A. XOR",
    },
    {
        "question": "A register capable of increasing or decreasing it's contents is",
        "options": ["A. Counter", "B. Decoder", "C. Multiplexer", "D. Demultiplexer"],
        "correct_answer": "A. Counter"
    },
    {
        "question": "For a particular design of multiplication unit with 6 bit multiplicand and 3 bit multiplier What is the worst case number of adders required for the design and what would be the size of those adders ?",
        "options": ["A. 9 Adders; Size 3 bits", "B. 3 Adders; Size 9 bits", "C. 6 Adders; Size 6 bits", "D. 3 Adders; Size 6 bits"],
        "correct_answer": "B. 3 Adders; Size 9 bits"
    },
    {
        "question": "How many 4 bit adders are required to design a 16 bit carry select adder? Assume equal groups of sizes of 4 bit adder. Inputs are A[15:0], B[15:0] and C0.",
        "options": ["A. 8", "B. 16", "C. 15", "D. 17"],
        "correct_answer": "A. 8"
    },
    {
        "question": "Which of the following represents the characteristic equations",
        "options": ["A. AQ’ + B’Q", "B. AB’ + Q’", "C. A’B’ + ,Q’", "D. A’Q + B’Q"],
        "correct_answer": "A. AQ’ + B’Q"
    }
    
]
# returns a question statement and answer option
def generate_question_theory(level):

    # if level == 1:
    #     filtered_question = list(filter(lambda questions: questions[level] == 1, questions))
    #     selected_question = random.choice(questions)
    # else:
    #     selected_question = random.choice(questions)
    #     filtered_question = list(filter(lambda questions: questions.level == "2", questions))
    selected_question = random.choice(questions)

    question_text = selected_question["question"]
    options = selected_question["options"]
    correct_answer = selected_question["correct_answer"]
    return question_text, options, correct_answer