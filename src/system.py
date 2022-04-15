# This module defines the System class, which holds the entire system state and methods to carry out instructions.
import memory as memory
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


class System:

    def __init__(self):
        self.mem = memory.Memory()
        # Registers hold 64 bits, i.e python ints from 0 to 2^64 - 1
        self.registers = [0 for _ in range(15)]
        self.program_counter = 0
        self.status = Status.AOK
        self.overflow_flag = False
        self.sign_flag = False
        self.zero_flag = False

    def __repr__(self):
        return (f'registers: {[self.mem.to_signed(register) for register in self.registers]}\n'
        f'program_counter: {self.program_counter}\n'
        f'status: {self.status}\n'
        f'overflow flag: {self.overflow_flag} ; sign flag {self.sign_flag} ; zero flag {self.zero_flag}')

    def halt(self):
        """
        Sets halt status on the processor

        :return:
        """
        self.status = Status.HLT

    def bin_op(self, src, dest, op_code):
        """
        Executes instructions which consist of binary operations on words in registers.

        :param src: Index of the source register in the register file
        :param dest: Index of the destination register in the register file
        :param op_code: Specifies which binary operation to perform.
        :return:
        """
        src_val, dest_val = self.registers[src], self.registers[dest]
        overflow = False
        if op_code == 0:
            overflow, self.registers[dest] = self.mem.overflowing_add(dest_val, src_val)
        elif op_code == 1:
            # dest - src
            overflow, self.registers[dest] = self.mem.overflowing_sub(dest_val, src_val)
        elif op_code == 2:
            self.registers[dest] = src_val & dest_val
        elif op_code == 3:
            self.registers[dest] = src_val ^ dest_val
        else:
            self.status = Status.INS
            return

        self.overflow_flag = overflow
        self.sign_flag = self.mem.to_signed(self.registers[dest]) < 0
        self.zero_flag = self.registers[dest] == 0
        self.program_counter += 2

    def jxx(self, dest, op_code):
        """
        Implements jump instructions, which jump to an address depending on the state of the system's condition codes

        :param dest: Memory address to jump to.
        :param op_code: Specifies which flags to check.
        :return:
        """
        will_jump = False

        if op_code == 0:
            will_jump = True
        elif op_code == 1:
            will_jump = self.zero_flag or (self.sign_flag != self.overflow_flag)
        elif op_code == 2:
            will_jump = self.sign_flag != self.overflow_flag
        elif op_code == 3:
            will_jump = self.zero_flag
        elif op_code == 4:
            will_jump = not self.zero_flag
        elif op_code == 5:
            will_jump = self.zero_flag or (self.sign_flag == self.overflow_flag)
        elif op_code == 6:
            will_jump = not self.zero_flag and (self.sign_flag == self.overflow_flag)
        else:
            self.status = Status.INS
            return

        if will_jump:
            self.program_counter = dest
        else:
            self.program_counter += 9

        return

    def irmovq(self, immediate, dest):
        """
        :param immediate: An immediate value
        :param dest: Register to move the immediate value to.
        :return:
        """
        self.registers[dest] = immediate
        self.program_counter += 10

    def rrmovq(self, src, dest):
        """
        :param src: A register which holds a value to be copied
        :param dest: The register in which the value of src will be copied
        :return:
        """
        self.registers[dest] = self.registers[src]
        self.program_counter += 2

    def rmmovq(self, src, dest_reg, displacement):
        """
        Copies the contents of src to main memory at the address in memory determined by the contents of dest_reg
        + displacement

        :param src: A register holding a value to copy to memory
        :param dest_reg: A register holding a memory address
        :param displacement: The difference between where we wish to write to memory and the contents dest_reg
        :return:
        """
        destination = self.registers[dest_reg] + displacement
        self.mem.write(self.registers[src], destination)
        self.program_counter += 10

    def mrmovq(self, src_reg, dest, displacement):
        """
        Copies the memory pointed at by the contents of src_reg + replacement to the dest register

        :param src_reg: Register holding an address to memory
        :param dest: The register to which you wish to move data from memory
        :param displacement: Where in memory you wish to read from relative to the address held by src_reg
        :return:
        """
        source = self.registers[src_reg] + displacement
        self.registers[dest] = self.mem.read(source)
        self.program_counter += 10

    def cmovxx(self, src, dest, op_code):
        will_move = False

        if op_code == 0:
            will_move = True
        elif op_code == 1:
            print('here')
            will_move = self.zero_flag or (self.sign_flag != self.overflow_flag)
        elif op_code == 2:
            will_move = self.sign_flag != self.overflow_flag
        elif op_code == 3:
            will_move = self.zero_flag
        elif op_code == 4:
            will_move = not self.zero_flag
        elif op_code == 5:
            will_move = self.zero_flag or (self.sign_flag == self.overflow_flag)
        elif op_code == 6:
            will_move = (not self.zero_flag) and (self.sign_flag == self.overflow_flag)
        else:
            self.status = Status.INS
            return

        if will_move:
            self.registers[dest] = self.registers[src]

        self.program_counter += 2

    def pushq(self, src):
        # Register four is the stack pointer
        self.registers[4] -= 8
        self.mem.write(self.registers[src], self.registers[4])
        self.program_counter += 2

    def popq(self, dest):
        self.registers[dest] = self.mem.read(self.registers[4])
        self.registers[4] += 8
        self.program_counter += 2

    def call(self, dest):
        self.registers[4] -= 8
        self.program_counter += 9
        self.mem.write(self.program_counter, self.registers[4])
        self.program_counter = dest

    def ret(self):
        address = self.mem.read(self.registers[4])
        self.registers[4] += 8
        self.program_counter = address
