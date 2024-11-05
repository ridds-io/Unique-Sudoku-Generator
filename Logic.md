# Logic

## The personalised sudoku generator works on four main functions:

<br>

1. Generating a playable sudoku square of particular complexity
2. Recording time taken by the user to solve
3. Assume certain time conventions for difficulty:
   for example:

      - easy level sudoku = 5 minutes
      - medium level sudoku = 15 minutes
      - difficult level sudoku = 30 minutes
        
4. Changing the difficulty of a sudoku based on solving time

<br>

### Now looking into each of those steps further:

<br>

1. Generating a playable sudoku square of particular complexity

- <B>Create a Grid:</B> Start with an empty 9x9 grid.
- <B>Backtracking Function:</B> Write a function that attempts to fill the grid by placing numbers 1-9 in each cell, checking if the placement is valid.
- <B>Validation:</B> Ensure that each number placement follows Sudoku rules (no duplicates in rows, columns, or 3x3 subgrids).
- <B>Recursion:</B> If a valid number is placed, recursively attempt to fill the next cell. If no valid number can be placed, backtrack by removing the last placed number and trying the next possibility.

Here's a high-level pseudocode outline:

```
function solve(grid):
    if grid is complete:
        return true
    for each number from 1 to 9:
        if number is valid in current cell:
            place number in cell
            if solve(grid):
                return true
            remove number from cell
    return false
```





