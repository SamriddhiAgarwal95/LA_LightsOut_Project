import tkinter as tk
import numpy as np
import random

SIZE = 3
MODULUS = 3
COLORS = ["red", "green", "blue"]  # 0, 1, 2

class LightsOutMod3:
    def __init__(self, master):
        self.master = master
        self.buttons = [[None] * SIZE for _ in range(SIZE)]
        self.states = [[0] * SIZE for _ in range(SIZE)]  # 0 = red, 1 = green, 2 = blue

        for i in range(SIZE):
            for j in range(SIZE):
                btn = tk.Button(master, width=6, height=3,
                                bg=COLORS[0],
                                command=lambda x=i, y=j: self.toggle(x, y))
                btn.grid(row=i, column=j)
                self.buttons[i][j] = btn

        solve_btn = tk.Button(master, text="Solve", command=self.solve)
        solve_btn.grid(row=SIZE, column=0, columnspan=SIZE, sticky="we")

        self.randomize()

    def update_button(self, i, j):
        self.buttons[i][j].config(bg=COLORS[self.states[i][j]])

    def toggle(self, i, j):
        for x, y in [(i, j), (i-1, j), (i+1, j), (i, j-1), (i, j+1)]:
            if 0 <= x < SIZE and 0 <= y < SIZE:
                self.states[x][y] = (self.states[x][y] + 1) % MODULUS
                self.update_button(x, y)
        if self.is_solved():
            print("🎉 You win!")

    def is_solved(self):
        target = self.states[0][0]
        return all(self.states[i][j] == target for i in range(SIZE) for j in range(SIZE))

    def randomize(self):
        for i in range(SIZE):
            for j in range(SIZE):
                self.states[i][j] = random.randint(0, MODULUS - 1)
                self.update_button(i, j)

    def index(self, i, j):
        return i * SIZE + j

    def build_toggle_matrix(self):
        n = SIZE * SIZE
        A = np.zeros((n, n), dtype=int)
        for i in range(SIZE):
            for j in range(SIZE):
                idx = self.index(i, j)
                A[idx, idx] = 1
                for x, y in [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]:
                    if 0 <= x < SIZE and 0 <= y < SIZE:
                        A[idx, self.index(x, y)] = 1
        return A % MODULUS

    def solve(self):
        n = SIZE * SIZE
        A = self.build_toggle_matrix()
        b = np.array([self.states[i][j] for i in range(SIZE) for j in range(SIZE)])

        # Try solving to reach color 0 (red), but could adapt for any target
        target_color = 0
        b = (b - target_color) % MODULUS

        x = self.solve_mod3(A, b)
        if x is None:
            print("No solution.")
        else:
            print("Auto-solving:")
            for idx in range(n):
                count = x[idx]
                if count > 0:
                    i, j = divmod(idx, SIZE)
                    print(f"Toggle ({i}, {j}) {count} time(s)")
                    for _ in range(count):
                        self.toggle(i, j)

    def solve_mod3(self, A, b):
        """Gaussian elimination mod 3"""
        A = A.copy()
        b = b.copy()
        n = len(b)

        for col in range(n):
            pivot = None
            for row in range(col, n):
                if A[row, col] % MODULUS != 0:
                    pivot = row
                    break
            if pivot is None:
                continue

            A[[col, pivot]] = A[[pivot, col]]
            b[col], b[pivot] = b[pivot], b[col]

            inv = pow(int(A[col, col]), -1, MODULUS)
            A[col] = (A[col] * inv) % MODULUS
            b[col] = (b[col] * inv) % MODULUS

            for row in range(n):
                if row != col and A[row, col] % MODULUS != 0:
                    factor = A[row, col]
                    A[row] = (A[row] - factor * A[col]) % MODULUS
                    b[row] = (b[row] - factor * b[col]) % MODULUS

        # Check for inconsistency
        for row in range(n):
            if not A[row].any() and b[row] != 0:
                print("No solution exists for the given configuration.")
                return None

        return b % MODULUS

# Run the game
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Lights Out Modulo 3 (Red, Green, Blue)")
    game = LightsOutMod3(root)
    root.mainloop()
