import random

from .missing_value_questions import generate_question_missing_values
from .finaltruthtable import generate_question_final
from .expression_identify import generate_question_expression_identify

question_map = {
    1: generate_question_missing_values,
    2: generate_question_final,
    3: generate_question_expression_identify,
}

def get_svg_from_file(filepath):
    with open(filepath, "r") as f:
        return f.read()

def generate_question_boolean_algebra():
    q,o,a,image_files = question_map[random.randint(1,3)]()
    return q,o,a,[get_svg_from_file(file) for file in image_files]
