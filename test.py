import unittest

class TestISAImplementation(unittest.TestCase):

    def test_irmovq(self):
        """
        irmovq 5, %rax
        """
        encoded_program = "0x30F07000000000000000"

    def test_addq(self):
        """
        irmovq 5, %rax
        addq %rax, %rax
        Expected result: 10
        """
        encoded_program = "0x30f005000000000000006000"


    def test_subq(self):
        """
        irmovq 5, %rax
        irmovq 10, %rbx
        subq %rbx, %rax
        Expected result: -5
        """
        encoded_program = "0x30f0050000000000000030f30a000000000000006130"

    def test_andq(self):
        """
        irmovq 5, %rax
        irmovq 12, %rbx
        andq %rbx, %rax
        Expected result: 4
        """
        encoded_program = "0x30f0050000000000000030f30c0000006230"

    def test_xorq(self):
        """
        irmovq 11, %rax
        irmovq 21, %rbx
        xorq %rbx, %rax
        Expected result: 30
        """

        encoded_program = "0x30f00b0000000000000030f315000000000000006330"


    def test_rrmovq(self):
        """
        irmovq 5, %rbx
        rrmovq %rbx, %rax
        """
