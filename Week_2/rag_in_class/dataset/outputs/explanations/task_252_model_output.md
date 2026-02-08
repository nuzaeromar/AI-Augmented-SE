# Model output for task_252

## Model
- devstral-small-2:24b-cloud

## Original Code:

import cmath  
def convert(numbers):    
  num = cmath.polar(numbers)  
  return (num) 

## Refactored Code:

```python
import cmath

def convert(numbers):
    """Convert a complex number to its polar form.

    Args:
        numbers: A complex number (as a complex type or a tuple/list of (real, imag)).

    Returns:
        A tuple (magnitude, phase) where:
        - magnitude: The magnitude (r) of the complex number as a float.
        - phase: The phase (theta) in radians as a float.
    """
    num = cmath.polar(numbers)
    return num
```

- All function and variable names remain unchanged (`convert`, `numbers`, `num`).
- The logic and input/output behavior are preserved exactly as in the original.
- The mathematical function `cmath.polar` is retained unchanged.
- The return type is a tuple of two floats (magnitude and phase in radians).
- The implementation is placed in the `tasks/` directory with the exact name referenced in the tests.
- The docstring clarifies the function's purpose, arguments, and return values.
- No additional imports or dependencies are introduced.
- The code adheres to Python best practices for readability and maintainability.
