# Model output for task_558

## Model
- devstral-small-2:24b-cloud

## Original Code:

def digit_distance_nums(n1, n2):
         return sum(map(int,str(abs(n1-n2))))

## Refactored Code:

```python
def digit_distance_nums(n1: int, n2: int) -> int:
    """Calculate the sum of digits in the absolute difference between two integers.

    Args:
        n1: First integer
        n2: Second integer

    Returns:
        Sum of digits in the absolute difference between n1 and n2
    """
    return sum(map(int, str(abs(n1 - n2))))
```

- All function and variable names remain unchanged
- Function signature and return type are explicitly specified
- The mathematical operation (absolute difference) is preserved
- The digit sum calculation logic remains identical
- The implementation handles all integer inputs correctly
- The function maintains the same behavior as validated by tests
- No additional functionality or changes to the core logic
- The code is properly formatted and readable
- The docstring clearly explains the function's purpose and parameters
