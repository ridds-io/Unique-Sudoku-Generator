import time
import random
import pygame
from tabulate import tabulate

# N is the size of the 2D matrix (9*9)
N = 9

# Global variables
start_time = None
total_pause_time = 0  # Total accumulated pause time
pause_start_time = 0  # When the current pause began
is_paused = False
current_username = ""

def main():
    global start_time, total_pause_time, is_paused, current_username, pause_start_time

    # Initialize pygame
    pygame.init()
    pygame.font.init()
    
    # Set mode initializes window and sets the size of the window
    Window = pygame.display.set_mode((600, 600))
    
    # Set title
    pygame.display.set_caption("SUDOKU GAME by Ridds-io")
    
    # Show user login screen
    current_username = show_login_screen(Window)
    
    # Get user's difficulty preference
    difficulty_level = show_difficulty_selection(Window)
    
    # Set units_erased based on difficulty level
    if difficulty_level == "easy":
        units_erased = 45
    elif difficulty_level == "intermediate":
        units_erased = 55
    else:  # difficult
        units_erased = 62
    
    # This generates an empty grid with shuffled first row
    sudoku = shuffle_first_row(initialize_grid(N))
    
    # fill_grid function solves and edits sudoku variable to have filled grid
    if fill_grid(sudoku):
        solution_grid = [row[:] for row in sudoku]
    
    # Generates the question grid with unique solution
    question_grid = create_unique_question_grid(solution_grid, units_erased)
    
    # Size of each cell
    diff = 45
    
    font = pygame.font.SysFont("comicsans", 20)
    font1 = pygame.font.SysFont("comicsans", 30)
    button_font = pygame.font.SysFont("comicsans", 15)
    
    # user_grid is the grid the user is going to be able to make changes to
    user_grid = [row[:] for row in question_grid]
    
    running = True
    selected = False
    value = 0
    x, z = 0, 0  # coordinates for selected cell
    
    # start the timer
    start_time = time.time()
    total_pause_time = 0
    is_paused = False
    
    # Create buttons - centered in the blank space
    pause_button = pygame.Rect(480, 50, 100, 30)
    quit_button = pygame.Rect(480, 90, 100, 30)
    
    # Pause overlay buttons (will be initialized later)
    resume_button = None
    pause_quit_button = None
    
    # Calculate grid size
    grid_size = diff * 9
    
    # Center the grid horizontally and vertically
    grid_x_offset = (600 - grid_size) // 2
    grid_y_offset = 150
    
    while running:
        current_time = calculate_current_time()
        
        # Fill the window with light purple background
        Window.fill((230, 220, 240))
        
        # Draw timer
        timer_text = font1.render(f"Time: {format_time(current_time)}", True, (50, 50, 50))
        Window.blit(timer_text, (20, 20))
        
        # Draw username
        username_text = font1.render(f"Player: {current_username}", True, (50, 50, 50))
        Window.blit(username_text, (20, 60))
        
        # Draw difficulty
        difficulty_text = font1.render(f"Difficulty: {difficulty_level}", True, (50, 50, 50))
        Window.blit(difficulty_text, (20, 100))
        
        # Draw buttons with lilac color and properly centered text
        pygame.draw.rect(Window, (200, 190, 230), pause_button)
        pygame.draw.rect(Window, (200, 160, 200), quit_button)
        
        pause_text = button_font.render("PAUSE", True, (50, 50, 50))
        quit_text = button_font.render("QUIT", True, (50, 50, 50))
        
        # Center the text in the buttons
        pause_text_rect = pause_text.get_rect(center=pause_button.center)
        quit_text_rect = quit_text.get_rect(center=quit_button.center)
        
        Window.blit(pause_text, pause_text_rect)
        Window.blit(quit_text, quit_text_rect)
        
        # First draw the white background for empty cells
        for i in range(9):
            for j in range(9):
                if question_grid[i][j] == 0: # empty cell
                    pygame.draw.rect(Window, (255, 255, 255), 
                                    (j * diff + grid_x_offset, i * diff + grid_y_offset, diff + 1, diff + 1))
        
        # Then highlight the clues given
        drawlines(question_grid, Window, diff, font, grid_x_offset, grid_y_offset)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                
                if is_paused:
                    # Check if resume button was clicked during pause
                    if resume_button and resume_button.collidepoint(pos):
                        toggle_pause()
                        continue
                    
                    # Check if quit button was clicked during pause
                    if pause_quit_button and pause_quit_button.collidepoint(pos):
                        running = False
                        continue
                else:
                    # Check if pause button was clicked
                    if pause_button.collidepoint(pos):
                        toggle_pause()
                        continue
                    
                    # Check if quit button was clicked
                    if quit_button.collidepoint(pos):
                        running = False
                        continue
                    
                    # Check if clicked on grid (with offset)
                    if (grid_x_offset <= pos[0] < grid_x_offset + grid_size and 
                        grid_y_offset <= pos[1] < grid_y_offset + grid_size):
                        x = int((pos[0] - grid_x_offset) // diff)
                        z = int((pos[1] - grid_y_offset) // diff)
                        selected = True
                    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    toggle_pause()
                    continue
                
                if not is_paused:
                    if event.key == pygame.K_LEFT:
                        x = max(0, x - 1)
                    if event.key == pygame.K_RIGHT:
                        x = min(8, x + 1)
                    if event.key == pygame.K_UP:
                        z = max(0, z - 1)
                    if event.key == pygame.K_DOWN:
                        z = min(8, z + 1)
                        
                    # Number inputs
                    if pygame.K_1 <= event.key <= pygame.K_9:
                        value = event.key - pygame.K_0
                        if selected and question_grid[z][x] == 0:
                            user_grid[z][x] = value
                            value = 0
                    
                    # Clear current cell with backspace or delete
                    if (event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE):
                        if selected and question_grid[z][x] == 0:  # Only clear if not a fixed number
                            user_grid[z][x] = 0
                            
                    # To check if sudoku is solved
                    if event.key == pygame.K_RETURN:
                        if is_solved(user_grid, solution_grid):
                            elapsed_time = current_time
                            
                            # Display victory message
                            show_victory_screen(Window, elapsed_time)
                            
                            # Generate a new puzzle
                            sudoku = shuffle_first_row(initialize_grid(N))
                            if fill_grid(sudoku):
                                solution_grid = [row[:] for row in sudoku]
                            question_grid = create_unique_question_grid(solution_grid, units_erased)
                            user_grid = [row[:] for row in question_grid]
                            
                            # Reset timer
                            start_time = time.time()
                            total_pause_time = 0
                            is_paused = False
                        else:
                            show_not_solved_message(Window)
                            
                    # If r key is pressed, a new sudoku grid should be generated 
                    if event.key == pygame.K_r:
                        sudoku = shuffle_first_row(initialize_grid(N))
                        if fill_grid(sudoku):
                            solution_grid = [row[:] for row in sudoku]
                        question_grid = create_unique_question_grid(solution_grid, units_erased)
                        user_grid = [row[:] for row in question_grid]
                        
                        # Restart the timer for the new grid
                        start_time = time.time()
                        total_pause_time = 0
                        is_paused = False
                        
                    # If d key is pressed, all user inputs are erased
                    elif event.key == pygame.K_d:
                        user_grid = [row[:] for row in question_grid]
                        
                    # If 'a' letter key is pressed, all answers are displayed
                    elif event.key == pygame.K_a:
                        user_grid = [row[:] for row in solution_grid]
                    
        # Draw grid and input
        draw_grid(Window, user_grid, diff, font, grid_x_offset, grid_y_offset)
        if selected and not is_paused:
            highlight_cell(Window, x, z, diff, grid_x_offset, grid_y_offset)
            
        # Show pause overlay if game is paused
        if is_paused:
            resume_button, pause_quit_button = show_pause_overlay(Window)
            
        pygame.display.update()
        
    pygame.quit()

def toggle_pause():
    global is_paused, total_pause_time, pause_start_time
    
    current_time = time.time()
    if is_paused:
        # Resume the game - add this pause duration to total
        is_paused = False
        total_pause_time += (current_time - pause_start_time)
    else:
        # Pause the game - record when the pause started
        is_paused = True
        pause_start_time = current_time

def calculate_current_time():
    global start_time, total_pause_time, is_paused, pause_start_time
    
    current_time = time.time()
    if is_paused:
        # When paused, don't count time since pause started
        return (current_time - start_time) - (current_time - pause_start_time) - total_pause_time
    else:
        # When running, subtract all pause time
        return (current_time - start_time) - total_pause_time

def format_time(seconds):
    minutes, seconds = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    if hours > 0:
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes:02d}:{seconds:02d}"

def show_login_screen(window):
    font = pygame.font.SysFont("comicsans", 30)
    input_box = pygame.Rect(200, 250, 200, 50)
    submit_button = pygame.Rect(250, 320, 100, 40)
    
    username = ""
    active = True
    done = False
    
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if submit_button.collidepoint(event.pos) and username:
                    done = True
                    
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN and username:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    else:
                        username += event.unicode
        
        # Light purple background
        window.fill((230, 220, 240))
        
        # Draw title
        title_text = font.render("Sudoku Game", True, (50, 50, 50))
        window.blit(title_text, (225, 150))
        
        # Draw input prompt
        prompt_text = font.render("Enter Username:", True, (50, 50, 50))
        window.blit(prompt_text, (215, 200))
        
        # Draw input box
        pygame.draw.rect(window, (255, 255, 255), input_box)  # White input box
        pygame.draw.rect(window, (80, 80, 80), input_box, 2)
        
        # Draw username text
        text_surface = font.render(username, True, (50, 50, 50))
        window.blit(text_surface, (input_box.x + 5, input_box.y + 10))
        
        # Draw submit button with lilac color
        pygame.draw.rect(window, (200, 190, 230), submit_button)
        
        # Center the text in the button
        submit_text = font.render("Start", True, (50, 50, 50))
        submit_text_rect = submit_text.get_rect(center=submit_button.center)
        window.blit(submit_text, submit_text_rect)
        
        pygame.display.flip()
        
    return username

def show_difficulty_selection(window):
    font = pygame.font.SysFont("comicsans", 30)
    
    easy_button = pygame.Rect(200, 200, 200, 50)
    intermediate_button = pygame.Rect(200, 270, 200, 50)
    difficult_button = pygame.Rect(200, 340, 200, 50)
    
    done = False
    
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_button.collidepoint(event.pos):
                    return "easy"
                elif intermediate_button.collidepoint(event.pos):
                    return "intermediate"
                elif difficult_button.collidepoint(event.pos):
                    return "difficult"
        
        # Light purple background
        window.fill((230, 220, 240))
        
        # Draw title
        title_text = font.render("Select Difficulty", True, (50, 50, 50))
        window.blit(title_text, (210, 120))
        
        # Draw buttons with lilac color
        pygame.draw.rect(window, (200, 190, 230), easy_button)  # Lilac color
        pygame.draw.rect(window, (190, 180, 220), intermediate_button)  # Slightly darker lilac
        pygame.draw.rect(window, (180, 170, 210), difficult_button)  # Even darker lilac
        
        # Draw button texts with proper centering
        easy_text = font.render("Easy", True, (50, 50, 50))
        intermediate_text = font.render("Intermediate", True, (50, 50, 50))
        difficult_text = font.render("Difficult", True, (50, 50, 50))
        
        # Center text in buttons
        easy_text_rect = easy_text.get_rect(center=easy_button.center)
        intermediate_text_rect = intermediate_text.get_rect(center=intermediate_button.center)
        difficult_text_rect = difficult_text.get_rect(center=difficult_button.center)
        
        window.blit(easy_text, easy_text_rect)
        window.blit(intermediate_text, intermediate_text_rect)
        window.blit(difficult_text, difficult_text_rect)
        
        pygame.display.flip()

def show_victory_screen(window, time_taken):
    font = pygame.font.SysFont("comicsans", 40)
    message_font = pygame.font.SysFont("comicsans", 30)
    
    overlay = pygame.Surface((600, 600), pygame.SRCALPHA)
    overlay.fill((50, 50, 70, 150))
    window.blit(overlay, (0, 0))
    
    # Draw victory message
    victory_text = font.render("Puzzle Solved!", True, (220, 220, 100))
    victory_rect = victory_text.get_rect(center=(300, 220))
    window.blit(victory_text, victory_rect)
    
    # Draw time message
    time_text = message_font.render(f"Time: {format_time(time_taken)}", True, (220, 220, 220))
    time_rect = time_text.get_rect(center=(300, 280))
    window.blit(time_text, time_rect)
    
    # Draw continue message
    continue_text = message_font.render("Press any key to continue", True, (220, 220, 220))
    continue_rect = continue_text.get_rect(center=(300, 340))
    window.blit(continue_text, continue_rect)
    
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

def show_not_solved_message(window):
    font = pygame.font.SysFont("comicsans", 30)
    
    original_surface = window.copy()
    
    overlay = pygame.Surface((600, 600), pygame.SRCALPHA)
    overlay.fill((50, 50, 70, 150))
    window.blit(overlay, (0, 0))
    
    # Draw message
    message_text = font.render("Not solved yet! Keep trying!", True, (220, 150, 150))
    message_rect = message_text.get_rect(center=(300, 250))
    window.blit(message_text, message_rect)
    
    pygame.display.flip()
    
    # Wait for 1.5 seconds
    pygame.time.delay(1500)
    
    # Restore original screen
    window.blit(original_surface, (0, 0))
    pygame.display.flip()

def show_pause_overlay(window):
    font = pygame.font.SysFont("comicsans", 40)
    button_font = pygame.font.SysFont("comicsans", 25)
    
    overlay = pygame.Surface((600, 600), pygame.SRCALPHA)
    overlay.fill((50, 50, 70, 150))
    window.blit(overlay, (0, 0))
    
    # Draw pause message
    pause_text = font.render("GAME PAUSED", True, (220, 220, 220))
    pause_rect = pause_text.get_rect(center=(300, 250))
    window.blit(pause_text, pause_rect)
    
    # Create resume and quit buttons
    resume_button = pygame.Rect(200, 320, 200, 40)
    quit_button = pygame.Rect(200, 380, 200, 40)
    
    # Draw buttons with lilac colors
    pygame.draw.rect(window, (200, 190, 230), resume_button)  # Lilac color
    pygame.draw.rect(window, (200, 160, 200), quit_button)    # Darker lilac
    
    # Draw button text
    resume_button_text = button_font.render("RESUME", True, (50, 50, 50))
    quit_button_text = button_font.render("QUIT", True, (50, 50, 50))
    
    # Center text in buttons
    resume_text_rect = resume_button_text.get_rect(center=resume_button.center)
    quit_text_rect = quit_button_text.get_rect(center=quit_button.center)
    
    window.blit(resume_button_text, resume_text_rect)
    window.blit(quit_button_text, quit_text_rect)
    
    # Draw spacebar instruction (smaller and below buttons)
    space_text = pygame.font.SysFont("comicsans", 20).render("or press SPACE to resume", True, (180, 180, 180))
    space_rect = space_text.get_rect(center=(300, 440))
    window.blit(space_text, space_rect)
    
    return resume_button, quit_button  # Return button rects so we can check for clicks

# Initializes the grid to have only 0s
def initialize_grid(N):
    rows = N
    cols = N
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    return grid

# Search grid to find an entry that is still unassigned
# l is a list that keeps track of current position
def find_empty_location(arr, l):
    for row in range(9):
        for col in range(9):
            if (arr[row][col] == 0):
                l[0] = row
                l[1] = col
                return True
    return False

# Check if number is present in the row
def used_in_row(arr, row, num):
    for i in range(9):
        if (arr[row][i] == num):
            return True
    return False

# Check if number is present in the column
def used_in_column(arr, col, num):
    for i in range(9):
        if (arr[i][col] == num):
            return True
    return False

# Check if number is present in the given box
def used_in_box(arr, row, col, num):
    for i in range(3):
        for j in range(3):
            if (arr[row + i][col + j] == num):
                return True
    return False

# Check if the number is acceptable for a particular cell
def is_safe(arr, row, col, num):
    return (not used_in_row(arr, row, num) and
            (not used_in_column(arr, col, num) and
            (not used_in_box(arr, row - row % 3, col - col % 3, num))))

def choose_random_number(start, end):
    i = int(random.uniform(start, end))
    return i

# ORIGINAL PLAN:
# finds a random start location 
# fill 5 random spaces with a random number

# OBSERVATION 1:
# most sudokus had 1 2 3 4 5 6 7 8 9 as their first line
# until and unless the very first number is something else
# hence hard coding in the randomize function to choose different first numbers (arr[0][0])

# OBSERVATION 2:
# even if the first number is random,
# the other numbers form an ascending pattern only
# so the solution is to shuffle the first row entirely 
def shuffle_first_row(arr):
    list_of_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    random.shuffle(list_of_numbers)
    for i in range(len(list_of_numbers)):
        arr[0][i] = list_of_numbers[i]
    return arr

# Checks if sudoku is solvable
# Fills the grid with numbers to generate a solved sudoku square
def fill_grid(arr):
    # l is the start position
    l = [0, 0]

    # If there are no empty locations, sudoku is solved
    if (not find_empty_location(arr, l)):
        return True

    # Assigning row and col values
    row = l[0]
    col = l[1]

    # Trying to fill out digits (1-9)
    for num in range(1, 10):
        if is_safe(arr, row, col, num):
            # Assuming a number
            arr[row][col] = num

            # This is a recursive function
            # Returns True if successfully solved
            if (fill_grid(arr)):
                return True
            
            # If fails then unmake assumption
            arr[row][col] = 0

    # Trigger backtracking
    return False

# Counts how many solutions a sudoku puzzle has
def count_solutions(grid):
    # Make a copy of the grid to avoid modifying the original
    grid_copy = [row[:] for row in grid]
    count = [0]  # Use a list to store count for pass by reference
    
    # Helper function for backtracking
    def backtrack(grid):
        # Find empty cell
        l = [0, 0]
        if not find_empty_location(grid, l):
            count[0] += 1
            return
        
        row, col = l[0], l[1]
        
        # Try digits 1-9
        for num in range(1, 10):
            if is_safe(grid, row, col, num):
                grid[row][col] = num
                
                # If we've already found 2 solutions, we can stop
                if count[0] < 2:
                    backtrack(grid)
                
                grid[row][col] = 0
    
    backtrack(grid_copy)
    return count[0]

# Create a sudoku puzzle with exactly one solution
def create_unique_question_grid(solution_grid, units_erased=55):
    max_attempts = 50  # Limit attempts to avoid infinite loop
    
    for _ in range(max_attempts):
        question = [row[:] for row in solution_grid]
        cells_to_erase = []
        
        # Create a list of all cell positions
        for i in range(9):
            for j in range(9):
                cells_to_erase.append((i, j))
        
        # Shuffle the list of cells to erase
        random.shuffle(cells_to_erase)
        
        # Erase cells one by one
        erased_count = 0
        for i, j in cells_to_erase:
            if erased_count >= units_erased:
                break
                
            # Save the original value
            temp = question[i][j]
            question[i][j] = 0
            erased_count += 1
            
            # Check if the puzzle still has exactly one solution
            if count_solutions(question) != 1:
                # If not, restore the value
                question[i][j] = temp
                erased_count -= 1
        
        # If we've erased enough cells, return the puzzle
        if erased_count >= 0.7 * units_erased:  # Allow some flexibility
            return question
    
    # If we couldn't create a unique solution puzzle, create a normal one
    print("Could not create a unique solution puzzle. Creating a standard puzzle instead.")
    return create_question_grid(solution_grid, units_erased)

# Takes the grid and randomly reassigns value 0 to {units_erased} cells
def create_question_grid(arr, units_erased=55):
    question = [row[:] for row in arr]
    count = 0 
    while count != units_erased:
        i = choose_random_number(0, 9)
        j = choose_random_number(0, 9)
        if question[i][j] != 0:
            question[i][j] = 0
            count += 1
    return question

# Highlights the cell selected by the user with lighter border
def highlight_cell(Window, x, z, diff, x_offset, y_offset):
    pygame.draw.rect(Window, (150, 150, 220), 
                    (x * diff + x_offset, z * diff + y_offset, diff, diff), 3)

# Draws the sudoku grid on the opened window
def draw_grid(Window, grid, diff, font, x_offset, y_offset):
    for i in range(9):
        for j in range(9):
            if grid[j][i] != 0:
                value = font.render(str(grid[j][i]), True, (50, 50, 50))
                Window.blit(value, (i * diff + 15 + x_offset, j * diff + 15 + y_offset))
                
    for i in range(10):
        pygame.draw.line(Window, (50, 50, 50), 
                        (0 + x_offset, i * diff + y_offset), 
                        (9 * diff + x_offset, i * diff + y_offset), 
                        2 if i % 3 == 0 else 1)
        pygame.draw.line(Window, (50, 50, 50), 
                        (i * diff + x_offset, 0 + y_offset), 
                        (i * diff + x_offset, 9 * diff + y_offset), 
                        2 if i % 3 == 0 else 1)

# Highlights the clues given (fixed numbers)
def drawlines(question_grid, Window, diff, font, x_offset, y_offset):
    for i in range(9):
        for j in range(9):
            if question_grid[i][j] != 0:  
                # Gives the fixed numbers a light purple background
                pygame.draw.rect(Window, (215, 200, 235), 
                                (j * diff + x_offset, i * diff + y_offset, diff + 1, diff + 1))
                text1 = font.render(str(question_grid[i][j]), 1, (50, 50, 50)) 
                Window.blit(text1, (j * diff + 15 + x_offset, i * diff + 15 + y_offset))

# Checks if the user_grid is a valid solution
def is_valid_solution(user_grid):
    # Check that all cells are filled
    for row in user_grid:
        if 0 in row:
            return False
            
    # Check rows and columns
    for i in range(9):
        if len(set(user_grid[i])) != 9 or len(set(row[i] for row in user_grid)) != 9:
            return False
    # Check the 3x3 sub-grids
    for box_row in range(0, 9, 3):
        for box_col in range(0, 9, 3):
            subgrid = [user_grid[row][col] for row in range(box_row, box_row + 3) for col in range(box_col, box_col + 3)]
            if len(set(subgrid)) != 9:
                return False
    return True

# Check if the sudoku is solved
def is_solved(user_grid, solution_grid):
    if user_grid == solution_grid or is_valid_solution(user_grid):
        return True
    else:
        return False

# Prints the grid as a sudoku square
def printing(N, arr):
    print(tabulate(arr, tablefmt="grid"))

if __name__ == "__main__":
    main()
