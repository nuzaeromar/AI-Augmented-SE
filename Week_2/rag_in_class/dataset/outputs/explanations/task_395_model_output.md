# Model output for task_395

## Model
- devstral-small-2:24b-cloud

## Original Code:

def first_non_repeating_character(str1):
  char_order = []
  ctr = {}
  for c in str1:
    if c in ctr:
      ctr[c] += 1
    else:
      ctr[c] = 1 
      char_order.append(c)
  for c in char_order:
    if ctr[c] == 1:
      return c
  return None

## Refactored Code:

```python
def first_non_repeating_character(str1):
    """Return the first non-repeating character in the input string.

    Args:
        str1 (str): The input string to search for the first non-repeating character.

    Returns:
        str or None: The first non-repeating character, or None if all characters repeat.
    """
    char_order = []
    ctr = {}
    for c in str1:
        if c in ctr:
            ctr[c] += 1
        else:
            ctr[c] = 1
            char_order.append(c)
    for c in char_order:
        if ctr[c] == 1:
            return c
    return None
```

- All function and variable names remain unchanged.
- The logic for tracking character counts and order is preserved.
- The return type and behavior (returning the first non-repeating character or None) are maintained.
- The implementation handles edge cases (e.g., all characters repeating) as in the original.
- The mathematical logic (counting occurrences) is identical to the original.
- The function signature and return type are explicitly documented.
- The code structure and flow are improved for readability while keeping the original logic.
