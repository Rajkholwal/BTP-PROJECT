import random

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