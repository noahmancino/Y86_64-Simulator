import unittest
from instructions import System, Status
from memory import Memory
from Y86_64 import run

class TestISAImplementation(unittest.TestCase):

    def test_irmovq(self):
        """
        irmovq 5, %rax
        """
        system = System()
        encoded_program = "30F00500000000000000"
        byte_list = Memory.hex_string_to_bytes(encoded_program)
        for i, byte in enumerate(byte_list):
            system.mem.main[i] = byte

        while run(system):
            pass
        self.assertTrue(system.registers[0] == 5)

    def test_addq(self):
        """
        irmovq 5, %rax
        addq %rax, %rax
        Expected result: 10
        """
        system = System()
        encoded_program = "30f005000000000000006000"
        byte_list = Memory.hex_string_to_bytes(encoded_program)
        for i, byte in enumerate(byte_list):
            system.mem.main[i] = byte

        while run(system):
            pass
        self.assertTrue(system.registers[0] == 10)


    def test_subq(self):
        """
        irmovq 5, %rax
        irmovq 10, %rbx
        subq %rbx, %rax
        Expected result: -5
        """
        system = System()
        encoded_program = "30f0050000000000000030f30a000000000000006130"
        byte_list = Memory.hex_string_to_bytes(encoded_program)
        for i, byte in enumerate(byte_list):
            system.mem.main[i] = byte

        while run(system):
            pass
        self.assertTrue(Memory.to_signed(system.registers[0]) == -5)

    def test_andq(self):
        """
        irmovq 5, %rax
        irmovq 12, %rbx
        andq %rbx, %rax
        Expected result: 4
        """
        system = System()
        encoded_program = "30f0050000000000000030f30c000000000000006230"
        byte_list = Memory.hex_string_to_bytes(encoded_program)
        for i, byte in enumerate(byte_list):
            system.mem.main[i] = byte

        while run(system):
            pass
        self.assertTrue(system.registers[0] == 4)

    def test_xorq(self):
        """
        irmovq 11, %rax
        irmovq 21, %rbx
        xorq %rbx, %rax
        Expected result: 29
        """
        system = System()
        encoded_program = "30f00b0000000000000030f316000000000000006330"
        byte_list = Memory.hex_string_to_bytes(encoded_program)
        for i, byte in enumerate(byte_list):
            system.mem.main[i] = byte

        while run(system):
            pass
        self.assertTrue(system.registers[0] == 29)


    def test_rrmovq(self):
        """
        irmovq 5, %rbx
        rrmovq %rbx, %rax
        Expected result: 5
        """
        system = System()
        encoded_program = "30f305000000000000002030"
        byte_list = Memory.hex_string_to_bytes(encoded_program)
        for i, byte in enumerate(byte_list):
            system.mem.main[i] = byte

        while run(system):
            pass
        self.assertTrue(system.registers[0] == 5)


    def test_rmmovq(self):
        """
        irmovq 5, %rbx
        rmmovq %rbx, 0(%rcx)
        Expected result: first byte = 5
        """
        system = System()
        encoded_program = "30f3050000000000000040310000000000000000"
        byte_list = Memory.hex_string_to_bytes(encoded_program)
        for i, byte in enumerate(byte_list):
            system.mem.main[i] = byte

        while run(system):
            pass
        self.assertTrue(system.mem.main[0] == 5)

    def test_mrmovq(self):
        """
        irmovq 5, %rbx
        rmmovq %rbx, 0(%rcx)
        mrmovq 0(%rcx), %rax
        Expected result: %rax = 5
        """
        system = System()
        encoded_program = "30f305000000000000004031000000000000000050010000000000000000"
        byte_list = Memory.hex_string_to_bytes(encoded_program)
        for i, byte in enumerate(byte_list):
            system.mem.main[i] = byte

        while run(system):
            pass
        self.assertTrue(system.registers[0] == 5)

    def test_halt(self):
        """
        halt
        Expected result: system halts
        """
        system = System()
        encoded_program = "00"
        byte_list = Memory.hex_string_to_bytes(encoded_program)
        for i, byte in enumerate(byte_list):
            system.mem.main[i] = byte

        while run(system):
            pass
        self.assertTrue(system.status == Status.HLT and system.program_counter == 0)

    def test_nop(self):
        """
        nop
        Expected result: Nothing happens? Not sure what to check here.
        """
        system = System()
        encoded_program = "10"
        byte_list = Memory.hex_string_to_bytes(encoded_program)
        for i, byte in enumerate(byte_list):
            system.mem.main[i] = byte

        while run(system):
            pass
        self.assertTrue(system.program_counter == 1)

    def test_jmp(self):
        """
        jmp next
        halt
        next: irmovq 5, %rax
        Expected result: %rax = 5
        """
        system = System()

        encoded_program = "700a000000000000000030f00500000000000000"
        byte_list = Memory.hex_string_to_bytes(encoded_program)
        for i, byte in enumerate(byte_list):
            system.mem.main[i] = byte

        while run(system):
            pass
        self.assertTrue(system.registers[0] == 5)

    def test_jle(self):
        """
        irmovq 5, %rbx
        subq %rbx, %rcx
        jle next
        end: halt
        next: rrmovq %rbx, %rax
        addq %rbx, %rax
        jle next

        Expected result: %rax = 10 and no infinite loop
        """
        encoded_program = "30f3050000000000000061317116000000000000000020306030711600000000000000"
