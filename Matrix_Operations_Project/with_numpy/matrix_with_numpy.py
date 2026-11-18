"""
3x3 Matrix Operations GUI - WITH NumPy
Install once: python -m pip install numpy
Run: python matrix_with_numpy.py
"""
import tkinter as tk
from tkinter import messagebox
import numpy as np

SIZE = 3

class MatrixApp:
    def __init__(self, root):
        self.root = root
        root.title("3x3 Matrix Calculator - With NumPy")
        root.geometry("760x650")
        root.configure(bg="#eef3f8")
        tk.Label(root, text="3×3 MATRIX CALCULATOR", font=("Arial", 20, "bold"),
                 bg="#17324d", fg="white", pady=14).pack(fill="x")
        panel = tk.Frame(root, bg="#eef3f8", padx=18, pady=12)
        panel.pack()
        self.entries = []
        samples = ( [[1,2,3],[0,1,4],[5,6,0]], [[2,0,1],[1,3,2],[0,1,1]] )
        for index, matrix_name in enumerate(("Matrix A", "Matrix B")):
            frame = tk.LabelFrame(panel, text=matrix_name, font=("Arial", 11, "bold"),
                                  bg="#eef3f8", padx=10, pady=8)
            frame.pack(side="left", padx=12)
            grid = []
            for r in range(SIZE):
                row = []
                for c in range(SIZE):
                    entry = tk.Entry(frame, width=7, justify="center", font=("Arial", 12))
                    entry.grid(row=r, column=c, padx=4, pady=4)
                    entry.insert(0, str(samples[index][r][c]))
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
            values = [[float(self.entries[number][r][c].get()) for c in range(SIZE)]
                      for r in range(SIZE)]
            return np.array(values, dtype=float)
        except ValueError:
            raise ValueError("Please enter a valid number in every matrix cell.")

    def show(self, message):
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, message)

    def format_matrix(self, M):
        # Convert NumPy values to readable text: integers stay integers.
        # Square brackets make the output look like a matrix.
        rows = []
        for row in M:
            values = []
            for x in row:
                value = float(x)
                if value.is_integer():
                    values.append(str(int(value)))
                else:
                    values.append(f"{value:.3f}".rstrip("0").rstrip("."))
            rows.append("[ " + "  ".join(values) + " ]")
        return "[\n " + "\n ".join(rows) + "\n]"

    def calculate(self, operation):
        try:
            A, B = self.read_matrix(0), self.read_matrix(1)
            self.show(self.format_matrix(operation(A, B)))
        except (ValueError, np.linalg.LinAlgError) as error:
            messagebox.showerror("Input / Calculation Error", str(error))

    # NumPy performs the matrix calculation in one function call.
    def run_add(self): self.calculate(np.add)
    def run_sub(self): self.calculate(np.subtract)
    def run_mul(self): self.calculate(np.matmul)
    def run_transpose(self):
        try: self.show(self.format_matrix(self.read_matrix(0).T))
        except ValueError as e: messagebox.showerror("Input Error", str(e))
    def run_det(self):
        try: self.show(f"Determinant of A = {np.linalg.det(self.read_matrix(0)):.3f}")
        except ValueError as e: messagebox.showerror("Input Error", str(e))
    def run_inverse(self):
        try: self.show(self.format_matrix(np.linalg.inv(self.read_matrix(0))))
        except (ValueError, np.linalg.LinAlgError) as e:
            messagebox.showerror("Calculation Error", str(e))

    def load_sample(self):
        samples = ( [[1,2,3],[0,1,4],[5,6,0]], [[2,0,1],[1,3,2],[0,1,1]] )
        for n in range(2):
            for r in range(SIZE):
                for c in range(SIZE):
                    self.entries[n][r][c].delete(0, tk.END)
                    self.entries[n][r][c].insert(0, str(samples[n][r][c]))

if __name__ == "__main__":
    root = tk.Tk()
    MatrixApp(root)
    root.mainloop()
