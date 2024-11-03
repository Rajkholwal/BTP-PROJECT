import random
import os
import itertools
import schemdraw
import schemdraw.logic as logic
from schemdraw.parsing import logicparse

################################## UTILITIES ##############################################################

def replace_operators(expr):
    """Replace logical operators with symbols for better readability."""
    return expr.replace("not", "!").replace(" and", "&").replace(" or", "|").replace("NOT", "!").replace(" AND", "&").replace(" OR", "|")

def get_svg_from_file(filepath):
    """Read the SVG content from a file."""
    with open(filepath, "r") as f:
        return f.read()

############################## FOR THE AVOID DUPLICATE QUESTION ##############################
def generate_question(level):
    """Randomly generate a question of either type, ensuring no duplicates."""
    global previous_questions

    for _ in range(10):  # Try a few times to avoid duplicates
        if random.choice([True, False]):
            question_data = generate_equivalent_circuit_question()
        else:
            question, options, correct_answer, svg_path = generate_simple_gate_operation_question()
            question_data = (question, options, correct_answer, [get_svg_from_file(svg_path)])
        
        question_text = question_data[0]
        
        # If the question hasn't been asked before, return it
        if question_text not in previous_questions:
            previous_questions.add(question_text)
            return question_data

    # If all attempts produced duplicates, force generate a new question
    return generate_question(level)

# Define possible gates (excluding XOR, NAND, and NOR)
gates = ['and', 'or', 'not']

previous_questions = set()  # Set to track previously generated questions

def random_expression(variables, num_gates):
    """Generate a random logic expression with a given number of gates and variables."""
    if num_gates == 0:
        return random.choice(variables)
    
    gate = random.choice(gates)
    expr = '('
    
    if gate == 'not':
        expr += f'not {random_expression(variables, num_gates - 1)}'
    else:
        expr += f'{random_expression(variables, num_gates - 1)} {gate} {random_expression(variables, num_gates - 1)}'
    
    expr += ')'
    return expr

def eval_expr(expr, values):
    """Evaluate the expression by substituting the values."""
    for var, val in values.items():
        expr = expr.replace(var, str(val))
    return eval(expr)

###################### Algo for the equivalent circuit identification #######################
def generate_truth_table(expr, variables):
    """Generate a truth table for the given expression using itertools."""
    truth_table = []
    
    # Generate all possible combinations of input values
    for combination in itertools.product([0, 1], repeat=len(variables)):
        values = dict(zip(variables, combination))
        try:
            output = eval_expr(expr, values)
        except Exception as e:
            print(f"Error evaluating expression '{expr}': {e}")
            continue  # Skip to the next combination on error
            
        truth_table.append((combination, int(output)))
    
    return truth_table

def create_and_save_diagram(expression, file_path):
    """Create a logic circuit diagram from the expression and save it as SVG."""
    try:
        d = logicparse(expression, outlabel=r'$\text{Output}$')
        d.save(file_path)
    except Exception as e:
        print(f"Error creating diagram for expression '{expression}': {e}")

def compare_truth_tables(table1, table2):
    """Compare two truth tables for equivalence."""
    if len(table1) != len(table2):
        return False  # Different lengths indicate they can't be equivalent

    # Compare each entry in the truth tables
    for row1, row2 in zip(table1, table2):
        if row1[1] != row2[1]:  # Compare the outputs
            return False

    return True  # All outputs match, so the expressions are equivalent

####################### INPUT OUTPUT ALGO ###############################

def generate_simple_gate_operation_question():
    """Generate a question involving a simple gate operation and save the gate image."""
    gates = ['AND', 'OR', 'NOT']
    gate_type = random.choice(gates)
    
    if gate_type == 'NOT':
        input_values = [random.choice([0, 1])]
    else:
        input_values = [random.choice([0, 1]) for _ in range(2)]
    
    if gate_type == 'AND':
        output = int(all(input_values))
    elif gate_type == 'OR':
        output = int(any(input_values))
    elif gate_type == 'NOT':
        output = int(not input_values[0])
    
    d = schemdraw.Drawing()
    d.config(fontsize=8)
    
    if gate_type == 'AND':
        gate = logic.And(inputs=2)
        d += gate
    elif gate_type == 'OR':
        gate = logic.Or(inputs=2)
        d += gate
    elif gate_type == 'NOT':
        gate = logic.Not()
        d += gate
    
    svg_path = f'LogicGates/images/{gate_type}_Gate.svg'
    d.save(svg_path)
    
    options = ['0', '1']
    correct_answer = str(output)
    random.shuffle(options)
    
    question = f"What is the output of the {gate_type} gate with inputs {', '.join(map(str, input_values))}?"
    if gate_type == 'NOT':
        question = f"What is the output of the {gate_type} gate with input {input_values[0]}?"
    
    return question, options, correct_answer, svg_path

def generate_equivalent_circuit_question():
    """Generate a question involving equivalent circuits using truth tables, ensuring they are not equivalent."""
    variables = [chr(ord('a') + i) for i in range(random.randint(2, 3))]  # Generate 2 to 3 variables
    
    # Generate the first random expression
    expr1 = random_expression(variables, random.randint(2, 3))
    
    # Generate a second expression that is intended to be different
    expr2 = random_expression(variables, random.randint(2, 3))
    while expr2 == expr1 or compare_truth_tables(generate_truth_table(expr1, variables), generate_truth_table(expr2, variables)):
        # Keep generating expr2 until it is different from expr1 and has a different truth table
        expr2 = random_expression(variables, random.randint(2, 3))
    
    # Create SVG diagrams for each expression
    svg_path1 = f'LogicGates/images/random_logic_circuit_{random.randint(1, 10000)}_1.svg'
    svg_path2 = f'LogicGates/images/random_logic_circuit_{random.randint(1, 10000)}_2.svg'

    create_and_save_diagram(expr1, svg_path1)
    create_and_save_diagram(expr2, svg_path2)

    # Generate truth tables for both expressions for final verification
    truth_table1 = generate_truth_table(expr1, variables)
    truth_table2 = generate_truth_table(expr2, variables)

    # Since we constructed them to differ, this should ideally be False, but we check again to confirm
    equivalent = compare_truth_tables(truth_table1, truth_table2)

    # Prepare the question
    question = f"Are these two circuits equivalent?\nExpression 1: {replace_operators(expr1)}\nExpression 2: {replace_operators(expr2)}"
    options_text = ["True", "False"]
    correct_answer = 'False' if not equivalent else 'True'  # Should always be 'False'

    return (question, options_text, correct_answer, [get_svg_from_file(x) for x in [svg_path1, svg_path2]])
