# Logic

## The personalised sudoku generator works on four main functions:

<Br>

1. Generating a playable sudoku square of particular complexity
2. Recording time taken by the user to solve
3. Determining difficulty catered solving time
   for example:

      - easy level sudoku = 5 minutes
      - medium level sudoku = 15 minutes
      - difficult level sudoku = 30 minutes
        
4. Changing the difficulty of a sudoku based on solving time

<br>

### Now looking into each of those steps further:

<br>

## 1. Generating a playable sudoku square of particular complexity

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

## 2. Recording time taken by the user to solve

Tracking the solving time by using the time.time() function and subtracting current time from start time

<Br>

## 3. Determining difficulty catered solving time

Start with some assumptions and then refine them based on user data. Here’s a possible strategy:

<B>Initial Assumptions:</B> Start with a baseline time for each difficulty level. For example, assume an "easy" puzzle takes 5 minutes, a "medium" puzzle takes 10 minutes, and a "hard" puzzle takes 20 minutes.

<B>Thresholds:</B> Set thresholds for what constitutes a quick or slow solve. For example:

If the user solves an "easy" puzzle in less than 4 minutes, increase the difficulty.
If the user takes more than 6 minutes, decrease the difficulty.

<B>Adjust Difficulty:</B> Based on the solving time, adjust the number of pre-filled cells or the complexity of the puzzle for the next round.

<Br>

## 4. Changing the difficulty of a sudoku based on solving time

<B>Number of Clues:</B> Easier puzzles have more pre-filled cells, while harder puzzles have fewer. You can adjust the number of clues based on the time taken to solve the previous puzzle.

<B>Clue Distribution:</B> The placement of clues can also affect difficulty. For example, evenly distributed clues might make the puzzle easier, while clustering them in certain areas can make it harder.

<B>Puzzle Generation Algorithm:</B> You can use different algorithms to generate puzzles of varying difficulty. Some algorithms are designed to create puzzles that require more advanced solving techniques.

