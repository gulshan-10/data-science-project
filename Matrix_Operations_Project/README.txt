3x3 MATRIX OPERATIONS GUI PROJECT

FOLDERS
1. without_numpy/matrix_without_numpy.py
   Uses only built-in Python lists, loops and functions. No third-party package required.
2. with_numpy/matrix_with_numpy.py
   Uses NumPy for matrix calculations.

REQUIREMENTS
- Python 3.9 or newer recommended
- Tkinter (usually included with standard Python installation)
- NumPy is required only for the NumPy version

RUN WITHOUT NUMPY
Open a terminal in the project folder:
    python without_numpy/matrix_without_numpy.py

RUN WITH NUMPY
Install NumPy:
    python -m pip install numpy
Then run:
    python with_numpy/matrix_with_numpy.py

USAGE
- Edit the 9 values in Matrix A and Matrix B.
- Addition, subtraction and multiplication use both matrices.
- Transpose, determinant and inverse use Matrix A.
- Use Load Sample Values to restore the demonstration matrices.
- Inverse is not available when determinant is zero.

SAMPLE MATRICES
A = [[1, 2, 3], [0, 1, 4], [5, 6, 0]]
B = [[2, 0, 1], [1, 3, 2], [0, 1, 1]]

This is an educational 3x3 project. Both versions use the same GUI layout
and sample values so their results can be compared fairly.
