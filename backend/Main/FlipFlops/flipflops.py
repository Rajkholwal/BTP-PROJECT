import random

# level - 1 questions
questions = [
    {
        "question": "Which condition is shown in J-K flip flop as no changes next state from the present state",
        "options": ["A. J = 0, K = 0", "B. J = 0, K = 1", "C. J = 1, K = 0", "D. J = 1, K = 1"],
        "correct_answer": "A. J = 0, K = 0",
    },
    {
        "question": "D flip flip can be made from a J-L flip flop by making",
        "options": ["A. J=K","B. J=K=1","C. J=0 K=1","D. J=K\'"],
        "correct_answer": "D. J=K\'",
    }
]

def generate_question_flipflops(level):
    selected_question = random.choice(questions)
    question_text = selected_question['question']
    options = selected_question['options']
    correct_answer = selected_question['correct_answer']
    return question_text, options, correct_answer