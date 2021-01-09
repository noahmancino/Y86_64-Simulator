import memory
from instructions import *

def run(sys: System):
    """
    Runs the instruction pointed to by the program counter if the system is AOK

    :param sys: A System object
    :return:
    """
    if sys.status != Status.AOK:
        return

    next_ins = sys.mem.main[sys.program_counter:sys.program_counter+10]
    instruction_function = next_ins[0] & 0xf
    instruction_specifier = (next_ins[0] & 0xf0) >> 4
    print(instruction_specifier)
    # Note: Not all instructions actually have register specifiers
    reg_a = (next_ins[1] & 0xf0) >> 4
    reg_b = next_ins[1] & 0xf0
    if instruction_specifier == 0:
        sys.halt()
    elif instruction_specifier == 1:
        print('hello!')
        sys.program_counter += 1
    elif instruction_specifier == 2:
        sys.rrmovq(reg_a, reg_b)
    elif instruction_specifier == 3:
        immediate = sys.mem.read(sys.program_counter + 2)
        sys.irmovq(immediate, reg_b)
    elif instruction_specifier == 4:
        displacement = sys.mem.read(sys.program_counter + 2)
        sys.rmmovq(reg_a, reg_b, displacement)
    elif instruction_specifier == 5:
        displacement = sys.mem.read(sys.program_counter + 2)
        sys.mrmovq(reg_a, reg_b, displacement)
    elif instruction_specifier == 6:
        sys.bin_op(reg_a, reg_b, instruction_function)
    elif instruction_specifier == 7:
        destination = sys.mem.read(sys.program_counter + 1)
        sys.jxx(destination, instruction_function)
    elif instruction_specifier == 8:
        destination = sys.mem.read(sys.program_counter + 1)
        sys.call(destination)
    elif instruction_specifier == 9:
        sys.ret()
    elif instruction_specifier == 10:
        sys.pushq(reg_a)
    elif instruction_specifier == 11:
        sys.popq(reg_a)
    else:
        sys.status = Status.INS

sys = System()
sys.mem.main[0] = 1 << 4
run(sys)
sys.pprint()