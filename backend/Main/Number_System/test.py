import random
def generate_binary_options(binary_number):
    options = set()
    options.add(binary_number)

    while len(options) < 4:
        answer_list = list(binary_number)
        flip_index = random.randint(0,len(answer_list)-1)
        if answer_list[flip_index] == '1':
            answer_list[flip_index] = '0'
        else:
            answer_list[flip_index] = '1'
        options.add(''.join(answer_list))

    option_list = list(options)
    random.shuffle(option_list)
    
    idx = 'A'
    correct_option = "error-0"
    new_list = []

    for option in option_list:
        new_option = idx+". "+option
        if option == binary_number:
            correct_option = new_option
        new_list.append(new_option)
        idx = chr(ord(idx) + 1)
        

    return new_list,correct_option

def generate_octal_options(octal_number):
    options = set()
    options.add(octal_number)

    while len(options) < 4:
        answer_list = list(octal_number)
        flip_index = random.randint(0, len(answer_list) - 1)
        new_digit = random.randint(0, 7)  # Generate a random octal digit
        answer_list[flip_index] = str(new_digit)
        options.add(''.join(answer_list))

    option_list = list(options)
    random.shuffle(option_list)
    
    idx = 'A'
    correct_option = "error-0"
    new_list = []

    for option in option_list:
        new_option = idx + ". " + option
        if option == octal_number:
            correct_option = new_option
        new_list.append(new_option)
        idx = chr(ord(idx) + 1)

    return new_list, correct_option
    
def generate_decimal_options(decimal_number):
    options = set()
    decimal_number = str(decimal_number)
    options.add(decimal_number)

    while len(options) < 4:
        answer_list = list(str(decimal_number))
        flip_index = random.randint(0, len(answer_list) - 1)
        new_digit = random.randint(0, 9)  # Generate a random decimal digit
        answer_list[flip_index] = str(new_digit)
        options.add(''.join(answer_list))

    option_list = list(options)
    random.shuffle(option_list)
    
    idx = 'A'
    correct_option = "error-0"
    new_list = []

    for option in option_list:
        new_option = idx + ". " + str(option)
        if option == str(decimal_number):
            correct_option = new_option
        new_list.append(new_option)
        idx = chr(ord(idx) + 1)

    return new_list, correct_option

def generate_hexadecimal_options(hexadecimal_number):
    options = set()
    options.add(hexadecimal_number)

    while len(options) < 4:
        answer_list = list(hexadecimal_number)
        flip_index = random.randint(0, len(answer_list) - 1)
        new_digit = random.choice('0123456789ABCDEF')  # Generate a random hexadecimal digit
        answer_list[flip_index] = new_digit
        options.add(''.join(answer_list))

    option_list = list(options)
    random.shuffle(option_list)
    
    idx = 'A'
    correct_option = "error-0"
    new_list = []

    for option in option_list:
        new_option = idx + ". " + option
        if option == hexadecimal_number:
            correct_option = new_option
        new_list.append(new_option)
        idx = chr(ord(idx) + 1)

    return new_list, correct_option


# utilities
def generate_random_binary(length=8, decimal_places=4):
    # Generate a random integer with the specified length
    rand_int = random.randint(0, 2**length - 1)

    # Convert the integer to binary with the specified number of decimal places
    binary_str = format(rand_int, f'0{length}b')
    
    # Insert the decimal point
    binary_str = f"{binary_str[:-decimal_places]}.{binary_str[-decimal_places:]}"

    return binary_str

def binary_to_decimal_binary(binary_str):
    decimal = 0
    ans = 0
    if binary_str[0] == '1':
        ans = ans + (2**3) 
    if binary_str[1] == '1':
        ans = ans + (2**2) 
    if binary_str[2] == '1':
        ans = ans + (2**1) 
    if binary_str[3] == '1':
        ans = ans + (2**0) 
    if binary_str[5] == '1':
        ans = ans + (2**-1) 
    if binary_str[6] == '1':
        ans = ans + (2**-2) 
    if binary_str[7] == '1':
        ans = ans + (2**-3) 
    if binary_str[8] == '1':
        ans = ans + (2**-4) 
    return ans

# Question 1
def generate_question__binary_arithimetic(level):
    binary_number = generate_random_binary()
    question_text = f"The decimal equivalent of {binary_number} is?"
    correct_answer = binary_to_decimal_binary(binary_number)
    options, correct_answer = generate_decimal_options(correct_answer)
    return question_text,options,correct_answer

if __name__ == "__main__":
    # Example usage:
    ans = generate_question__binary_arithimetic(1)
    print(ans)