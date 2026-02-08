# Model output for task_882

## Model
- devstral-small-2:24b-cloud

## Original Code:

def parallelogram_perimeter(b,h):
  perimeter=2*(b*h)
  return perimeter

## Refactored Code:

```python
def parallelogram_perimeter(b, h):
    """Calculate the perimeter of a parallelogram given base and height.

    Args:
        b (float): Length of the base of the parallelogram.
        h (float): Height of the parallelogram.

    Returns:
        float: Perimeter of the parallelogram calculated as 2 * (b * h).
    """
    perimeter = 2 * (b * h)
    return perimeter
```

- All function and variable names remain unchanged (`parallelogram_perimeter`, `b`, `h`, `perimeter`).
- The mathematical equation `2 * (b * h)` is preserved exactly as in the original code.
- The function signature and return type are explicitly documented.
- The logic and input/output behavior are identical to the original implementation.
- The function is placed in the `tasks/` directory as required.
- Floating-point precision is maintained as per the original implementation (no rounding or truncation applied).
- The docstring clarifies the purpose, arguments, and return value of the function.
