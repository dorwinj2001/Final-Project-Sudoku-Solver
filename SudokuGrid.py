from tkinter import *

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
    board = []
    for row in range(2, 11):
        rows = []
        for column in range(1, 10):
            value = cell[(row, column)].get()
            rows.append(int(value) if value else 0)
        board.append(rows)
    if solve_sudoku(board):
        for row in range(2, 11):
            for column in range(1, 10):
                cell[(row, column)].delete(0, "end")
                cell[(row, column)].insert(0, board[row-2][column-1])
        successLabel.config(text="Solved!")
    else:
        errLabel.config(text="No solution exists")

def is_valid(board, row, col, num):
    if num in board[row]:
        return False
    if num in [board[i][col] for i in range(9)]:
        return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def solve_sudoku(board):
    empty = find_empty_location(board)
    if not empty:
        return True
    row, col = empty
    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num
            if solve_sudoku(board):
                return True
            board[row][col] = 0
    return False

def find_empty_location(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None

btn_solve = Button(root, command=getAndSolve, text="Solve", width=10)
btn_solve.grid(row=20, column=1, columnspan=5, pady=20)

btn_clear = Button(root, command=clearValues, text="Clear", width=10)
btn_clear.grid(row=20, column=5, columnspan=5, pady=20)

draw9x9Grid()
root.mainloop()
