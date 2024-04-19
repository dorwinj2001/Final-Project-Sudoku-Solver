from tkinter import *
import sys
import threading

sys.setrecursionlimit(2000)

root = Tk()
root.title("Sudoku Solver")
root.geometry("324x550")

label = Label(root, text="Fill in the numbers and click solve").grid(row=0, column=1, columnspan=10)

errLabel = Label(root, text="", fg="red")
errLabel.grid(row=15, column=1, columnspan=10, pady=5)

successLabel = Label(root, text="", fg="green")
successLabel.grid(row=15, column=1, columnspan=10, pady=5)

cell = {}

def validateNumber(P):
    out = (P.isdigit() or P == "") and len(P) < 2
    return out

reg = root.register(validateNumber)

def draw3x3Grid(row, column, bgColor):
    for i in range(3):
        for j in range(3):
            e = Entry(root, width=5, bg=bgColor, justify="center", validate="key", validatecommand=(reg, "%P"))
            e.grid(row=row + i + 1, column=column + j + 1, sticky="nsew", padx=1, pady=1, ipady=5)
            cell[(row + i + 1, column + j + 1)] = e

def draw9x9Grid():
    color = "#D0ffff"
    for rowNumber in range(1, 10, 3):
        for colNumber in range(0, 9, 3):
            draw3x3Grid(rowNumber, colNumber, color)
            color = "#ffffd0" if color == "#D0ffff" else "#D0ffff"

def clearValues():
    errLabel.configure(text="")
    successLabel.configure(text="")
    for row in range(2, 11):
        for column in range(1, 10):
            cell[(row, column)].delete(0, "end")

def getAndSolve():
    errLabel.config(text="")
    successLabel.config(text="Solving... Please wait.")
    root.update()  # Force the UI to update the label before solving

    board = [[int(cell[(row, col)].get() or 0) for col in range(1, 10)] for row in range(2, 11)]

    if solve_sudoku(board):
        for row in range(2, 11):
            for col in range(1, 10):
                cell[(row, col)].delete(0, "end")
                cell[(row, col)].insert(0, str(board[row-2][col-1]))
        successLabel.config(text="Solved!")
    else:
        successLabel.config(text="No solution found.")
        errLabel.config(text="No solution exists.")

def is_valid(board, row, col, num):
    block_row, block_col = (row // 3) * 3, (col // 3) * 3
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
        if board[block_row + (i // 3)][block_col + (i % 3)] == num:
            return False
    return True

def solve_sudoku(board):
    empty = find_empty_location(board)
    if not empty:
        return True  # Puzzle solved
    row, col = empty

    possible_numbers = [num for num in range(1, 10) if is_valid(board, row, col, num)]
    if not possible_numbers:
        return False  # Dead end reached, no valid numbers to place

    for num in possible_numbers:
        board[row][col] = num
        if solve_sudoku(board):
            return True
        board[row][col] = 0  # Backtrack
    
    return False  # No valid moves found, trigger backtracking


def find_empty_location(board):
    min_count = 10  # More than the maximum possibilities (1-9)
    best_spot = None
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                count = len({num for num in range(1, 10) if is_valid(board, row, col, num)})
                if count < min_count:
                    min_count, best_spot = count, (row, col)
                    if count == 1:
                        return best_spot  # Return immediately if only one possibility
    return best_spot

def load_puzzle(puzzle):
    clearValues()
    for i in range(9):
        for j in range(9):
            cell_value = puzzle[i][j]
            cell[(i+2, j+1)].delete(0, END)
            if cell_value != 0:
                cell[(i+2, j+1)].insert(0, cell_value)

def threaded_solve(): # Speeds up hard puzzles that have to backtrack a lot
    board = [[int(cell[(row, col)].get() or 0) for col in range(1, 10)] for row in range(2, 11)]
    successLabel.config(text="Solving... Please wait.")
    root.update_idletasks()

    if solve_sudoku(board):
        for row in range(2, 11):
            for col in range(1, 10):
                cell[(row, col)].delete(0, END)
                cell[(row, col)].insert(0, str(board[row-2][col-1]))
        successLabel.config(text="Solved!")
    else:
        errLabel.config(text="No solution exists")
        successLabel.config(text="No solution found")

def start_thread():
    solve_thread = threading.Thread(target=threaded_solve)
    solve_thread.start()
    
puzzles = {
    "Very Easy": [
        [9, 0, 0, 1, 0, 0, 0, 0, 5],
        [0, 0, 5, 0, 9, 0, 2, 0, 1],
        [8, 0, 0, 0, 4, 0, 0, 0, 0],
        [0, 0, 0, 0, 8, 0, 0, 0, 0],
        [0, 0, 0, 7, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 2, 6, 0, 0, 9],
        [2, 0, 0, 3, 0, 0, 0, 0, 6],
        [0, 0, 0, 2, 0, 0, 9, 0, 0],
        [0, 0, 1, 9, 0, 4, 5, 7, 0]
    ],
    
    "Easy": [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ],
    "Medium": [
        [0, 2, 0, 6, 0, 8, 0, 0, 0],
        [5, 8, 0, 0, 0, 9, 7, 0, 0],
        [0, 0, 0, 0, 4, 0, 0, 0, 0],
        [3, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 6, 0, 0, 0, 0, 0, 0, 5],
        [0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 3, 2, 0, 0, 0, 8, 0],
        [0, 0, 0, 4, 0, 3, 0, 5, 0]
    ],

    "Hard": [
        [8, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 3, 6, 0, 0, 0, 0, 0],
        [0, 7, 0, 0, 9, 0, 2, 0, 0],
        [0, 5, 0, 0, 0, 7, 0, 0, 0],
        [0, 0, 0, 0, 4, 5, 7, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 3, 0],
        [0, 0, 1, 0, 0, 0, 0, 6, 8],
        [0, 0, 8, 5, 0, 0, 0, 1, 0],
        [0, 9, 0, 0, 0, 0, 4, 0, 0]
    ],

    "Really Hard": [
        
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 3, 0, 8, 5],
        [0, 0, 1, 0, 2, 0, 0, 0, 0],
        [0, 0, 0, 5, 0, 7, 0, 0, 0],
        [0, 0, 4, 0, 0, 0, 1, 0, 0],
        [0, 9, 0, 0, 0, 0, 0, 0, 0],
        [5, 0, 0, 0, 0, 0, 0, 7, 3],
        [0, 0, 2, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 4, 0, 0, 0, 9]
    ]
}

puzzle_var = StringVar(root)
puzzle_var.set("Select a puzzle")

puzzle_menu = OptionMenu(root, puzzle_var, *puzzles.keys())
puzzle_menu.grid(row=1, column=0, columnspan=50, pady=20)

load_button = Button(root, text="Load Puzzle", command=lambda: load_puzzle(puzzles[puzzle_var.get()]))
load_button.grid(row=1, column=7, columnspan=20, pady=20)

draw9x9Grid()

btn_solve = Button(root, command=getAndSolve, text="Solve", width=10)
btn_solve.grid(row=20, column=1, columnspan=5, pady=20)

btn_clear = Button(root, command=clearValues, text="Clear", width=10)
btn_clear.grid(row=20, column=5, columnspan=5, pady=20)

btn_solve.config(command=start_thread)

root.mainloop()