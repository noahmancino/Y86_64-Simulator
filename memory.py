"""
This module defines the structure of system memory and provides some helper functions for working with python integers
as if they were words in system memory.
"""


class Memory:
    """
    Holds the state of main memory along with some methods to read to, write to, and interpret it.
    """
    def __init__(self):
        # Main memory is little endian, and holds 'bytes' which in this case are just python integers from 0 to 2^8
        self.main = [0 for _ in range(1000)]

    def write(self, src, destination):
        """
        :param src: A value to write.
        :param destination: Address of memory to write to
        :return:
        """
        val = src
        mask = 2 ** 8 - 1
        for i in range(8):
            byte = (val >> (8 * i)) & mask
            self.main[destination + i] = byte

    def read(self, address):
        """
        :param address: A direct address to main memory, between 0 and 1000 - 8
        :return: The next 8 bytes after address read into a 64 bit number.
        """
        combined = 0
        for x in range(8):
            combined = combined << 8
            combined |= self.main[address + 7 - x]
        return combined

    def pprint(self):
        print("main:")
        for i in range(125):
            print([self.main[j + (i * 8)] for j in range(8)])

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
        Note that in operations we use on memory, there are a number of places where logical bit shift is needed but
        none where arithmetic bit shift is needed. Since python's built in bit shift operator is arithmetic,
        memory will always be stored as an unsigned int and only be converted to a signed in some intermediate
        computations and sometimes when displaying information to users.

        :param num: A python integer which can fit into 64 unsigned bits
        :return: The conversion of num interpreted as an unsigned int to num interpreted as a twos_compliment int
        """
        smallest_int = 1 << 63
        if num & smallest_int:
            num -= 2 * smallest_int
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
        result = sum_res
        if sum_res >= max_num:
            result = sum_res % (max_num + 1)
        sign1, sign2, sign3 = (Memory.to_signed(num1) < 0), (Memory.to_signed(num2) < 0), (Memory.to_signed(result) < 0)
        overflow = sign1 == sign2 and sign1 != sign3
        return overflow, result

    @staticmethod
    def overflowing_sub(num1, num2):
        """
        :param num1: First argument to subtraction operation :param num2: Second argument to subtraction operation
        :return: A 2-tuple containing the result of two's compliment subtraction between num1 and num2 preceded by a
        bool indicating if overflow occurred.
        """
        # num2 = -num2
        num2 = Memory.to_unsigned(-Memory.to_signed(num2))
        return Memory.overflowing_add(num1, num2)
