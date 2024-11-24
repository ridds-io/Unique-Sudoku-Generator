import time
import random
from tabulate import tabulate
import pygame


# N is the size of the 2D matrix (9*9)
N = 9

# coordinates for selected cell
x, z = 0, 0
start_time = None

def main():
    global start_time

    # this generates an empty grid with shuffled first row
    sudoku = shuffle_first_row(initialize_grid(N))

    # fill_grid function solves and edits sudoku variable to have filled grid
    # if it returns true, create a copy of the sudoku grid
    # solution_grid = answered sudoku grid
    if fill_grid(sudoku):
        solution_grid = [row[:] for row in sudoku]  

    # generates the question grid
    '''GENERATING A QUESTION GRID NEEDS TO BE WORKED ON TO INCORPORATE COMPLEXITY'''
    question_grid = create_question_grid(solution_grid, complexity(units_erased=45, solving_time=10))

    '''THIS IS JUST FOR DEMO PURPOSES'''
    '''SO AS TO SOLVE SUDOKU QUICKLY'''
    printing(N, solution_grid)

    # incorporating pygame
    pygame.font.init()

    # set mode initializes window and sets the size of the window
    Window = pygame.display.set_mode((500, 500))

    # set caption or title
    pygame.display.set_caption("SUDOKU GAME by Ridds-io")

    # size of each cell is 500/9
    diff = 500 / 9
    font = pygame.font.SysFont("comicsans", 20)
    font1 = pygame.font.SysFont("comicsans", 40)

    # user_grid is the grid the user is going to be able to make changes to
    user_grid = [row[:] for row in question_grid]
    running = True
    selected = False
    value = 0

    
    # start the timer
    start_time = time.time()

    while running:
        # fill the sudoku with a pink background
        Window.fill((255, 182, 193))  

        # draw the sudoku grid on the window
        drawlines(question_grid, Window, diff, font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    x, z = int(pos[0] // diff), int(pos[1] // diff)
                    selected = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x-= 1
                    flag1 = 1
                if event.key == pygame.K_RIGHT:
                    x+= 1
                    flag1 = 1
                if event.key == pygame.K_UP:
                    z-= 1
                    flag1 = 1
                if event.key == pygame.K_DOWN:
                    z+= 1
                    flag1 = 1   
                if event.key == pygame.K_1:
                    value = 1
                if event.key == pygame.K_2:
                    value = 2   
                if event.key == pygame.K_3:
                    value = 3
                if event.key == pygame.K_4:
                    value = 4
                if event.key == pygame.K_5:
                    value = 5
                if event.key == pygame.K_6:
                    value = 6
                if event.key == pygame.K_7:
                    value = 7
                if event.key == pygame.K_8:
                    value = 8
                if event.key == pygame.K_9:
                    value = 9 
                if event.key == pygame.K_RETURN:
                    if is_solved(user_grid, solution_grid):
                        print(f"Well Done! You have solved the sudoku in {time_tracker(start_time)}!")
                        running = False 
                # if r key is pressed, a new sudoku grid should be generated 
                if event.key == pygame.K_r:
                    user_grid = create_question_grid(solution_grid)
                    
                    # restart the timer for the new grid
                    start_time = time.time()  
                elif event.key == pygame.K_d:
                    user_grid = [row[:] for row in question_grid]
                elif pygame.K_1 <= event.key <= pygame.K_9:
                    value = event.key - pygame.K_0
                    if selected and question_grid[z][x] == 0:
                            user_grid[z][x] = value
                            value = 0

    # Draw grid and input
        draw_grid(Window, user_grid, diff, font)
        if selected:
            highlight_cell(Window, x, z, diff)

        pygame.display.update()

    pygame.quit()



# STEP 1: GENERATING A FULLY SOLVED SUDOKU SQUARE -X-


# measures the time taken by the user to solve the sudoku
# returns a formatted string containing time taken
def time_tracker(start_time):
    # ideally should only start tracking time function after user starts filling in the grid
    # work on that later
    end_time = time.time()
    time_taken = round(end_time - start_time, 2) / 60
    # formatting in hours and minutes
    if time_taken > 60:
        time_taken = f"{time_taken//60} hours and {time_taken-((time_taken//60)*60)} minutes"
    else:
        time_taken = f"{time_taken} minutes" 
    return time_taken

# initialises the grid to have only 0s
def initialize_grid(N):
    rows = N
    cols = N
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    return grid


# search grid to find an entry that is still unassigned
# l is a list that keeps track of current position
# ie. it keeps track of incrementation of rows and cols
def find_empty_location(arr, l):
    for row in range(9):
        for col in range(9):
            if (arr[row][col] == 0):
                l[0] = row
                l[1] = col
                return True
    return False
    

# check if number is present in the row
def used_in_row(arr, row, num):
    for i in range(9):
        if (arr[row][i] == num):
            return True
    return False

# check if number is present in the column
def used_in_column(arr, col, num):
    for i in range(9):
        if (arr[i][col] == num):
            return True
    return False

# check if number is present in the given box
def used_in_box(arr, row, col, num):
    for i in range(3):
        for j in range(3):
            if (arr[row + i][col + j] == num):
                return True
    return False

# check if the number is acceptable for a particular cell
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
    list_of_numbers = [1, 2, 3, 4, 5, 6 , 7 , 8 , 9]
    random.shuffle(list_of_numbers)
    #print(list_of_numbers)
    for i in range(len(list_of_numbers)):
        arr[0][i] = list_of_numbers[i]
    return arr

'''
def assign_random_numbers(arr):
    #arr[0][0] = choose_random_number(1, 10)
    for i in range(5):
        #i = choose_random_number(0, 9)
        #j = choose_random_number(0, 9)
        num = choose_random_number(1, 10) 
        if (arr[i][0] == 0):
            arr[i][0] = num
    return arr
'''

# checks if sudoku is solvable
# fills the grid with numbers to generate a solved sudoku square
def fill_grid(arr):

    # l is the start position
    l = [0, 0]

    # if there are no empty locations, sudoku is solved
    if (not find_empty_location(arr, l)):
        return True

    # assigning row and col values
    row = l[0]
    col = l[1]

    # trying to fill out digits (1-9)
    for num in range(1, 10):
        if is_safe(arr, row, col, num):

            # assuming a number
            arr[row][col] = num

            # this is a recursive funtion
            # returns True if successfully solved
            if (fill_grid(arr)):
                return True
            
            # if fails then unmake assumption
            arr[row][col] = 0

    # trigger backtracking
    return False



# STEP 2: MAKING THE GRID A PLAYABLE SUDOKU SQUARE OF PARTICULAR COMPLEXITY -X- 



# clone created in the main function

# judges time taken to solve and analyses required complexity for next sudoku
# returns number of units to erase the value of in the solved grid
# if this is the first time then, set complexity as easy
def complexity(units_erased, solving_time):
    max_time_expected_easy = 5
    max_time_expected_medium = 15
    max_time_expected_hard = 30

    # for easy level adjustments
    if 45 <= units_erased < 55:
        # if solved in less than expected time, complexity more
        # hence units erased more
        if solving_time < max_time_expected_easy:
            units_erased += 4

        # if solved in more than expected time, complexity less
        # hence units erased less
        if solving_time > max_time_expected_easy:
            units_erased -= 3

    # for medium level adjustments
    if 55 <= units_erased < 65:
        if solving_time < max_time_expected_medium:
            units_erased += 3

        if solving_time > max_time_expected_medium:
            units_erased -= 2

    # for easy level adjustments
    if 65 <= units_erased <= 75:
        
        if solving_time < max_time_expected_hard:
            units_erased += 2

        if solving_time > max_time_expected_hard:
            units_erased -= 1

    return units_erased


# takes the grid and randomly reassigns value 0 to {units_erased} cells
'''def create_question_grid(arr, units_erased=45):
    for _ in range(units_erased):
        i = choose_random_number(0, 9)
        j = choose_random_number(0, 9)
        arr[i][j] = 0
    return arr'''

def create_question_grid(arr, units_erased=45):
    """Generate a question grid by erasing cells."""
    question = [row[:] for row in arr]
    count = 0
    while count < units_erased:
        i, j = random.randint(0, 8), random.randint(0, 8)
        if question[i][j] != 0:
            question[i][j] = 0
            count += 1
    return question



# STEP 3: MAKING IT PLAYABLE ON PYGAME



def cord(pos, diff):
    global x
    x = pos[0]//diff
    global z
    z = pos[1]//diff

# highlights the cell selected by the user
'''def highlightbox(Window, diff):
    for k in range(2):
        pygame.draw.line(Window, (0, 0, 0), (x * diff-3, (z + k)*diff), (x * diff + diff + 3, (z + k)*diff), 7)
        pygame.draw.line(Window, (0, 0, 0), ( (x + k)* diff, z * diff ), ((x + k) * diff, z * diff + diff), 7) '''

def highlight_cell(Window, x, z, diff):
    pygame.draw.rect(Window, (0, 255, 0), (x * diff, z * diff, diff, diff), 3)


def draw_grid(Window, grid, diff, font):
    """Draw the sudoku grid on the Pygame window."""
    for i in range(9):
        for j in range(9):
            if grid[j][i] != 0:
                value = font.render(str(grid[j][i]), True, (0, 0, 0))
                Window.blit(value, (i * diff + 15, j * diff + 15))
    for i in range(10):
        pygame.draw.line(Window, (0, 0, 0), (0, i * diff), (500, i * diff), 2 if i % 3 == 0 else 1)
        pygame.draw.line(Window, (0, 0, 0), (i * diff, 0), (i * diff, 500), 2 if i % 3 == 0 else 1)

# fills the value given by user into a given cell
def fillvalue(value, Window, diff, font):
    text1 = font.render(str(value), 1, (0, 0, 0))
    Window.blit(text1, (x * diff + 15, z * diff + 15))

# raises error is number outside 1-9 is entered
def raiseerror(Window, font):
    text1 = font.render("wrong!", 1, (0, 0, 0))
    Window.blit(text1, (20, 570)) 

# raises error if character entered is not a digit
def raiseerror1(Window, font):
    text1 = font.render("wrong ! enter a valid key for the game", 1, (0, 0, 0))
    Window.blit(text1, (20, 570))

# don't really need this function coz we already have the answer grid
# need to just check if all values are filled
# and once all values are filled, display "Sudoku Solved!"
def validvalue(m, k, l, value):
    for it in range(9):
        if m[k][it]== value:
            return False
        if m[it][l]== value:
            return False
    it = k//3
    jt = l//3
    for k in range(it * 3, it * 3 + 3):
        for l in range (jt * 3, jt * 3 + 3):
            if m[k][l]== value:
                return False
    return True

# Update drawlines to highlight fixed numbers
'''FIX THIS'''
'''THE HIGHLIGHTED NUMBERS DON'T CHANGE WHEN R KEY IS PRESSED'''
def drawlines(question_grid, Window, diff, font):
    for i in range(9):
        for j in range(9):
            if question_grid[i][j] != 0:  # Check if the number is fixed
                # Draw a light green background for fixed numbers
                pygame.draw.rect(Window, (144, 238, 144), (j * diff, i * diff, diff + 1, diff + 1))
                # Render the fixed number
                text1 = font.render(str(question_grid[i][j]), 1, (0, 0, 0))  # Black text
                Window.blit(text1, (j * diff + 15, i * diff + 15))
            '''elif solution_grid[i][j] != 0:  # Check if the cell is filled by the user
                # Draw a yellow background for user-entered numbers
                pygame.draw.rect(Window, (255, 255, 0), (j * diff, i * diff, diff + 1, diff + 1))
                # Render the user-entered number
                text1 = font.render(str(solution_grid[i][j]), 1, (0, 0, 0))  # Black text
                Window.blit(text1, (j * diff + 15, i * diff + 15))'''
    
    # Draw grid lines
    for l in range(10):
        thick = 7 if l % 3 == 0 else 1  # Thicker lines for 3x3 sub-grids
        pygame.draw.line(Window, (0, 0, 0), (0, l * diff), (500, l * diff), thick)  # Horizontal lines
        pygame.draw.line(Window, (0, 0, 0), (l * diff, 0), (l * diff, 500), thick)  # Vertical lines

# check if the sudoku is solved
def is_solved(user_grid, solution_grid):
    for i in range(len(user_grid)):
        for j in range(len(user_grid[i])):
            # Check if any cell mismatches or is empty
            if user_grid[i][j] != solution_grid[i][j]:
                return False
    return True

# prints the grid as a sudoku square
def printing(N, arr):
    print(tabulate(arr, tablefmt="grid"))
'''
    for i in range(N):
        for j in range(N):
            print(arr[i][j], end=" ")
        print()
'''

if __name__ == "__main__":
    main()
