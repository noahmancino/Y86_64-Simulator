# This module defines the System class, which includes the state of memory and all instructions
import memory


class System:
    def __init__(self):
        self.mem = memory.Memory()

    def halt(self):
        """
        Sets halt status on the processor

        :return:
        """
        self.mem.status = memory.Status.HLT

    def bin_op(self, src, dest, op_code):
        """
        Executes instructions which consist of binary operations on words in registers.

        :param src: Index of the source register in the register file
        :param dest: Index of the destination register in the register file
        :param op_code: Specifies which binary operation to perform.
        :return:
        """
        src_val, dest_val = self.mem.registers[src], self.mem.registers[dest]
        overflow = False
        if op_code == 0:
            overflow, self.mem.registers[dest] = memory.overflowing_add(dest_val, src_val, 64)
        elif op_code == 1:
            overflow, self.mem.registers[dest] = memory.overflowing_sub(dest_val, src_val, 64)
        elif op_code == 2:
            self.mem.registers[dest] = src_val & dest_val
        elif op_code == 3:
            self.mem.registers[dest] = src_val | dest_val
        else:
            self.mem.status = memory.Status.INS
            return

        self.mem.overflow_flag = overflow
        self.mem.sign_flag = self.mem.registers[dest] < 0
        self.mem.zero_flag = self.mem.registers[dest] == 0
        self.mem.program_counter += 2

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
            will_jump = self.mem.zero_flag or (self.mem.sign_flag != self.mem.overflow_flag)
        elif op_code == 2:
            will_jump = self.mem.sign_flag != self.mem.overflow_flag
        elif op_code == 3:
            will_jump = self.mem.zero_flag
        elif op_code == 4:
            will_jump = not self.mem.zero_flag
        elif op_code == 5:
            will_jump = self.mem.zero_flag or (self.mem.sign_flag == self.mem.overflow_flag)
        elif op_code == 6:
            will_jump = not self.mem.zero_flag and (self.mem.sign_flag == self.mem.overflow_flag)
        else:
            self.mem.status = memory.Status.INS
            return

        if will_jump:
            self.mem.program_counter = dest
        else:
            self.mem.program_counter += 9

        return

    def irmovq(self, immediate, dest):
        """
        :param immediate: An immediate value
        :param dest: Register to move the immediate value to.
        :return:
        """
        self.mem.registers[dest] = immediate
        self.mem.program_counter += 10

    def rrmovq(self, src, dest):
        """
        :param src: A register which holds a value to be copied
        :param dest: The register in which the value of src will be copied
        :return:
        """
        self.mem.registers[dest] = self.mem.registers[src]
        self.mem.program_counter += 2

    def rmmovq(self, src, dest_reg, displacement):
        """
        Copies the contents of src to main memory at the address in memory determined by the contents of dest_reg
        + displacement

        :param src: A register holding a value to copy to memory
        :param dest_reg: A register holding a memory address
        :param displacement: The difference between where we wish to write to memory and the contents dest_reg
        :return:
        """
        destination = self.mem.registers[dest_reg] + displacement
        self.mem.write(src, destination)
        self.mem.program_counter += 10

    def mrmovq(self, src_reg, dest, displacement):
        """
        Copies the memory pointed at by the contents of src_reg + replacement to the dest register

        :param src_reg: Register holding an address to memory
        :param dest: A register to which you wish to hold data from memory
        :param displacement: Where in memory you wish to read from relative to the address held by src_reg
        :return:
        """
        source = self.mem.registers[src_reg] + displacement
        self.mem.read(dest, source)
        self.mem.program_counter += 10

    def cmovxx(self):