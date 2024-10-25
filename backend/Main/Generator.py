import random
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

import LogicGates.logic_gates
import Number_System.numerSystemFinal
import Boolean_Algebra.booleanAlgebraFinal
import FlipFlops.flipflops
import StateMachines.fsm
import SequenceDetector.SequenceDetector
import LogicGates
import TruthTable
import StateMachines
import io
import os
import svg2png

import TruthTable.generator
pdf_folder = "./PDF"

# Function to convert SVG to PNG in-memory and return a BytesIO object with adjusted size and quality
def convert_svg_to_png(svg_content):
    png_io = io.BytesIO()
    svg2png(bytestring=svg_content, write_to=png_io, scale=2.0)  # Increased scale for better quality
    png_io.seek(0)  # Reset the pointer to the beginning of the BytesIO object
    return png_io

# Here we generate question based on tags and then generate a PDF
def generate_pdf(num_questions, level, tags):
    filename = f"questions_{num_questions}_level_{level}.pdf"
    document_title = f"Generated Questions - Level {level}"

    # Create PDF
    pdf_path = os.path.join(pdf_folder, filename)
    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer)
    c.setTitle(document_title)

    # Set up initial depth
    depth = 700

    # Number of questions per page
    questions_per_page = 5

    # Convert num_questions to an integer
    num_questions = int(num_questions)
    right_padding = 50

    for question_num in range(num_questions):
        # Check if a new page is needed
        if question_num > 0 and question_num % questions_per_page == 0:
            c.showPage()  # Start a new page
            depth = 700  # Reset depth for the new page

        question, options, answer = generate_question(level, tags)
        question_x = 100
        option_x = 120
        question_1 = ""
        question_2 = ""
        if len(question) >= 70:
            question_1 = question[:70]
            question_2 = question[70:]
            c.drawString(question_x, depth, f"Q{question_num + 1}: {question_1}")
            depth -= 20
            c.drawString(question_x, depth, f"{question_2}")
        else:
            c.drawString(question_x, depth, f"Q{question_num + 1}: {question}")

        depth -= 20

        for option in options:
            c.drawString(option_x, depth, f" {option}")
            depth -= 20
            
        # depth -= 20
        c.drawString(option_x, depth, f"Correct answer: {answer}")
        depth -= 30

    # Saving the file
    c.save()
    with open(pdf_path, 'wb') as pdf_file:
            pdf_file.write(pdf_buffer.getvalue())
    print(f"PDF '{filename}' generated successfully.")


def generate_question(level,tags):
    print(level,tags)
    random_list = []
    tag1 = "Number-System"
    tag2 = "Boolean-algebra"
    tag3 = "Logic-Gates"
    tag4 = "Flip-flops"
    tag5 = "SequenceDetector"
    tag6 = "Truth-Tables"
    tag7 = "State-Machine"
    
    print("tags are")
    print(tags)
    for tag in tags:
        print(tag)
        if tag == tag1:
            random_list.append(1)
        elif tag == tag2:
            random_list.append(2)
        elif tag == tag3:
            random_list.append(3)
        elif tag == tag4:
            random_list.append(4)
        elif tag == tag5:
            random_list.append(5)
        elif tag == tag6:
            random_list.append(6)
        elif tag == tag7:
            random_list.append(7)

    flag = random.choice(random_list)
    
    print("It goes like..")
    # print(tags)
    print(random_list)
    if flag == 1:
        return Number_System.numerSystemFinal.generate_question_number_system(level)
    elif flag == 2:
        return Boolean_Algebra.booleanAlgebraFinal.generate_question_boolean_algebra(level)
    elif flag == 3:
        return LogicGates.logic_gates.generate_question(level)
    elif flag == 4:
        return FlipFlops.flipflops.generate_question_flipflops(level)
    elif flag == 5:
        return SequenceDetector.SequenceDetector.generate_questions(level)
    elif flag == 6:
        return TruthTable.generator.generate_question_boolean_algebra()
    elif flag == 7:
        return StateMachines.fsm.genearte_question_FSM(level)
