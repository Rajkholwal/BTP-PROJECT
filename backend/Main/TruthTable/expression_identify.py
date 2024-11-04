import itertools
import random
import os
import schemdraw
from schemdraw.logic import table
import matplotlib
matplotlib.use('Agg')

# Utilities

# Function to generate distractor options
def distractors_options(correct_expr, variables, used_expressions):
    operators = ['and', 'or']
    
    # Create a list of possible modifications to the expression
    possible_modifications = []

    # Generate possible distractors by negating each variable
    for var in variables:
        modified_expr = correct_expr.replace(var, f'not ({var})') if f'not ({var})' not in correct_expr else correct_expr.replace(f'not ({var})', var)
        if modified_expr != correct_expr and modified_expr not in used_expressions:
            possible_modifications.append(modified_expr)

    # Generate possible distractors by changing each operator
    split_expr = correct_expr.split()
    for i, part in enumerate(split_expr):
        if part in operators:
            for operator in operators:
                if operator != part:
                    modified_expr = ' '.join(split_expr[:i] + [operator] + split_expr[i+1:])
                    if modified_expr != correct_expr and modified_expr not in used_expressions:
                        possible_modifications.append(modified_expr)

    # Randomly select a distractor from the possible modifications
    if possible_modifications:
        new_expr = random.choice(possible_modifications)
        used_expressions.add(new_expr)
        return new_expr

    # If no valid distractor was found, return a simple negation
    return f'not ({correct_expr})' if 'not' not in correct_expr else correct_expr.replace('not ', '')

def generate_random_expression(variables):
    operators = ['and', 'or']
    num_operators = random.randint(1, 3)  # Choose between 1 to 3 operators for complexity
    expression = random.choice(variables)

    for _ in range(num_operators):
        op = random.choice(operators)
        expr = random.choice(variables)
        if random.choice([True, False]):
            expr = f'not ({expr})'
        expression = f'({expression}) {op} ({expr})'

    return expression

# Function to evaluate logical expressions
def evaluate_expression(expr, *values):
    # Map variable names to their corresponding values
    variables = 'ABC'
    for i, value in enumerate(values):
        expr = expr.replace(variables[i], str(value))
    return eval(expr.replace('and', ' and ').replace('or', ' or ').replace('not', ' not '))

# Function to generate the truth table and save as an image
def generate_truth_table_image(expr, save_path, num_vars):
    headers = [chr(65 + i) for i in range(num_vars)]  # Generate headers A, B, C, etc.
    headers.append('Q')

    table_str = " | ".join(headers) + "\n"
    table_str += "|".join(["---"] * (num_vars + 1)) + "\n"

    for values in itertools.product([0, 1], repeat=num_vars):
        Q = evaluate_expression(expr, *values)
        table_str += " | ".join(map(str, values)) + f" | {int(Q)}\n"

    # Generate the truth table image using schemdraw
    colfmt = 'c|' * (num_vars + 1)
    tbl_schem = table.Table(table=table_str.strip(), colfmt=colfmt)
    d = schemdraw.Drawing()
    d += tbl_schem
    d.save(save_path)
    print(f"Truth table saved as {save_path}")

# Question Template Function
def generate_question_expression_identify():
    generated_expressions = set()  # Set to track previously generated questions

    def create():
        num_vars = random.choice([2, 3])  # Randomly choose number of variables (2 to 3)

        # Generate a unique random expression
        while True:
            variables = [chr(65 + i) for i in range(num_vars)]
            expr = generate_random_expression(variables)
            if expr not in generated_expressions:
                generated_expressions.add(expr)  # Add to the set of used questions
                break

        # Generate options ensuring they are unique
        used_expressions = {expr}  # Track used expressions for the options
        options = []
        
        while len(options) < 3:
            distractor = distractors_options(expr, variables, used_expressions)
            if distractor not in options:  # Ensure distinct incorrect options
                options.append(distractor)

        options.append(expr)  # Add the correct expression
        random.shuffle(options)  # Shuffle the options

        # Generate the truth table and save it as an SVG
        svg_path = f'TruthTable/images/expression_identify_truth_table_{random.randint(1, 10000)}.svg'
        generate_truth_table_image(expr, svg_path, num_vars)

        return ("Which expression corresponds to the given truth table?", options, expr, [svg_path])

    return create()
