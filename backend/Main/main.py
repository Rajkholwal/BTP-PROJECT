# function which generates the question
import Generator

class question_tags:
    def __init__(self, text, tags):
        self.text = text
        self.tags = tags

tags = [
    question_tags("tag-1", ["Number-System"]),
    question_tags("tag-2", ["Boolean-algebra"]),
    question_tags("tag-3", ["Logic-Gates"]),
    question_tags("tag-4", ["Flip-flops"]),
    question_tags("tag-5",["Theory"]),
    question_tags("tag-6",["Truth-Tables"]),
    question_tags("tag-7", ["State-Machine"]),
    # Add more questions with different tags
]
def main(selected_tags,num_questions,level):
    print(selected_tags)
    print(num_questions)
    print(level)
    Generator.generate_pdf(num_questions,level,selected_tags)
    

if __name__ == "__main__":
    print("here")

import os

def create_python_file(filename):
    if not filename.endswith('.py'):
        filename += '.py'
    cwd = os.getcwd()
    folder_path = os.path.join(cwd, filename[:-3])
    os.makedirs(folder_path, exist_ok=True)
    filepath = os.path.join(folder_path, filename)

    if os.path.exists(filepath):
        print(f"File '{filename}' already exists.")
        return

    code = """
# def generate_question_"""+filename+"""(level):
# return q,o,a

# if __name__ == "__main__":
# ans = generate_question_"""+filename+"""(1)
# print(ans)
"""
    with open(filepath, 'w') as f:
        f.write(code)
