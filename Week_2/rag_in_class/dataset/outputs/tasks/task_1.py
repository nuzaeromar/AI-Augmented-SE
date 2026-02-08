R = 3
C = 3

def min_cost(cost, m, n):
    # Initialize a DP table with zeros
    tc = [[0 for _ in range(C)] for _ in range(R)]

    # Base case: starting at (0, 0)
    tc[0][0] = cost[0][0]

    # Fill first column (only moving down)
    for i in range(1, m + 1):
        tc[i][0] = tc[i - 1][0] + cost[i][0]

    # Fill first row (only moving right)
    for j in range(1, n + 1):
        tc[0][j] = tc[0][j - 1] + cost[0][j]

    # Fill the rest of the table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            # Take the minimum of the three possible previous cells
            tc[i][j] = min(tc[i - 1][j - 1], tc[i - 1][j], tc[i][j - 1]) + cost[i][j]

    # Return the minimum cost to reach the bottom-right corner
    return tc[m][n]
