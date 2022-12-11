# Future Work:
# Full matrix gen
# Crisscross matrix gen


from PIL import Image, ImageDraw
from time import process_time
import numpy as np
import sympy as sp
import scipy as sc
import pandas as pd


def genCircle(n, decimals, isfilled):
    # Grids less than 3 x 3 are meaningless
    # x o x
    # o x o
    # x o x

    fileName = "test.png"

    if isfilled:
        fillcolor = 'white'
    else:
        fillcolor = 'black'

    drawing = Image.new(mode = 'RGB', size = (n, n), color = (0,0,0))
    draw = ImageDraw.Draw(drawing)
    # Outline is ontop of fill not another layer around it
    draw.ellipse((0, 0, n - 1, n - 1), fill = fillcolor, outline ='white')
    drawing.save(fileName)

    im = Image.open(fileName)
    # Each array represents the RGB values for each column
    A = np.array(im)

    # Take the first column from each array and combine them into one array that's n x n
    # (Can take first column or any column since R,G, & B will all be the same values for black and white))
    A = (A[:,:,0])
    print(A)

    # Random mask of values from 0 to 1
    mask = np.random.rand(n, n).round(decimals)
    # Multiply individual values by mask
    A = A * mask
    print(A)
    
    #A = A / 255
    b = np.random.rand(n, 1).round(decimals)

    return A, b

def solverNumpy(A, b):

    try:
        st = process_time()
        x = np.linalg.solve(A,b)
        et = process_time()
        time = et - st
        unique = True
    except:
        unique = False
        time = 0
        pass

    return unique, time

def solverScipy(A, b):
    try:
        st = process_time()
        x = sc.linalg.solve(A,b)
        et = process_time()
        time = et - st
        unique = True
    except:
        unique = False
        time = 0
        pass

    return unique, time

def rrefSympy(A, b):
    A = np.append(A, b, axis = 1)
    A = sp.Matrix(A)
    st = process_time()
    A = A.rref()
    et = process_time()
    time = et - st

    return A, time

def rrefMine(A, b):
    
    n = b.size
    x = np.zeros(n)

    # Eliminate Down

    for i in range(n - 1):
        for j in range(i + 1, n):
            scalar = A[j, i] / A[i, i]
            for k in range(i, n):
                A[j, k] = A[j, k] - scalar * A[i, k]
            b[j] = b[j] - scalar * b[i]

    # Eliminate Up

    x[n - 1] = b[n - 1] / A[n - 1, n - 1]
    for j in range(n - 2, -1, -1):
        entry = b[j]
        for k in range(j + 1, n):
            entry = entry - A[j, k] * x[k]
        x[j] = entry / A[j, j]
    
    return x


# Limit of 2 decimal places when printing
np.set_printoptions(formatter={'float': lambda x: "{0:3.2f}".format(x)})
#sp.init_printing(use_unicode=True)

cols = ['n x n', 'Decimals', 'Filled Shape', 'Solutions', 'Time - RREF', 'Time - Numpy', 'Time - Sympy']
df = pd.DataFrame(columns = cols)

for k in range(3, 24):
    n = k
    for l in range(5):
        decimals = l
        for m in [True, False]:
            isfilled = m
            for o in range(20):
                A, b = genCircle(n, decimals, isfilled)
                unique1, time1 = solverNumpy(A, b)
                unique2, time2 = solverScipy(A, b)
                S, time3 = rrefSympy(A, b)

                if unique1:
                    solution = 'Unique'
                else:
                    # [0] takes only the matrix not the pivot row
                    # the rest converts it from Sympy matrix to Numpy matrix
                    S = np.array(S[0]).astype(np.float64)
                    print(S)

                    # find non-zero entries in last column
                    # if that row is not all zeros, then there is no solution
                    # else there are infinite solutions
                    noSolution = False
                    for i in range(n):
                        # i goes to nth row
                        # n goes to (n + 1)th column
                        if S[i, n] != 0:
                            # j goes to the nth column
                            if all(S[i, j] == 0 for j in range(n)):
                                noSolution = True

                    if noSolution:
                        solution = 'No Solution'
                    else:
                        solution = 'Infinite Solutions'

                print('Solution:', solution)
                data = [n, decimals, isfilled, solution, time3, time1, time2]    
                df0 = pd.DataFrame([data], columns = cols)
                df = pd.concat([df, df0], ignore_index = True)

df.to_excel("Output.xlsx", sheet_name = 'Results', index = False)
