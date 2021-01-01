# This module defines the System class, which includes the state of memory and all instructions
import memory


class System:
    def __init__(self):
        self.memory = memory.Memory()

    def halt(self):
        """
        Sets halt status on the processor

        :return:
        """
        self.memory.status = memory.Status.HLT

    def bin_op(self, src, dest, op_code):
        """
        Executes instructions which consist of binary operations on words in registers.

        :param src: Index of the source register in the register file
        :param dest: Index of the destination register in the register file
        :param op_code: Specifies which binary operation to perform.
        :return:
        """
        src_val, dest_val = self.memory.registers[src], self.memory.registers[dest]
        overflow = False
        if op_code == 0:
            overflow, self.memory.registers[dest] = memory.overflowing_add(dest_val, src_val, 64)
        elif op_code == 1:
            overflow, self.memory.registers[dest] = memory.overflowing_sub(dest_val, src_val, 64)
        elif op_code == 2:
            self.memory.registers[dest] = src_val & dest_val
        elif op_code == 3:
            self.memory.registers[dest] = src_val | dest_val
        else:
            self.memory.status = memory.Status.INS
            return

        self.memory.overflow_flag = overflow
        self.memory.sign_flag = self.memory.registers[dest] < 0
        self.memory.zero_flag = self.memory.registers[dest] == 0
        self.memory.program_counter += 2

    def jxx(self, dest, op_code):
        """

        :param dest:
        :param op_code:
        :return:
        """


