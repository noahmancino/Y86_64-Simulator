from instructions import System


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

    tokenize(lines)