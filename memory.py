'''
This module defines the structure of system memory and provides some helper functions for working with python integers
as if they were words in system memory.
'''
from enum import Enum

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

    def write(self, src, destination):
        """
        :param src: Register that holds a write value
        :param destination: Address of memory to write to
        :return:
        """
        val = self.registers[src]
        mask = 2 ** 8 - 1
        for i in range(8):
            byte = (val >> (8 * i)) & mask
            self.main[destination + i] = byte

    def read(self, dest, address):
        """
        Reads main memory at 'address' into the destination register.

        :param address: A direct address to main memory, between 0 and 5000 - 8
        :param dest: The location of a register in the register file
        :return:
        """
        combined = 0
        for x in range(8):
            combined = combined << 8
            combined |= self.main[address + 7 - x]

        self.registers[dest] = combined

    def pprint(self):
        print(f'registers: {self.registers}')
        print(f'program counter: {self.program_counter}')
        print(f'status: {self.status}')
        print(f'flags: overflow {self.overflow_flag}, sign: {self.sign_flag}, zero: {self.zero_flag}')

    @staticmethod
    def to_unsigned(num):
        """
        :param num: A python integer which can be represented in 64 bits with two's compliment encoding.
        :return: The conversion of num interpreted as a two's compliment signed int to an unsigned int.
        """
        if num < 0:
            num += 2**64

        return num

    @staticmethod
    def to_signed(num):
        """
        Note that in operations we use on memory, there are a number of places where logical bit shift is needed but none
        where arithmetic bit shift is needed. Since python's built in bit shift operator is arithmetic, memory will
        always be stored as an unsigned int and only be converted to a signed in some intermediate computations and
        sometimes when displaying information to users.

        :param num: A python integer which can fit into 64 unsigned bits
        :return: The conversion of num interpreted as an unsigned int to num interpreted as a twos_compliment int
        """
        smallest_int = 1 << 64
        if num & smallest_int:
            num -= smallest_int
        return num

    @staticmethod
    def overflowing_add(num1, num2):
        """
        :param num1: First number to add (unsigned 64-bit)
        :param num2: Second number to add (unsigned 64-bit)
        :return: A 2-tuple containing the result of two's compliment addition between num1 and num2 preceded by a bool
                 indicating if overflow occurred.
        """
        max_num = 2**64 - 1
        sum_res = num1 + num2
        result = (False, sum_res)
        if sum_res >= max_num:
            result = (True, sum_res % (max_num + 1))
        return result

    def overflowing_sub(self, num1, num2):
        """
        :param num1: First argument to subtraction operation
        :param num2: Second argument to subtraction operation
        :return: A 2-tuple containing the result of two's compliment subtraction between num1 and num2 preceded by a bool
                 indicating if overflow occurred.
        """
        # num2 = -num2
        num2 = self.to_unsigned(-self.to_signed(num2))
        return self.overflowing_add(num1, num2)

