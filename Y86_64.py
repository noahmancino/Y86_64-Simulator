from instructions import System

sys = System()
sys.mem.write(100, 0)
sys.mem.write(2**62, 10)
sys.mem.pprint()
sys.mrmovq(0, 2, 0)
sys.mrmovq(0, 3, 10)
sys.bin_op(2, 3, 0)
sys.pprint()