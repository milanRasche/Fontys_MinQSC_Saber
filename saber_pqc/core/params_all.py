SEED_BYTES = 32

#Constant acoss all Saber
N = 256
Q = 8192 #2^13
EQ = 13
MU = 10
EP = 10

def compute_rounding_constant_p():
    return 1 << (EQ - EP - 1)

def compute_compression_shift_p():
    return EQ - EP

def compute_compression_constant_t(ET):
    return 1 << (EQ - ET - 1)

def compute_compression_shift_t(ET):
    return EQ - ET