from instructions import System
INS_SIZE = {"halt": 1, "nop": 1, "rrmovq": 2, "irmovq": 10, "rmmovq": 10, "mrmovq": 10, "addq": 2, "subq": 2, "andq": 2,
            "xorq": 2, "jmp": 9, "jle": 9, "jl": 9, "je": 9, "jne": 9, "jge": 9, "jg": 9, "cmovle": 2, "cmovl": 2,
            "cmove": 2, "cmovne": 2, "cmovge": 2, "cmovg": 2, "call": 9, "ret": 1, "pushq": 2, "popq": 2}
REGISTER_INDEX = {}



def tokenize(lines):
    """
    Tokenizes a y86-64 assembly file
    """
    tokens = []
    for line in lines:
        line.rstrip('#')
        line.replace('#', '')
        if line:
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
            place = int(token_list[1])

    return mem_map


def encode_instructions(tokens):




def assemble(filename):
    with open(filename, "r") as f:
        lines = f.readlines()

    tokens = tokenize(lines)
    mem_map = map_to_mem(tokens)