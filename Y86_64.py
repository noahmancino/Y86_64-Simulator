from instructions import System

sys = System()
sys.mem.registers[0] = (2 ** 63)
sys.mem.registers[1] = 0
sys.mem.write(0, 0)
sys.mem.write(0, 10)
sys.mrmovq(1, 2, 0)
sys.mrmovq(1, 3, 10)
sys.bin_op(2, 3, 0)
sys.mem.pprint()
print(sys.mem.overflowing_sub(2**62, 2**62 + 2))