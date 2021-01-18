from instructions import System
INS_SIZE = {"halt": 1, "nop": 1, "rrmovq": 2, "irmovq": 10, "rmmovq": 10, "mrmovq": 10, "addq": 2, "subq": 2, "andq": 2,
            "xorq": 2, "jmp": 9, "jle": 9, "jl": 9, "je": 9, "jne": 9, "jge": 9, "jg": 9, "cmovle": 2, "cmovl": 2,
            "cmove": 2, "cmovne": 2, "cmovge": 2, "cmovg": 2, "call": 9, "ret": 1, "pushq": 2, "popq": 2}


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

def assemble(filename):
    with open(filename, "r") as f:
        lines = f.readlines()

    tokens = tokenize(lines)
    mem_map = map_to_mem(tokens)