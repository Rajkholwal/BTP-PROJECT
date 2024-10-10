
def 

def main():
    number_of_questions = input("Enter the number of questions and level:")
    num = int(number_of_questions)
    
    for _ in range(num):
        conversion_start, start_value, conversion_end, correct_answer = generate_question_conversion(1)
        user_answer = input(f"What is the {conversion_end} representation of {start_value} (in {conversion_start})? ").strip()
        UA = str(user_answer)
        CA = str(correct_answer)

        if UA == CA:
            print("Correct!\n")
        else:
            print(f"Wrong. The correct answer is {correct_answer}.\n")



if __name__ == "__main__":
    main()