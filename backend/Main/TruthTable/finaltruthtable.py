import itertools
import random
import os
import schemdraw
from schemdraw.logic import table
from fpdf import FPDF
import time
import cairosvg

# Function to generate random logical expressions with a given set of variables
def generate_random_expression(variables, existing_expressions):
    operators = ['and', 'or']
    num_operators = random.randint(1, 3)  # Choose between 1 to 3 operators for complexity
    expression = random.choice(variables)
    
    for _ in range(num_operators):
        op = random.choice(operators)
        expr = random.choice(variables)
        if random.choice([True, False]):
            expr = f'not ({expr})'
        expression = f'({expression}) {op} ({expr})'
    
    # Ensure unique expression
    if expression in existing_expressions:
        existing_expressions.add(expression)  # Add the current expression to avoid infinite loop
        return generate_random_expression(variables, existing_expressions)
    
    existing_expressions.add(expression)
    return expression

# Function to evaluate logical expressions
def evaluate_expression(expr, *values):
    # Map variable names to their corresponding values
    variables = 'ABC'
    for i, value in enumerate(values):
        expr = expr.replace(variables[i], str(value))
    return eval(expr.replace('and', ' and ').replace('or', ' or ').replace('not', ' not '))

# Function to generate the truth table
def generate_truth_table(expr, num_vars):
    truth_table = []
    for values in itertools.product([0, 1], repeat=num_vars):
        Q = evaluate_expression(expr, *values)
        truth_table.append((values, Q))
    return truth_table

# Function to check if the expression matches the truth table
def does_truth_table_match_expression(expr, truth_table):
    for values, expected in truth_table:
        actual = evaluate_expression(expr, *values)
        if actual != expected:
            return False
    return True

# Function to generate the truth table image
def generate_truth_table_image(truth_table, save_path, num_vars):
    headers = [chr(65 + i) for i in range(num_vars)]  # Generate headers A, B, C, etc.
    headers.append('Q')
    
    # Create table string
    table_str = " | ".join(headers) + "\n"
    table_str += "|".join(["---"] * (num_vars + 1)) + "\n"
    
    for values, Q in truth_table:
        table_str += " | ".join(map(str, values)) + f" | {int(Q)}\n"
    
    # Ensure the column format matches the number of columns
    colfmt = 'c|' * (num_vars + 1)
    
    try:
        # Generate the truth table image using schemdraw
        tbl_schem = table.Table(table=table_str.strip(), colfmt=colfmt)
        d = schemdraw.Drawing()
        d += tbl_schem
        d.save(save_path)
        print(f"Truth table saved as {save_path}")
    except Exception as e:
        print(f"Error generating truth table image: {e}")
        print(f"Table String:\n{table_str}")
        print(f"Column Format: {colfmt}")


def generate_question_final():
    existing_expressions = set()
    svg_path = f'TruthTable/images/final_truth_table{random.randint(1, 10000)}.svg'
    question = "Is the following expression correct for the given truth table?\n"
    num_vars = random.choice([2, 3])
    variables = [chr(65 + i) for i in range(num_vars)]
    expr = generate_random_expression(variables, existing_expressions)
    correct_answer = ""

    # Generate true questions
    if random.randint(1, 2) == 1:
        # Generate and check the truth table
        truth_table = generate_truth_table(expr, num_vars)
        
        if does_truth_table_match_expression(expr, truth_table):
            generate_truth_table_image(truth_table, svg_path, num_vars)
            correct_answer = "True"
    else:
        valid_expr = generate_random_expression(variables, existing_expressions)
        truth_table = generate_truth_table(valid_expr, num_vars)

        if not does_truth_table_match_expression(expr, truth_table):
            generate_truth_table_image(truth_table, svg_path, num_vars)
            correct_answer = "False"

    return (question + expr, ["True", "False"], correct_answer, [svg_path])
