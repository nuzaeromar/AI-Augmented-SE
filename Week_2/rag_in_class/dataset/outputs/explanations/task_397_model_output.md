# Model output for task_397

## Model
- devstral-small-2:24b-cloud

## Original Code:

def median_numbers(a,b,c):
 if a > b:
    if a < c:
        median = a
    elif b > c:
        median = b
    else:
        median = c
 else:
    if a > c:
        median = a
    elif b < c:
        median = b
    else:
        median = c
 return median

## Refactored Code:

```python
def median_numbers(a, b, c):
    """
    Calculate the median of three numbers.

    Args:
        a (float): First number
        b (float): Second number
        c (float): Third number

    Returns:
        float: The median value of the three input numbers
    """
    if a > b:
        if a < c:
            median = a
        elif b > c:
            median = b
        else:
            median = c
    else:
        if a > c:
            median = a
        elif b < c:
            median = b
        else:
            median = c
    return median
```

- All function and variable names remain unchanged
- The logic and equation for finding the median are preserved exactly
- The function signature and return type are maintained
- The implementation handles all edge cases as in the original
- The code structure follows the original implementation exactly
- No additional functionality or changes to behavior are introduced
- The function works with floating-point numbers as in the original
- All test cases should pass without modification
