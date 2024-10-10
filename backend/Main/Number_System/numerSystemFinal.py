import random
import struct

# Utilites
def generate_binary_number(length):
    binary_number = ''.join(random.choice('01') for _ in range(length))
    return binary_number

def decimal_to_binary(decimal):
    return bin(decimal)[2:]

def decimal_to_octal(decimal):
    return oct(decimal)[2:]

def decimal_to_hexadecimal(decimal):
    return hex(decimal)[2:]

def octal_to_decimal(octal):
    return int(octal, 8)

def octal_to_binary(octal):
    decimal = octal_to_decimal(octal)
    return bin(decimal)[2:]

def octal_to_hexadecimal(octal):
    decimal = octal_to_decimal(octal)
    return hex(decimal)[2:]

def binary_to_decimal(binary):
    return int(binary, 2)

def binary_to_octal(binary):
    decimal = binary_to_decimal(binary)
    return oct(decimal)[2:]

def binary_to_hexadecimal(binary):
    decimal = binary_to_decimal(binary)
    return hex(decimal)[2:]

def hexadecimal_to_decimal(hexadecimal):
    return int(hexadecimal, 16)

def hexadecimal_to_octal(hexadecimal):
    decimal = hexadecimal_to_decimal(hexadecimal)
    return oct(decimal)[2:]

def hexadecimal_to_binary(hexadecimal):
    decimal = hexadecimal_to_decimal(hexadecimal)
    return bin(decimal)[2:]

def decimal_to_bcd(decimal_digit):
    binary_digit = bin(decimal_digit)[2:].zfill(4)
    return binary_digit

def decimal_to_excess_3_bcd(decimal_digit):
    excess_3_digit = (decimal_digit + 3) % 10  # Add 3 and take modulo 10
    binary_digit = bin(excess_3_digit)[2:].zfill(4)
    return binary_digit

def gray_to_binary(gray_code):
    binary_code = gray_code[0]
    for i in range(1, len(gray_code)):
        binary_code += str(int(gray_code[i]) ^ int(binary_code[i - 1]))
    return binary_code

def decimal_to_bcd(decimal_number):
    binary_digits = [format(int(digit), '04b') for digit in str(decimal_number)]
    bcd_result = ''.join(binary_digits)
    return bcd_result

def gray_to_bcd(binary_num):
    a1 = gray_to_binary(binary_num)
    a2 = binary_to_decimal(a1)
    a3 = decimal_to_bcd(a2)
    return a3




# Distractors
# For binary number
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


# Binary-Codes Questions....
# Question type-1
def generate_question_graycode_to_bcd(level):
    binary_number_length = 8
    binary_number = generate_binary_number(binary_number_length)
    question_text = f"Convert the given Gray code ({binary_number})GRAY into BCD format"
    correct_answer = gray_to_bcd(binary_number)
    options,correct_answer = generate_binary_options(correct_answer)

    return question_text,options,correct_answer

# Question type-2
def generate_question_decimal_to_excess3_bcd(level):
    decimal_number = random.randint(10,99)
    question_text = f"How do you represent decimal number {decimal_number} in excess 3 BCD code"
    tens_digit = decimal_number // 10
    ones_digit = decimal_number % 10
    tens_excess_3_bcd = decimal_to_excess_3_bcd(tens_digit)
    ones_excess_3_bcd = decimal_to_excess_3_bcd(ones_digit)
    correct_answer = tens_excess_3_bcd + ones_excess_3_bcd
    options,correct_answer = generate_binary_options(correct_answer)
    return question_text,options,correct_answer
    
# Question type-3
def generate_question_decimal_to_8421_bcd(level):
    decimal_number = random.randint(10,99)
    question_text = f"How do you represent decimal number {decimal_number} in 8421 BCD code"
    tens_digit = decimal_number // 10
    ones_digit = decimal_number % 10
    tens_bcd = decimal_to_bcd(tens_digit)
    ones_bcd = decimal_to_bcd(ones_digit)
    correct_answer = tens_bcd + ones_bcd
    options,correct_answer = generate_binary_options(correct_answer)
    return question_text,options,correct_answer


def generate_question_binary_codes(level):
    binary_codes_topic_list = [1,2,3]
    selected_topic = random.choice(binary_codes_topic_list)
    if selected_topic == 1:
        return generate_question_graycode_to_bcd(level)
    elif selected_topic == 2:
        return generate_question_decimal_to_excess3_bcd(level)
    elif selected_topic == 3:
        return generate_question_decimal_to_8421_bcd(level)

# Conversions Questions....

# Question type-1
def generate_question_conversion(level):
    options = []
    correct_answer = "error"
    initial_value = ''
    if level != 0:
        conversion_start = random.choice(["binary","hexadecimal","octal","decimal"])
        conversion_end = "binary"
        
        if conversion_start == "decimal":
            decimal = random.randint(0,255)
            initial_value = decimal
            conversion_end = random.choice(["hexadecimal","octal","binary"])
            if conversion_end == "binary":
                correct_answer = decimal_to_binary(decimal)
                options,correct_answer = generate_binary_options(correct_answer)
                
            elif conversion_end == "octal":
                correct_answer = decimal_to_octal(decimal)
                options,correct_answer = generate_octal_options(correct_answer)
            else:
                correct_answer = decimal_to_hexadecimal(decimal)
                options,correct_answer = generate_hexadecimal_options(correct_answer)

            
        elif conversion_start == "hexadecimal":
            hexadecimal = format(random.randint(0, 255), 'x')
            initial_value = hexadecimal
            conversion_end = random.choice(["decimal", "octal", "binary"])
            if conversion_end == "binary":
                correct_answer = hexadecimal_to_binary(hexadecimal)
                options,correct_answer = generate_binary_options(correct_answer)

            elif conversion_end == "decimal":
                correct_answer = hexadecimal_to_decimal(hexadecimal)
                options,correct_answer = generate_decimal_options(correct_answer)

            else:
                correct_answer = hexadecimal_to_octal(hexadecimal)
                options,correct_answer = generate_octal_options(correct_answer)


        elif conversion_start == "octal":
            octal = oct(random.randint(0, 255))[2:]
            initial_value = octal
            conversion_end = random.choice(["hexadecimal","decimal","binary"])
            if conversion_end == "binary":
                correct_answer = octal_to_binary(octal)
                options,correct_answer = generate_binary_options(correct_answer)

            elif conversion_end == "decimal":
                correct_answer = octal_to_decimal(octal)
                options,correct_answer = generate_decimal_options(correct_answer)

            else:
                correct_answer = octal_to_hexadecimal(octal)
                options,correct_answer = generate_hexadecimal_options(correct_answer)
            


        elif conversion_start == "binary":
            binary = bin(random.randint(0, 255))[2:]
            initial_value = binary
            conversion_end = random.choice(["hexadecimal","decimal","octal"])
            if conversion_end == "octal":
                correct_answer = binary_to_octal(binary)
                options,correct_answer = generate_octal_options(correct_answer)

            elif conversion_end == "decimal":
                correct_answer = binary_to_decimal(binary)
                options,correct_answer = generate_decimal_options(correct_answer)

            else:
                correct_answer = binary_to_hexadecimal(binary)
                options,correct_answer = generate_hexadecimal_options(correct_answer)
            
        question_text = question_text = f"What is the {conversion_end} representation of {initial_value} (in {conversion_start})? "
        return question_text,options,correct_answer
    

# Floating Numbers question

# Question - 1
def generate_question_floating_Q1(level):
    decimal_number = random.uniform(0, 10)
    question_text = f"Write the mantissa (in Hexadecimal) for the decimal number: {decimal_number}"
    float_representation = struct.unpack('f', struct.pack('f', decimal_number))[0]
    binary_representation = format(struct.unpack('!I', struct.pack('!f', float_representation))[0], '032b')
    sign_bit = binary_representation[0]
    exponent = binary_representation[1:9]
    # mantissa
    correct_answer = binary_representation[9:]
    correct_answer = binary_to_hexadecimal(correct_answer)
    options,correct_answer = generate_hexadecimal_options(correct_answer)
    return question_text,options,correct_answer
    
# Question - 2
def generate_question_floating_Q2(level):
    return 1
    




def generate_question_floating_numbers(level):
    floating_number_topic_list = [1]
    selected_topic = random.choice(floating_number_topic_list)
    if selected_topic == 1:
        return generate_question_floating_Q1(level)
    elif selected_topic == 2:
        return generate_question_floating_Q1(level)
        # return generate_question_decimal_to_excess3_bcd(level)
    # elif selected_topic == 3:
    #     return generate_question_decimal_to_8421_bcd(level)


# Binary Arithimetic Questions...

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
def generate_question__binary_arithimetic_decimal_equivalent(level):
    binary_number = generate_random_binary()
    question_text = f"The decimal equivalent of {binary_number} is?"
    correct_answer = binary_to_decimal_binary(binary_number)
    options, correct_answer = generate_decimal_options(correct_answer)
    return question_text,options,correct_answer

# Question 2
def generate_question_binary_arithimetic_breaking_in_parts(level):
    random_number = random.randint(15,100)
    first_number = random.randint(15,random_number)
    second_number = random_number - first_number
    hexa_random_number = decimal_to_hexadecimal(random_number)
    hexa_first_number = decimal_to_hexadecimal(first_number)
    hexa_second_number = decimal_to_hexadecimal(second_number)


# Main function
def generate_question_binary_arithimetic(level):
    binary_arithimetic_topic_list = [1,2]
    selected_topic = random.choice(binary_arithimetic_topic_list)
    if selected_topic == 1:
        return generate_question__binary_arithimetic_decimal_equivalent(level)
    elif selected_topic == 2:
        return generate_question__binary_arithimetic_decimal_equivalent(level)



# Overall function
def generate_question_number_system(level):
    number_system_topic_list = [1,2,3,4]
    selected_topic = random.choice(number_system_topic_list)
    if selected_topic == 1:
        return generate_question_binary_codes(level)
    elif selected_topic == 2:
        return generate_question_conversion(level)
    elif selected_topic == 3:
        return generate_question_floating_numbers(level)
    elif selected_topic == 4:
        return generate_question_binary_arithimetic(level)

if __name__ == "__main__":
    ans = generate_question_number_system(1)
    print(ans)
