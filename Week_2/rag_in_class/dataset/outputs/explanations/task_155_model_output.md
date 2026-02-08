# Model output for task_155

## Model
- devstral-small-2:24b-cloud

## Original Code:

def even_bit_toggle_number(n) : 
    res = 0; count = 0; temp = n 
    while (temp > 0) :     
        if (count % 2 == 1) : 
            res = res | (1 << count)      
        count = count + 1
        temp >>= 1 
    return n ^ res 

## Refactored Code:

```python
def even_bit_toggle_number(n):
    """
    Toggles the even-positioned bits (0-indexed from right) of the given integer n.

    Args:
        n (int): The input integer whose even-positioned bits will be toggled.

    Returns:
        int: The integer with even-positioned bits toggled.
    """
    res = 0
    count = 0
    temp = n
    while temp > 0:
        if count % 2 == 1:
            res = res | (1 << count)
        count += 1
        temp >>= 1
    return n ^ res
```

- Function signature and return type remain exactly the same.
- Variable names (`res`, `count`, `temp`) are preserved.
- Logic for toggling even-positioned bits is unchanged.
- Mathematical operations (bitwise OR, left shift, XOR) are identical to the original.
- All test cases should pass as the behavior is preserved.
- Code formatting improved for readability (consistent spacing, indentation).
- Docstring added to clarify function purpose, arguments, and return value.
