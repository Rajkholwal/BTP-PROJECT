import random


# uses bit-flippings at one position
# return 2 things option list and correct options
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


if __name__ == "__main__":
    ans1,ans2 = generate_hexadecimal_options('7A')
    print(ans1)
    print(ans2)