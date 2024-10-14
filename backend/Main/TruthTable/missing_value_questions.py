import itertools
import random
import os
import schemdraw
from schemdraw.logic import table
from fpdf import FPDF
import time
from cairosvg import svg2png
from io import BytesIO


########################## Utilities ##############################################################

# Function to flip bits for options 
def flip_bits(correct_missing_values, num_flips=1):
    incorrect_option = correct_missing_values.copy()
    indices_to_flip = random.sample(range(len(incorrect_option)), num_flips)
    
    for index in indices_to_flip:
        incorrect_option[index] = 1 - incorrect_option[index]  # Flip 0 to 1 or 1 to 0
    
    return incorrect_option

# Function to generate the four options for the missing entries
def generate_options(correct_missing_values):
    options = [correct_missing_values]
    
    # Generate three incorrect options
    while len(options) < 4:
        num_flips = random.randint(1, len(correct_missing_values))  # Randomly decide how many bits to flip
        incorrect_option = flip_bits(correct_missing_values, num_flips)
        
        if incorrect_option != correct_missing_values and incorrect_option not in options:
            options.append(incorrect_option)

    random.shuffle(options)  # Shuffle options so the correct one isn't always first
    return options

# Possible operators for generating random expressions
operators = ['and', 'or', 'not']

# Function to generate a random logical expression
def generate_random_expression(num_vars):
    variables = [chr(65 + i) for i in range(num_vars)]  # A, B, C, D, E...
    expr = variables[0]
    for i in range(1, num_vars):
        op = random.choice(operators[:-1])  # Choose 'and' or 'or'
        if random.choice([True, False]):
            expr = f'{expr} {op} {variables[i]}'
        else:
            expr = f'{expr} {op} not {variables[i]}'
    if random.choice([True, False]):
        expr = f'not ({expr})'
    return expr

# Function to evaluate logical expressions
def evaluate_expression(expr, values_dict):
    for var in values_dict:
        expr = expr.replace(var, str(values_dict[var]))
    return eval(expr)

# Function to generate the truth table with 50% missing entries
def generate_truth_table_image(expr, save_path, num_vars, complete=False):
    headers = [chr(65 + i) for i in range(num_vars)]  # A, B, C, D, E...
    headers.append('Q')
    
    table_str = " | ".join(headers) + "\n"
    table_str += "|".join(["---"] * (num_vars + 1)) + "\n"
    
    all_rows = []
    missing_values = []

    for values in itertools.product([0, 1], repeat=num_vars):
        values_dict = {chr(65 + i): val for i, val in enumerate(values)}
        Q = int(evaluate_expression(expr, values_dict))
        all_rows.append((values_dict, Q))
    
    num_rows = len(all_rows)
    missing_indices = set(random.sample(range(num_rows), num_rows // 2))  # 50% missing entries
    
    for i, (values_dict, Q) in enumerate(all_rows):
        if complete or i not in missing_indices:  # Include the correct answer if complete
            table_str += " | ".join(str(values_dict[header]) for header in headers[:-1]) + f" | {Q}\n"
        else:
            table_str += " | ".join(str(values_dict[header]) for header in headers[:-1]) + " | ?\n"  # Leave missing entries
            missing_values.append(Q)
    
    # Generate the truth table image using schemdraw and save as SVG
    colfmt = 'c|' * (num_vars + 1)
    tbl_schem = table.Table(table=table_str.strip(), colfmt=colfmt)
    d = schemdraw.Drawing()
    d += tbl_schem
    d.save(save_path)
    print(f"Truth table saved as {save_path}")

    return missing_values  # Return missing values for generating options

# Function to convert SVG to PNG in-memory and return a BytesIO object with adjusted size and quality
def convert_svg_to_png(svg_content):
    png_io = BytesIO()
    svg2png(bytestring=svg_content, write_to=png_io, scale=2.0)  # Increased scale for better quality
    png_io.seek(0)  # Reset the pointer to the beginning of the BytesIO object
    return png_io

##################################### Question template ##################################################

def generate_question_missing_values():
    num_vars = random.choice([2, 3])
    expr = generate_random_expression(num_vars)

    svg_path = f'TruthTable/images/missing_value_truth_table{random.randint(1, 10000)}.svg'
    correct_missing_values = generate_truth_table_image(expr, svg_path, num_vars, complete=False)

    options = generate_options(correct_missing_values)
    question = f"Fill in the missing entries for the expression: {expr}"
    options = [str(x) for x in options]
    return (question, options, str(correct_missing_values), [svg_path])
