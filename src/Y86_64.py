from system import *
import assembler
import os
import sys

HELP_MESSAGE = 'Enter nothing: execute the next instruction if program is paused. Otherwise end program.\n' \
               'Enter s: display flags, program counter, registers, and status.\n' \
               'Enter m: display all of main memory.\n' \
               'Enter h: display this message\n'


def run(sys: System):
    """
    Runs the instruction pointed to by the program counter if the system is AOK

    :param sys: A System object
    :return: True if system status is AOK after the instruction is run, false otherwise.
    """
    if sys.status != Status.AOK:
        return False

    next_ins = sys.mem.main[sys.program_counter:sys.program_counter + 10]
    instruction_function = next_ins[0] & 0xf
    instruction_specifier = (next_ins[0] & 0xf0) >> 4
    # Note: Not all instructions actually have register specifiers
    reg_a = (next_ins[1] & 0xf0) >> 4
    reg_b = next_ins[1] & 0xf
    if instruction_specifier == 0:
        sys.halt()
    elif instruction_specifier == 1:
        sys.program_counter += 1
    elif instruction_specifier == 2:
        if instruction_function == 0:
            sys.rrmovq(reg_a, reg_b)
        else:
            sys.cmovxx(reg_a, reg_b, instruction_function)
    elif instruction_specifier == 3:
        immediate = sys.mem.read(sys.program_counter + 2)
        sys.irmovq(immediate, reg_b)
    elif instruction_specifier == 4:
        displacement = sys.mem.read(sys.program_counter + 2)
        sys.rmmovq(reg_a, reg_b, displacement)
    elif instruction_specifier == 5:
        displacement = sys.mem.read(sys.program_counter + 2)
        sys.mrmovq(reg_b, reg_a, displacement)
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

    return True if sys.status == Status.AOK else False


def query_response(option, sys):
    if option == "h":
        print(HELP_MESSAGE)
    elif option == "s":
        sys.pprint()
    elif option == "m":
        sys.mem.pprint()


def main():
    system = System()
    assert len(sys.argv) == 2, "Please provide one input file"
    try:
        with open(sys.argv[1], 'r') as file:
            source_lines = file.readlines()
            print(source_lines)
    except FileNotFoundError:
        print('Input file not found')

    assembler.assemble(source_lines, system)
    x = 0
    while run(system) and x < 1000:
        registers = system.registers
        x += 1

    print(system)
    with open('final_memory_state.txt', 'w') as file:
        file.write(repr(system.mem))
    return

if __name__ == '__main__':
    main()