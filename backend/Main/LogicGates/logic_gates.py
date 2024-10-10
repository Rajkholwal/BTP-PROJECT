import random
import os
import schemdraw
import schemdraw.logic as logic
from schemdraw.parsing import logicparse

# Define possible gates
gates = ['and', 'or', 'nand', 'nor', 'xor', 'xnor', 'not']

def random_expression(variables, num_gates):
    """Generate a random logic expression with a given number of gates and variables."""
    if num_gates == 0:
        return random.choice(variables)
    
    gate = random.choice(gates)
    expr = '('
    
    if gate == 'not':
        expr += f'{gate} {random_expression(variables, num_gates - 1)}'
    else:
        expr += f'{random_expression(variables, num_gates - 1)} {gate} {random_expression(variables, num_gates - 1)}'
    
    expr += ')'
    return expr

def replace_operators(expr):
    return expr.replace("not", "!").replace(" and", " x").replace(" or", " +").replace("NOT", "!").replace(" AND", " x").replace(" OR", " +")

def create_and_save_diagram(expression, file_path):
    """Create a logic circuit diagram from the expression and save it as SVG."""
    try:
        d = logicparse(expression, outlabel=r'$\text{Output}$')
        d.save(file_path)
    except Exception as e:
        print(f"Error creating diagram for expression '{expression}': {e}")

def generate_simple_gate_operation_question():
    """Generate a question involving a simple gate operation and save the gate image."""
    gates = ['AND', 'OR', 'NOT', 'NAND', 'NOR', 'XOR']
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
    elif gate_type == 'NAND':
        output = int(not all(input_values))
    elif gate_type == 'NOR':
        output = int(not any(input_values))
    elif gate_type == 'XOR':
        output = int(sum(input_values) % 2 == 1)
    
    d = schemdraw.Drawing()
    d.config(fontsize=8)
    
    if gate_type == 'AND':
        gate = logic.And(inputs=2)
        d += gate
    elif gate_type == 'OR':
        gate = logic.Or(inputs=2)
        d += gate
    elif gate_type == 'NAND':
        gate = logic.Nand(inputs=2)
        d += gate
    elif gate_type == 'NOR':
        gate = logic.Nor(inputs=2)
        d += gate
    elif gate_type == 'XOR':
        gate = logic.Xor(inputs=2)
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

def get_svg_from_file(filepath):
    with open(filepath, "r") as f:
        return f.read()

def generate_question(level):
    variables = [chr(ord('a') + i) for i in range(random.randint(1, 3))]

    if random.choice([True, False]):
        if random.random() < 0.5:
            base_expr = random_expression(variables, random.randint(1, 3))
            expr1 = base_expr
            expr2 = base_expr
        else:
            base_expr = random_expression(variables, random.randint(1, 3))
            expr1 = base_expr
            expr2 = random_expression(variables, random.randint(1, 3))

        svg_path1 = f'LogicGates/images/random_logic_circuit_{random.randint(1, 10000)}_1.svg'
        svg_path2 = f'LogicGates/images/random_logic_circuit_{random.randint(1, 10000)}_2.svg'

        create_and_save_diagram(expr1, svg_path1)
        create_and_save_diagram(expr2, svg_path2)

        question = f"Are these two circuits equivalent?\nExpression 1: {replace_operators(expr1)}\nExpression 2: {replace_operators(expr2)}"
        options_text = ["True", "False"]
        correct_answer = 'True' if expr1 == expr2 else 'False'
        return (question, options_text, correct_answer, [get_svg_from_file(x) for x in [svg_path1, svg_path2]])
    else:
        question, options, correct_answer, svg_path = generate_simple_gate_operation_question()
        return (question, options, correct_answer, [get_svg_from_file(svg_path)])

# Example usage
# question_data = generate_question(level=1)
# print(question_data)
