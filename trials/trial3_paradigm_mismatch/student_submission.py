
def compute_factorial(val):
    res = 1
    # Student uses while loop instead of recursion
    while val > 0:
        res *= val
        val -= 1
    return res
