import tkinter as tk
import numpy as np

GRID_SIZE = 5  # You can change this (e.g., 4, 6, etc.)

class LightsOutGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Modulo 2 Lights Out Solver")

        self.grid = self.generate_solvable_grid()
        self.buttons = [[None]*GRID_SIZE for _ in range(GRID_SIZE)]

        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                btn = tk.Button(master, width=4, height=2, 
                                bg="black" if self.grid[i][j] else "white",
                                command=lambda x=i, y=j: self.toggle(x, y))
                btn.grid(row=i, column=j)
                self.buttons[i][j] = btn

        self.solve_button = tk.Button(master, text="Solve", command=self.solve_with_animation)
        self.solve_button.grid(row=GRID_SIZE, column=0, columnspan=GRID_SIZE, pady=10)

    def toggle(self, i, j):
        for x, y in [(i, j), (i-1, j), (i+1, j), (i, j-1), (i, j+1)]:
            if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
                self.grid[x][y] ^= 1
                self.buttons[x][y].configure(bg="black" if self.grid[x][y] else "white")

    def solve_with_animation(self):
        A = self.build_matrix()
        b = self.grid.flatten()
        x = self.gaussian_elimination_mod2(A, b)

        if x is None:
            print("No solution")
            return

        steps = [(divmod(idx, GRID_SIZE)) for idx, val in enumerate(x) if val == 1]

        def animate_step(i):
            if i >= len(steps):
                return
            r, c = steps[i]
            self.buttons[r][c].configure(bg="red")
            self.master.after(200, lambda: finish_step(r, c, i))

        def finish_step(r, c, i):
            self.toggle(r, c)
            self.master.after(300, lambda: animate_step(i + 1))

        self.master.after(0, lambda: animate_step(0))

    def build_matrix(self):
        size = GRID_SIZE * GRID_SIZE
        A = np.zeros((size, size), dtype=int)
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                idx = i * GRID_SIZE + j
                A[idx][idx] = 1
                for x, y in [(i-1,j), (i+1,j), (i,j-1), (i,j+1)]:
                    if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
                        A[idx][x * GRID_SIZE + y] = 1
        return A

    def gaussian_elimination_mod2(self, A, b):
        A = A.copy()
        b = b.copy()
        n = len(b)

        for col in range(n):
            pivot_row = None
            for row in range(col, n):
                if A[row][col] == 1:
                    pivot_row = row
                    break
            if pivot_row is None:
                continue
            A[[col, pivot_row]] = A[[pivot_row, col]]
            b[col], b[pivot_row] = b[pivot_row], b[col]

            for row in range(n):
                if row != col and A[row][col] == 1:
                    A[row] ^= A[col]
                    b[row] ^= b[col]

        for row in range(n):
            if not A[row].any() and b[row]:
                return None

        return b

    def generate_solvable_grid(self):
        A = self.build_matrix()
        size = GRID_SIZE * GRID_SIZE
        x = np.random.randint(0, 2, size)  # Random solution
        b = A @ x % 2                      # Apply A * x mod 2
        return b.reshape((GRID_SIZE, GRID_SIZE))

if __name__ == "__main__":
    root = tk.Tk()
    game = LightsOutGame(root)
    root.mainloop()
