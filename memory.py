'''
This module defines the structure of system memory and provides some helper functions for working with python integers
as if they were words in system memory.
'''
from enum import Enum


def twos_compliment(num, bits):
    """
    :param num: A python integer
    :param bits: Number of bytes to fit the integer into
    :return: The two's compliment value of num interpreted as a two's compliment bit string with 'bytes' bytes
    """
    smallest_int = 1 << bits
    if num & smallest_int:
        num -= smallest_int
    return num


def overflowing_add(num1, num2, bits):
    """
    :param num1: First number to add
    :param num2: Second number to add
    :param bits: Number of bits to fit the result into
    :return: Adds the two numbers modulo 2**bits - 1 and returns the result in a tuple preceded a bool indicating
             overflow occurred
    """
    max_num = 2 ** bits - 1
    sum_res = num1 + num2
    result = (False, sum_res)
    if sum_res > max_num - 1:
        result = (True, sum_res % max_num)
    return result


def overflowing_sub(num1, num2, bits):
    """
    :param num1: First argument to subtraction operation
    :param num2: Second argument to subtraction operation
    :param bits: Number of bits to fit the result into
    :return: Subtracts num2 from num1, wrapped around 2**bits - 1, and returns the result in a tuple preceded by a
             bool indicating whether overflow occured.
    """
    max_num = 2 ** bits - 1
    difference = num1 - num2
    result = (False, difference)
    if difference < 0:
        result = (1, max_num + difference + 1)
    return result


class Status(Enum):
    # Normal processor state
    AOK = 0
    # Halt instruction encountered
    HLT = 1
    # Reference to invalid memory address.
    ADR = 2
    # Invalid instruction
    INS = 3


class Memory:
    """
    Holds the state of memory, and includes some helper functions for reading writing and interpreting it.
    """
    def __init__(self):
        # Main memory is big endian, and holds 'bytes' which in this case are just python integers from 0 to 2^8
        self.main = [0 for _ in range(5000)]
        # Registers hold 64 bits, i.e python ints from 0 to 256
        self.registers = [0 for _ in range(15)]
        self.program_counter = 0
        self.status = Status.AOK
        self.overflow_flag = 0
        self.sign_flag = 0
        self.zero_flag = 0

    @staticmethod
    def extract_byte(byte, val):
        """
        :param byte: byte to be extracted, from 0 to 7
        :param val: 64-bit value from which to extract the byte
        :return: the 'byteth' byte of val
        """
        # Byte long bit mask
        mask = 2 ** 8 - 1
        return (val >> (8 * byte)) & mask

    def combine_bytes(self, address):
        """
        :param address: A direct address to main memory, between 0 and 5000 - 8
        :return: A python integer which the little endian interpreted value of the 8 consecutive bytes of memory
                 starting at the location specified by the address parameter
        """
        combined = 0
        for x in range(8):
            combined = combined >> 8
            combined |= self.main[address + x]
        return combined


