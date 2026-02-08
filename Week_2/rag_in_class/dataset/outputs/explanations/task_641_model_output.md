# Model output for task_641

## Model
- devstral-small-2:24b-cloud

## Original Code:

def is_nonagonal(n): 
	return int(n * (7 * n - 5) / 2) 

## Refactored Code:

```python
def is_nonagonal(n):
    """
    Calculate the nth nonagonal number.

    The nth nonagonal number is given by the formula: n * (7 * n - 5) / 2

    Args:
        n (int): The position in the sequence of nonagonal numbers.

    Returns:
        int: The nth nonagonal number.
    """
    return int(n * (7 * n - 5) / 2)
```

- The function `is_nonagonal` calculates the nth nonagonal number using the exact same formula as the original implementation.
- The function signature and return type remain unchanged.
- The logic and input/output behavior are preserved exactly as in the original code.
- The function name and variable names remain the same.
- The mathematical equation for nonagonal numbers is kept identical to the original.
- The function is designed to work with integer inputs and returns an integer result.
- The implementation is straightforward and maintains readability while preserving the original behavior.
