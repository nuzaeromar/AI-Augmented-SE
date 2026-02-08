# Model output for task_107

## Model
- devstral-small-2:24b-cloud

## Original Code:

def count_Hexadecimal(L,R) :  
    count = 0;  
    for i in range(L,R + 1) : 
        if (i >= 10 and i <= 15) : 
            count += 1;  
        elif (i > 15) : 
            k = i;  
            while (k != 0) :  
                if (k % 16 >= 10) : 
                    count += 1;  
                k = k // 16;  
    return count;  

## Refactored Code:

```python
def count_Hexadecimal(L, R):
    """
    Counts the number of hexadecimal digits in the range [L, R].

    Args:
        L (int): The lower bound of the range (inclusive).
        R (int): The upper bound of the range (inclusive).

    Returns:
        int: The count of hexadecimal digits in the range [L, R].
    """
    count = 0
    for i in range(L, R + 1):
        if 10 <= i <= 15:
            count += 1
        elif i > 15:
            k = i
            while k != 0:
                if k % 16 >= 10:
                    count += 1
                k = k // 16
    return count
```

- The function `count_Hexadecimal` is refactored to improve readability by using more Pythonic conditions and consistent indentation.
- The logic remains unchanged, preserving the original behavior of counting hexadecimal digits in the range [L, R].
- The function signature and return type are explicitly documented.
- The mathematical logic for checking hexadecimal digits (digits >= 10) is retained.
- The loop and conditional checks are simplified for better clarity.
- The function handles edge cases where L and R are the same or when the range includes numbers with multiple digits in base 16.
- The variable names and structure are kept identical to the original to ensure compatibility with existing tests.
- The function is designed to work with integer inputs and returns an integer count.
