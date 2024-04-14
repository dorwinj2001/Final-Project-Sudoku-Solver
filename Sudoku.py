#This is where our Sudoku code will go
from tkinter import *

root = Tk()
root.title("Sudoku Solver")
root.geometry("324x550")

label = Label(root,text="Fill in the numbers and click solve").grid(row=0,column=1,columnspan=10)

errLabel = Label(root, text="", fg="red")
errLabel.grid(row = 15, column = 1, columnspan = 10, pady=5)

successLabel = Label(root, text="", fg="green")
successLabel.grid(row = 15, column = 1, columnspan = 10, pady=5)

cell = {}

def validateNumber(P):
    out = (P.isdigit() or P == "") and len(P) < 2
    return out

reg = root.register(validateNumber)

def draw3x3Grid(row,column,bgColor):
    
    for i in range(3):
        for j in range(3):
            e = Entry(root, width = 5, bg = bgColor,justify = "center", validate="key", validatecommand = (reg, "%P"))
            e.grid(row = row + i + 1, column = column + j + 1, sticky = "nsew", padx = 1, pady = 1, ipady = 5)
            cell[(row+i+1, column+j+1)] = e

def draw9x9Grid():
    color = "#D0ffff"

    for rowNumber in range(1,10,3):
        for colNumber in range(0,9,3):
            draw3x3Grid(rowNumber,colNumber,color)
            if color == "#D0ffff":
                color = "#ffffd0"
            else:
                color = "#D0ffff"

def clearValues():
    errLabel.configure(text = "")
    successLabel.configure(text = "")

    for row in range(2,11):
        for column in range(1,10):
            cell = cell[(row,column)]
            cell.delete(0,"end")

def getValues():
    board = []

    errLabel.configure(text = "")
    successLabel.configure(text = "")

    for row in range(2,11):
        rows = []
        for column in range(1,10):
            value = cell[(row,column)].get()
            if value == "":
                rows.append(0)
            else:
                rows.append(int(value))
        board.append(rows)

btn = Button(root, command = getValues, text= "Solve", width = 10)
btn.grid(row = 20, column = 1, columnspan = 5, pady = 20)

btn = Button(root, command = clearValues, text= "Clear", width = 10)
btn.grid(row = 20, column = 5, columnspan = 5, pady = 20)


draw9x9Grid()
root.mainloop()










