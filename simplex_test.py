from SimplexSolver import SimplexSolver, clear
from scipy import optimize
import time
import csv

def run_custom(A, b, c):
  start = time.process_time()
  result = SimplexSolver().run_simplex(A, b, c)
  stop = time.process_time()

  return stop - start, result

def run_scipy(A, b, c):
  start = time.process_time()
  result = optimize.linprog(c, A, b)
  stop = time.process_time()

  return stop - start, result

def print_results(title, time, result, sep = '\n\n', end = f"{'-' * 80}\n"):
  print(title, end = sep)
  print(result, end = sep)
  print('Run for:', time, end = sep if end else '\n')
  
  if end:
    print(end)

if __name__ == '__main__':
  data = [
    {
      'A': [
        [4, 1],
        [-1, 1],
      ],
      'b': [8, 3],
      'c': [3, 4]
    },
    {
      'A': [
        [1, 1],
        [2, 1],
        [0, 1],
      ],
      'b': [300, 400, 250],
      'c': [50, 100],
    },
    {
      'A': [
        [17, 27, 34],
        [12, 21, 15],
      ],
      'b': [91800, 42000],
      'c': [8, 12, 22],
    },
    {
      'A': [
        [4, 3, 6],
        [6, 16, 8],
        [4, 1, 10],
      ],
      'b': [2, 4, 3],
      'c': [30, 256, 9],
    },
    {
      'A': [
        [1, 0, 0, 0],
        [0, 2, 0, 1],
        [1, 1, 1, 0],
        [0, 0, 1, 2],
      ],
      'b': [4, 3, 2, 1],
      'c': [8, 10, 25, 15],
    }
  ]

  file = open('tests.csv', 'w')
  writer = csv.writer(file, dialect='excel-tab', delimiter = ';')
  writer.writerow(['size', 'size_restrictions' 'time_solver', 'time_scipy'])

  for item in data:
    clear()
    A = item.get('A')
    b = item.get('b')
    c = item.get('c')
    cn = [-x for x in item.get('c')]

    time1, res1 = run_custom(A, b, c)
    time2, res2 = run_scipy(A, b, cn)

    print_results('SimplexSolver results:', time1, res1)
    print_results('SciPy results:', time2, res2)

    writer.writerow([len(c), len(A), time1, time2])
    input("Press enter to continue...")
