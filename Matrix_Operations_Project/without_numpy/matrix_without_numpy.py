"""
3x3 Matrix Operations GUI - WITHOUT NumPy
Run: python matrix_without_numpy.py
Only uses Python lists, loops, and functions.
"""
import tkinter as tk
from tkinter import messagebox

SIZE = 3

def add(A, B):
    # Add matching elements from both matrices.
    return [[A[i][j] + B[i][j] for j in range(SIZE)] for i in range(SIZE)]

def subtract(A, B):
    # Subtract matching elements from both matrices.
    return [[A[i][j] - B[i][j] for j in range(SIZE)] for i in range(SIZE)]

def multiply(A, B):
    # Each result cell is a row-column dot product.
    C = [[0 for _ in range(SIZE)] for _ in range(SIZE)]
    for i in range(SIZE):
        for j in range(SIZE):
            for k in range(SIZE):
                C[i][j] += A[i][k] * B[k][j]
    return C

def transpose(A):
    # Change rows into columns.
    return [[A[j][i] for j in range(SIZE)] for i in range(SIZE)]

def determinant(A):
    # Standard 3x3 determinant formula.
    a, b, c = A[0]
    d, e, f = A[1]
    g, h, i = A[2]
    return a * (e*i - f*h) - b * (d*i - f*g) + c * (d*h - e*g)

def inverse(A):
    # Inverse = adjugate / determinant.
    det = determinant(A)
    if abs(det) < 1e-10:
        raise ValueError("Inverse does not exist (determinant is zero).")

    cof = [
        [ A[1][1]*A[2][2] - A[1][2]*A[2][1],
         -(A[1][0]*A[2][2] - A[1][2]*A[2][0]),
          A[1][0]*A[2][1] - A[1][1]*A[2][0]],
        [-(A[0][1]*A[2][2] - A[0][2]*A[2][1]),
          A[0][0]*A[2][2] - A[0][2]*A[2][0],
         -(A[0][0]*A[2][1] - A[0][1]*A[2][0])],
        [ A[0][1]*A[1][2] - A[0][2]*A[1][1],
         -(A[0][0]*A[1][2] - A[0][2]*A[1][0]),
          A[0][0]*A[1][1] - A[0][1]*A[1][0]]
    ]
    adj = transpose(cof)
    return [[adj[r][c] / det for c in range(SIZE)] for r in range(SIZE)]

class MatrixApp:
    def __init__(self, root):
        self.root = root
        root.title("3x3 Matrix Calculator - Without NumPy")
        root.geometry("760x650")
        root.configure(bg="#eef3f8")
        tk.Label(root, text="3×3 MATRIX CALCULATOR", font=("Arial", 20, "bold"),
                 bg="#17324d", fg="white", pady=14).pack(fill="x")
        panel = tk.Frame(root, bg="#eef3f8", padx=18, pady=12)
        panel.pack()
        self.entries = []
        for matrix_name in ("Matrix A", "Matrix B"):
            frame = tk.LabelFrame(panel, text=matrix_name, font=("Arial", 11, "bold"),
                                  bg="#eef3f8", padx=10, pady=8)
            frame.pack(side="left", padx=12)
            grid = []
            for r in range(SIZE):
                row = []
                for c in range(SIZE):
                    entry = tk.Entry(frame, width=7, justify="center", font=("Arial", 12))
                    entry.grid(row=r, column=c, padx=4, pady=4)
                    entry.insert(0, str([[1,2,3],[0,1,4],[5,6,0]][r][c] if matrix_name=="Matrix A"
                                        else [[2,0,1],[1,3,2],[0,1,1]][r][c]))
                    row.append(entry)
                grid.append(row)
            self.entries.append(grid)

        buttons = tk.Frame(root, bg="#eef3f8", pady=8)
        buttons.pack()
        actions = [
            ("Addition", self.run_add), ("Subtraction", self.run_sub),
            ("Multiplication", self.run_mul), ("Transpose A", self.run_transpose),
            ("Determinant A", self.run_det), ("Inverse A", self.run_inverse)
        ]
        for index, (label, command) in enumerate(actions):
            tk.Button(buttons, text=label, command=command, width=17, bg="#2878a8",
                      fg="white", font=("Arial", 10, "bold"), relief="flat").grid(
                          row=index//3, column=index%3, padx=5, pady=5)
        tk.Button(root, text="Load Sample Values", command=self.load_sample,
                  bg="#526779", fg="white").pack(pady=4)
        self.output = tk.Text(root, height=11, width=75, font=("Consolas", 11),
                              bg="#ffffff", fg="#17324d")
        self.output.pack(padx=18, pady=10)
        self.show("Enter values and select an operation. A and B are used for +, − and ×.")

    def read_matrix(self, number):
        try:
            return [[float(self.entries[number][r][c].get()) for c in range(SIZE)]
                    for r in range(SIZE)]
        except ValueError:
            raise ValueError("Please enter a valid number in every matrix cell.")

    def show(self, message):
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, message)

    def format_matrix(self, M):
        # Show whole numbers as integers; keep up to 3 decimals when needed.
        # Square brackets make the output look like a matrix.
        rows = []
        for row in M:
            values = []
            for x in row:
                if float(x).is_integer():
                    values.append(str(int(x)))
                else:
                    values.append(f"{x:.3f}".rstrip("0").rstrip("."))
            rows.append("[ " + "  ".join(values) + " ]")
        return "[\n " + "\n ".join(rows) + "\n]"

    def calculate(self, operation):
        try:
            A = self.read_matrix(0)
            B = self.read_matrix(1)
            result = operation(A, B)
            self.show(self.format_matrix(result))
        except (ValueError, ZeroDivisionError) as error:
            messagebox.showerror("Input / Calculation Error", str(error))

    def run_add(self): self.calculate(add)
    def run_sub(self): self.calculate(subtract)
    def run_mul(self): self.calculate(multiply)
    def run_transpose(self):
        try: self.show(self.format_matrix(transpose(self.read_matrix(0))))
        except ValueError as e: messagebox.showerror("Input Error", str(e))
    def run_det(self):
        try: self.show(f"Determinant of A = {determinant(self.read_matrix(0)):.3f}")
        except ValueError as e: messagebox.showerror("Input Error", str(e))
    def run_inverse(self):
        try: self.show(self.format_matrix(inverse(self.read_matrix(0))))
        except ValueError as e: messagebox.showerror("Calculation Error", str(e))

    def load_sample(self):
        samples = [
            [[1,2,3],[0,1,4],[5,6,0]],
            [[2,0,1],[1,3,2],[0,1,1]]
        ]
        for n in range(2):
            for r in range(SIZE):
                for c in range(SIZE):
                    self.entries[n][r][c].delete(0, tk.END)
                    self.entries[n][r][c].insert(0, str(samples[n][r][c]))

if __name__ == "__main__":
    root = tk.Tk()
    MatrixApp(root)
    root.mainloop()
