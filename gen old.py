# Issues:
# rrefMine has divide by zero issue
# rrefNumpy has singular issue, needs exception handling
# rrefScipy has singular issue, needs exception handling
# rrefSympy needs to output the vector, not the rref form
# To do:
# Make 
# Create solver functions for RREF, etc.
# Impliment time recordings
# Impliment exporting of time recordings



from PIL import Image, ImageDraw
import numpy as np
# Don't show the decimal places when printing
np.set_printoptions(formatter={'float': lambda x: "{0:3.0f}".format(x)})
import sympy as sp
sp.init_printing(use_unicode=True)
import scipy as sc

# Grids less than 3 x 3 are meaningless
# x o x
# o x o
# x o x

def gen(n, isfilled):
    if isfilled:
        fillcolor = 'white'
    else:
        fillcolor = 'black'

    fileName = "test.png"
    

    drawing = Image.new(mode = 'RGB', size = (n, n), color = (0,0,0))
    draw = ImageDraw.Draw(drawing)
    # outline is ontop of fill not another layer around it
    draw.ellipse((0, 0, n - 1, n - 1), fill = fillcolor, outline ='white')
    #draw.point((0, 0), 'red')
    drawing.save(fileName)

    im = Image.open(fileName)
    # Each array represents the RGB values for each column
    A = np.array(im)
    # Take the first column from each array and combine them into one array that's n x n
    # (Can take first column or any column since R,G, & B will all be the same values for black and white))
    A = (A[:,:,0])
    print(A)
    # Random Mask of values from 0 to 1
    B = np.random.rand(n, n)
    # Multiply individual values by mask
    A = A * B
    print(A)
    
    #A = A / 255
    b = np.random.rand(n, 1)
    return A, b

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

def rrefNumpy(A, b):
    x = np.linalg.solve(A,b)
    return x

def rrefScipy(A, b):
    x = sc.linalg.solve(A,b)
    return x

def rrefSympy(A, b):
    A = np.append(A, b, axis = 1)
    A = sp.Matrix(A)
    A = A.rref()
    #return x


A, b = gen(3, False)
#rrefMine(A, b)
#rrefNumpy(A, b)
#rrefScipy(A, b)
#rrefSympy(A, b)