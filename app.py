from SimplexSolver import SimplexSolver

if __name__ == '__main__':
  A = [
    [4, 1],
    [-1, 1],
  ]

  b = [8, 3]
  c = [3, 4]

  solver = SimplexSolver()
  solver.run_simplex(A, b, c, enable_msg = True)
