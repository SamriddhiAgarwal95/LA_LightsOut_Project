import tkinter as tk
import numpy as np

SIZE = 5  # 3x3 grid

class LightsOut:
    def __init__(self, master):
        self.master = master
        self.buttons = [[None]*SIZE for _ in range(SIZE)]
        self.states = [[0]*SIZE for _ in range(SIZE)]  # 0 = off, 1 = on

        for i in range(SIZE):
            for j in range(SIZE):
                btn = tk.Button(master, width=6, height=3,
                                bg="black", command=lambda x=i, y=j: self.toggle(x, y))
                btn.grid(row=i, column=j)
                self.buttons[i][j] = btn

        solve_btn = tk.Button(master, text="Solve", command=self.solve)
        solve_btn.grid(row=SIZE, column=0, columnspan=SIZE, sticky="we")

        self.randomize()

    def toggle(self, i, j):
        for x, y in [(i, j), (i-1, j), (i+1, j), (i, j-1), (i, j+1)]:
            if 0 <= x < SIZE and 0 <= y < SIZE:
                self.states[x][y] ^= 1
                self.update_button(x, y)
        if all(self.states[i][j] == 0 for i in range(SIZE) for j in range(SIZE)):
            print("🎉 You win!")

    def update_button(self, i, j):
        color = "yellow" if self.states[i][j] else "black"
        self.buttons[i][j].config(bg=color)

    def randomize(self):
        import random
        for i in range(SIZE):
            for j in range(SIZE):
                if random.choice([True, False]):
                    self.toggle(i, j)

    def index(self, i, j):
        return i * SIZE + j

    def build_toggle_matrix(self):
        n = SIZE * SIZE
        A = np.zeros((n, n), dtype=int)

        for i in range(SIZE):
            for j in range(SIZE):
                idx = self.index(i, j)
                A[idx, idx] = 1
                for x, y in [(i-1,j),(i+1,j),(i,j-1),(i,j+1)]:
                    if 0 <= x < SIZE and 0 <= y < SIZE:
                        A[idx, self.index(x, y)] = 1
        return A

    def solve(self):
        n = SIZE * SIZE
        A = self.build_toggle_matrix()
        b = np.array([self.states[i][j] for i in range(SIZE) for j in range(SIZE)])

        # Solve A·x = b (mod 2)
        x = self.solve_mod2(A, b)
        if x is None:
            print("No solution.")
        else:
            print("Solution: press these cells:")
            for i in range(n):
                if x[i] == 1:
                    row, col = divmod(i, SIZE)
                    print(f"({row}, {col})")

    def solve_mod2(self, A, b):
        """Solves Ax = b mod 2 using Gaussian elimination."""
        A = A.copy()
        b = b.copy()
        n = len(b)

        for col in range(n):
            pivot_row = None
            for row in range(col, n):
                if A[row, col] == 1:
                    pivot_row = row
                    break
            if pivot_row is None:
                continue  # no pivot in this column

            # Swap rows
            A[[col, pivot_row]] = A[[pivot_row, col]]
            b[col], b[pivot_row] = b[pivot_row], b[col]

            # Eliminate below and above
            for row in range(n):
                if row != col and A[row, col] == 1:
                    A[row] = (A[row] + A[col]) % 2
                    b[row] = (b[row] + b[col]) % 2

        # Check for inconsistency
        for row in range(n):
            if not A[row].any() and b[row] != 0:
                return None  # No solution

        return b  # b now holds the solution vector

# Run GUI
root = tk.Tk()
root.title("Lights Out Solver")
game = LightsOut(root)
root.mainloop()