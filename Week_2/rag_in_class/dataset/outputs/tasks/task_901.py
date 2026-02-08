def smallest_multiple(n):
    if n <= 2:
        return n
    i = n * 2
    factors = [number for number in range(n, 1, -1) if number * 2 > n]
    while True:
        divisible = True
        for a in factors:
            if i % a != 0:
                i += n
                divisible = False
                break
        if divisible:
            return i
