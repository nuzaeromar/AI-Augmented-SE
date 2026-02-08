# Model output for task_453

## Model
- devstral-small-2:24b-cloud

## Original Code:

import math 
def sumofFactors(n) : 
    if (n % 2 != 0) : 
        return 0
    res = 1
    for i in range(2, (int)(math.sqrt(n)) + 1) :    
        count = 0
        curr_sum = 1
        curr_term = 1
        while (n % i == 0) : 
            count= count + 1
            n = n // i 
            if (i == 2 and count == 1) : 
                curr_sum = 0
            curr_term = curr_term * i 
            curr_sum = curr_sum + curr_term 
        res = res * curr_sum  
    if (n >= 2) : 
        res = res * (1 + n) 
    return res 

## Refactored Code:

```python
import math

def sumofFactors(n):
    """
    Calculate the sum of all factors of a given number n.

    Args:
        n (int): The input number for which to calculate the sum of factors.

    Returns:
        int: The sum of all factors of n. Returns 0 if n is odd.
    """
    if n % 2 != 0:
        return 0
    res = 1
    for i in range(2, int(math.sqrt(n)) + 1):
        count = 0
        curr_sum = 1
        curr_term = 1
        while n % i == 0:
            count += 1
            n = n // i
            if i == 2 and count == 1:
                curr_sum = 0
            curr_term *= i
            curr_sum += curr_term
        res *= curr_sum
    if n >= 2:
        res *= (1 + n)
    return res
```

- All function and variable names remain the same as in the original implementation.
- The logic and mathematical equations are preserved exactly as in the original code.
- The function signature and return type are clearly specified in the docstring.
- The code is formatted for better readability while maintaining the original behavior.
- The function handles edge cases (like odd numbers) as in the original implementation.
- The loop and conditional logic are kept intact to ensure the same output for all inputs.
- The docstring provides clear documentation of the function's purpose, arguments, and return value.
- The code adheres to the strict rules provided, ensuring no changes to the core logic or structure.
