# Unique Sudoku Generator
A feature-rich, interactive Sudoku puzzle game built with Python and Pygame. This game provides an engaging sudoku experience with multiple difficulty levels, timer functionality, pause/resume capability, and various user-friendly features.


## Video Demo: 
<URL HERE>


## How it works

1. Running the code will open a sudoku welcome screen
<img width="300" alt="Screenshot 2025-04-05 at 3 39 17 PM" src="https://github.com/user-attachments/assets/11831632-de06-4277-bd2c-d81b306a9ea5" />

<br>
<br>
  
2. Enter user name and chose difficulty level
<img width="300" alt="Screenshot 2025-04-05 at 3 42 04 PM" src="https://github.com/user-attachments/assets/d1749068-2f73-4e84-bbd5-326baa4034d6" />

<img width="300" alt="Screenshot 2025-04-05 at 3 42 25 PM" src="https://github.com/user-attachments/assets/eae8e38c-8af5-4728-b2f3-c7f0ccd63330" />

<br>
<br>
  
3. A sudoku question grid of respective difficulty will open up
<img width="300" alt="Screenshot 2025-04-05 at 3 44 48 PM" src="https://github.com/user-attachments/assets/fb788e1c-e9f7-4f66-a7dc-bfc4d07e68c0" />

## Project Overview
<img width="938" height="747" alt="Screenshot 2025-07-12 at 12 20 23 PM" src="https://github.com/user-attachments/assets/287783e5-8c19-4b1a-a24c-89e7410d43ce" />

### Further Functionalities:

- You can enter any number from 1-9 in the empty squares.
- Any other key and the number 0 are not recognised as valid inputs.
- Pressing the space bar will Pause the game.
- Pressing the space bar again will Resume the game.
- Pressing the 'D' key will delete all user solutions and allow user to retry solving the sudoku.
- Pressing the 'A' key will reveal answers.
  After pressing the A key however, you cannot go back to your solutions.
  If someone wishes to see the answers, the only way to attempt the same sudoku again is by pressing the 'D' key.
- Pressing the 'R' key will reload the sudoku grid to display a new sudoku.
  The timer at the top of the sudoku screen is also restarted.
- Pressing the 'Enter' key will either display a Congratulatory message on solving correctly,
  or display a Try Again message that closes on its own in 10 seconds.
- Pressing the 'Backspace' or 'Delete' key will allow user to clear currently selected cell,
  (as long as the currently selected cell is NOT a clue cell)
