# Model output for task_488

## Model
- devstral-small-2:24b-cloud

## Original Code:

import math
def area_pentagon(a):
  area=(math.sqrt(5*(5+2*math.sqrt(5)))*pow(a,2))/4.0
  return area

## Refactored Code:

```python
import math

def area_pentagon(a):
    """Calculate the area of a regular pentagon with side length a.

    Args:
        a (float): Side length of the pentagon.

    Returns:
        float: Area of the pentagon calculated using the formula:
               (sqrt(5*(5 + 2*sqrt(5))) * a^2) / 4
    """
    area = (math.sqrt(5 * (5 + 2 * math.sqrt(5))) * pow(a, 2)) / 4.0
    return area
```

- All function and variable names remain unchanged
- The mathematical formula for pentagon area is preserved exactly
- Input and output types remain consistent (float input, float output)
- The implementation is placed in the `tasks/` directory
- Floating-point precision is maintained as per original implementation
- The function signature and return type are explicitly documented
- The logic and equation are identical to the original implementation
