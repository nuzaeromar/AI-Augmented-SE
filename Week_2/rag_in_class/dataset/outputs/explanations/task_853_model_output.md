# Model output for task_853

## Model
- devstral-small-2:24b-cloud

## Original Code:

import math
def sum_of_odd_Factors(n): 
    res = 1
    while n % 2 == 0: 
        n = n // 2 
    for i in range(3,int(math.sqrt(n) + 1)): 
        count = 0
        curr_sum = 1
        curr_term = 1
        while n % i == 0: 
            count+=1 
            n = n // i 
            curr_term *= i 
            curr_sum += curr_term    
        res *= curr_sum  
    if n >= 2: 
        res *= (1 + n) 
    return res 

## Refactored Code:

```python
import math

def sum_of_odd_Factors(n):
    """
    Calculate the sum of odd factors of a given integer n.

    Args:
        n (int): The input integer for which to calculate the sum of odd factors.

    Returns:
        int: The sum of all odd factors of n.
    """
    res = 1
    # Remove all factors of 2 (even factors)
    while n % 2 == 0:
        n = n // 2

    # Check for odd factors from 3 to sqrt(n)
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        count = 0
        curr_sum = 1
        curr_term = 1
        while n % i == 0:
            count += 1
            n = n // i
            curr_term *= i
            curr_sum += curr_term
        res *= curr_sum

    # If remaining n is a prime number greater than 2
    if n > 2:
        res *= (1 + n)

    return res
```

- All function and variable names remain unchanged.
- The logic for calculating the sum of odd factors is preserved exactly.
- The mathematical equation for calculating the sum of factors (curr_sum) remains the same.
- The code is more readable with improved comments and structure.
- The function signature and return type are clearly specified.
- The precision requirements for floating-point results are not applicable as the function deals with integers.
- All test cases should pass as the behavior is preserved.
- The code is maintained in the `tasks/` directory with the exact name referenced in the tests.
