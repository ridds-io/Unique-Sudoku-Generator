import time
import random



# N is the size of the 2D matrix (9*9)
N = 9

def main():

    # this generates an empty grid with shuffled first row
    sudoku = shuffle_first_row(initialize_grid(N))
    
    # fill_grid function solves and edits sudoku variable to have filled grid
    # if it returns true, create a copy of the sudoku grid
    # sudoku = answered sudoku grid
    # clone = cloned sudoku grid in which we will delete values to make question sudoku
    if fill_grid(sudoku):
        #printing(N, sudoku)
        clone = sudoku
        
    # printing the question
    print("Time to solve the sudoku!")
    print("Difficulty: easy")
    printing(N, create_question_grid(clone))




# STEP 1: GENERATING A FULLY SOLVED SUDOKU SQUARE -X-



# measures the time taken by the user to solve the sudoku
def time_tracker():
    # generate sudoku grid
    # only run time_tracker function after user starts filling in the grid
    start = time.time()
    # run the function to solve sudoku here
    end = time.time()
    time_taken = end - start
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
    l = [1, 0]

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
def create_question_grid(arr, units_erased=45):
    for _ in range(units_erased):
        i = choose_random_number(0, 9)
        j = choose_random_number(0, 9)
        arr[i][j] = 0
    return arr


# prints the grid as a sudoku square
def printing(N, arr):
    for i in range(N):
        for j in range(N):
            print(arr[i][j], end=" ")
        print()

if __name__ == "__main__":
    main()
