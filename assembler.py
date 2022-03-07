from instructions import System
from memory import Memory
INS_SIZE = {
    "halt": 1, "nop": 1, "rrmovq": 2, "irmovq": 10, "rmmovq": 10, "mrmovq": 10, "addq": 2, "subq": 2, "andq": 2,
    "xorq": 2, "jmp": 9, "jle": 9, "jl": 9, "je": 9, "jne": 9, "jge": 9, "jg": 9, "cmovle": 2, "cmovl": 2,
    "cmove": 2, "cmovne": 2, "cmovge": 2, "cmovg": 2, "call": 9, "ret": 1, "pushq": 2, "popq": 2}
INS_OP_FUNCTION = {
    "halt": [0, 0], "nop": [1, 0], "rrmovq": [2, 0], "irmovq": [3, 0], "rmmovq": [4, 0], "mrmovq": [5, 0],
    "addq": [6, 0], "subq": [6, 1], "andq": [6, 2], "xorq": [6, 3], "jmp": [7, 0], "jle": [7, 1], "jl": [7, 2],
    "je": [7, 3], "jne": [7, 4], "jge": [7, 5], "jg": [7, 6], "cmovle": [2, 1], "cmovl": [2, 2], "cmove": [2,3],
    "cmovne": [2, 4], "cmovge": [2, 5], "cmovg": [2, 6], "call": [8, 0], "ret": [9, 0], "pushq": [10, 0],
    "popq": [11, 0]}
REGISTER_INDEX = {
    "%rax": 0, "%rcx": 1, "%rdx": 2, "%rbx": 3, "%rsp": 4, "%rbp": 5, "%rsi": 6, "%rdi": 7, "%r8": 8, "%r9": 9,
    "%r10": 10, "%r11": 11, "%r12": 12, "%r13": 13, "%r14": 14}


def tokenize(lines):
    """
    Tokenizes a y86-64 assembly file
    """
    tokens = []
    for line in lines:
        line = line.rstrip('#')
        line = line.replace('#', '')
        if ':' in line:
            line = line.replace(':', '\n')
            comma_seperated = line.split('\n')
            if not comma_seperated[0].isspace() and comma_seperated[0]:
                tokens.append(comma_seperated[0].split())
            if not comma_seperated[1].isspace() and comma_seperated[1]:
                tokens.append(comma_seperated[1].split())
        else:
            if not line.isspace() and line:
                tokens.append(line.split())

    return tokens


def map_to_mem(tokens):
    """
    Maps each lists of tokens (i.e each line) to their place in memory, and returns the map as a list of tuples
    """
    place = 0
    mem_map = []
    for token_list in tokens:
        mem_map.append((place, token_list))
        first_token = token_list[0]
        if first_token in INS_SIZE.keys():
            place += INS_SIZE[first_token]
        elif first_token == ".align":
            place += place % int(token_list[1])
        elif first_token == ".quad":
            place += 8
        elif first_token == ".pos":
            place = int(token_list[1], base=16)

    return mem_map

def encode_ins(instruction_tokens):
    instruction = instruction_tokens[0]

    if instruction == "halt":
        return "00"

    if instruction == "nop":
        return "10"

    if instruction == "rrmovq":
        reg_a = REGISTER_INDEX[instruction_tokens[1]]
        reg_a = f"{reg_a:x}"
        reg_b = "{0:x}".format(instruction_tokens[2])
        return f'20{reg_a}{reg_b}'

    if instruction == "irmovq":
        immediate = int(instruction_tokens[1])
        immediate = Memory.endian_conversion(f'{immediate:x}')
        reg_b = REGISTER_INDEX[instruction_tokens[2]]
        reg_b = "{0:x}".format(reg_b)
        return f'30f{reg_b}{immediate:0<16}'

    if instruction == "rmmovq":
        reg_a = REGISTER_INDEX[instruction_tokens[1]]
        reg_a = f"{reg_a:x}"
        tok_two = instruction_tokens[2].replace(')', '')
        dest, reg_b = tok_two.split('(')
        reg_b = REGISTER_INDEX[reg_b]
        reg_b = f'{reg_b:x}'
        dest = int(dest)
        dest = Memory.endian_conversion(f'{dest:x}')
        return f'40{reg_a}{reg_b}{dest:0<16}'

    if instruction == "mrmovq"


def encode(mapped_tokens):
    """
    Translates instructions to machine code and loads them into the system.
    """