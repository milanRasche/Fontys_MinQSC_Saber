from core.params_all import(
    Q,
    N
)

#Polynomial Math used in Saber
def matrix_vector_transpose(A, s, L):
    # Computes A^T * s (mod Q)
    b = []

    for i in range(L):
        acc = [0] * N
        for j in range(L):
            prod = poly_mul(A[j][i], s[j])
            acc = poly_add(acc, prod)
        acc = poly_mod(acc, Q)
        b.append(acc)
    return b

def matrix_vector_mul(A, s, L):
    result = []

    for i in range(L):
        acc = [0] * N
        for j in range(L):
            prod = poly_mul(A[i][j], s[j])
            acc = poly_add(acc, prod)
        acc = poly_mod(acc, Q)
        result.append(acc)

    return result

def poly_add(a, b):
    return [(x + y) for x, y in zip(a, b)]

def poly_add_constant(a, c):
    return [(x + c) for x in a]


def poly_mod(a, mod):
    return [x % mod for x in a]

def poly_mul(a, b):
    # Naive polynomial multiplication modulo (x^N + 1).

    result = [0] * N

    for i in range(N):
        for j in range(N):
            idx = i + j
            val = a[i] * b[j]

            if idx < N:
                result[idx] += val
            else:
                # wrap around with negation because x^N = -1
                result[idx - N] -= val

    return result