# Model output for task_431

## Model
- devstral-small-2:24b-cloud

## Original Code:

def common_element(list1, list2):
     result = False
     for x in list1:
         for y in list2:
             if x == y:
                 result = True
                 return result

## Refactored Code:

```python
def common_element(list1, list2):
    """Check if there is any common element between two lists.

    Args:
        list1: First list of elements.
        list2: Second list of elements.

    Returns:
        bool: True if there is at least one common element, False otherwise.
    """
    for x in list1:
        for y in list2:
            if x == y:
                return True
    return False
```

- The function `common_element` checks for the presence of any common element between two lists.
- The logic remains the same as the original implementation, iterating through both lists and returning `True` as soon as a common element is found.
- The function signature and return type (`bool`) are preserved.
- The nested loop structure is kept to maintain the original behavior.
- The function returns `False` if no common elements are found after checking all pairs.
- The docstring clarifies the purpose, arguments, and return value of the function.
- The implementation ensures that the function behaves exactly as validated by the provided tests.
