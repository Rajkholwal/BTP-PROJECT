import random

def generate_binary_number(length):
    binary_number = ''.join(random.choice('01') for _ in range(length))
    return binary_number