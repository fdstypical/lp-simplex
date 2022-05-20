import copy
from .helpers import clear

class SimplexSolver:
  def __init__(self):
    self.A = []
    self.b = []
    self.c = []
    self.tableau = []
    self.entering = []
    self.departing = []

  def run_simplex(self, A, b, c, enable_msg = False):
    ''' Run simplex algorithm. '''
    # Add slack & artificial variables
    self.set_simplex_input(A, b, c)

    # Are there any negative elements on the bottom (disregarding
    # right-most element...)
    while not self.should_terminate():
      # ... if so, continue.
      if enable_msg:
        clear()
        self._print_tableau()
        print(("Current solution: %s\n" % str(self.get_current_solution())))
        self._prompt()

      # Attempt to find a non-negative pivot.
      pivot = self.find_pivot()

      if pivot[1] < 0:
        if (enable_msg):
          print("There exists no non-negative pivot. ", "Thus, the solution is infeasible.")
        return None
      else:
        if enable_msg:
          clear()
          self._print_tableau()
          print(("\nThere are negative elements in the bottom row, "
                "so the current solution is not optimal. "
                  "Thus, pivot to improve the current solution. The "
                  "entering variable is %s and the departing "
                  "variable is %s.\n" %
                  (str(self.entering[pivot[0]]),
                  str(self.departing[pivot[1]]))))
          self._prompt()
          print("\nPerform elementary row operations until the "
                "pivot is one and all other elements in the "
                "entering column are zero.\n")

        # Do row operations to make every other element in column zero.
        self.pivot(pivot)

    solution = self.get_current_solution()

    if enable_msg:
      clear()
      self._print_tableau()
      print(("Current solution: %s\n" % str(solution)))
      print("That's all folks!")

    return solution

  def set_simplex_input(self, A, b, c):
    ''' Set initial variables and create tableau. '''
    # Convert all entries to fractions for readability.
    for a in A:
      self.A.append([x for x in a])

    self.b = [x for x in b]
    self.c = [x for x in c]

    self.update_enter_depart(self.get_Ab())

    self.create_tableau()
    self.update_enter_depart(self.tableau)

  def update_enter_depart(self, matrix):
    self.entering = []
    self.departing = []

    # Create tables for entering and departing variables
    for i in range(0, len(matrix[0])):
      if i < len(self.A[0]):
        prefix = 'x'
        self.entering.append("%s_%s" % (prefix, str(i + 1)))
      elif i < len(matrix[0]) - 1:
        self.entering.append("s_%s" % str(i + 1 - len(self.A[0])))
        self.departing.append("s_%s" % str(i + 1 - len(self.A[0])))
      else:
        self.entering.append("b")

  def add_slack_variables(self):
    ''' Add slack & artificial variables to matrix A to transform all inequalities to equalities. '''
    slack_vars = self._generate_identity(len(self.tableau))

    for i in range(0, len(slack_vars)):
      self.tableau[i] += slack_vars[i]
      self.tableau[i] += [self.b[i]]

  def create_tableau(self):
    ''' Create initial tableau table.'''
    self.tableau = copy.deepcopy(self.A)
    self.add_slack_variables()
    c = copy.deepcopy(self.c)

    for index, value in enumerate(c):
      c[index] = -value

    self.tableau.append(c + [0] * (len(self.b)+1))

  def find_pivot(self):
    ''' Find pivot index.'''
    enter_index = self.get_entering_var()
    depart_index = self.get_departing_var(enter_index)
    return [enter_index, depart_index]

  def pivot(self, pivot_index):
    ''' Perform operations on pivot. '''
    j, i = pivot_index
    pivot = self.tableau[i][j]
    self.tableau[i] = [element / pivot for element in self.tableau[i]]

    for index, row in enumerate(self.tableau):
      if index != i:
        row_scale = [y * self.tableau[index][j] for y in self.tableau[i]]
        self.tableau[index] = [x - y for x, y in zip(self.tableau[index], row_scale)]

    self.departing[i] = self.entering[j]

  def get_entering_var(self):
    ''' Get entering variable by determining the 'most negative' element of the bottom row. '''
    bottom_row = self.tableau[len(self.tableau) - 1]
    most_neg_ind = 0
    most_neg = bottom_row[most_neg_ind]

    for index, value in enumerate(bottom_row):
      if value < most_neg:
        most_neg = value
        most_neg_ind = index

    return most_neg_ind

  def get_departing_var(self, entering_index):
    ''' To calculate the departing variable, get the minimum of the ratio of b (b_i) to the corresponding value in the entering collumn. '''
    skip = 0
    min_ratio_index = -1
    min_ratio = 0

    for index, x in enumerate(self.tableau):
      if x[entering_index] != 0 and x[len(x)-1] / x[entering_index] > 0:
        skip = index
        min_ratio_index = index
        min_ratio = x[len(x) - 1] / x[entering_index]
        break

    if min_ratio > 0:
      for index, x in enumerate(self.tableau):
        if index > skip and x[entering_index] > 0:
          ratio = x[len(x)-1] / x[entering_index]

          if min_ratio > ratio:
            min_ratio = ratio
            min_ratio_index = index

    return min_ratio_index

  def get_Ab(self):
    ''' Get A matrix with b vector appended. '''
    matrix = copy.deepcopy(self.A)

    for i in range(0, len(matrix)):
      matrix[i] += [self.b[i]]

    return matrix

  def should_terminate(self):
    ''' Determines whether there are any negative elements on the bottom row '''
    result = True
    index = len(self.tableau) - 1

    for i, x in enumerate(self.tableau[index]):
      if x < 0 and i != len(self.tableau[index]) - 1:
        result = False

    return result

  def get_current_solution(self):
    ''' Get the current solution from tableau. '''
    solution = {}

    for x in self.entering:
      if x != 'b':
        if x in self.departing:
          solution[x] = self.tableau[self.departing.index(x)][len(self.tableau[self.departing.index(x)]) - 1]
        else:
          solution[x] = 0

    solution['z'] = self.tableau[len(self.tableau) - 1][len(self.tableau[0]) - 1]
    return solution

  def _generate_identity(self, n):
    ''' Helper function for generating a square identity matrix. '''
    I = []

    for i in range(0, n):
      row = []
      for j in range(0, n):
        if i == j:
          row.append(1)
        else:
          row.append(0)
      I.append(row)

    return I

  def _print_tableau(self):
    ''' Print simplex tableau. '''
    print(' ', end=' ')
    for val in self.entering:
      print('{:^5}'.format(str(val)), end = ' ')
    print(' ')
    for num, row in enumerate(self.tableau):
      print('|', end = ' ')
      for val in row:
        print('{:^5}'.format(str(val)), end = ' ')
      if num < (len(self.tableau) - 1):
        print('| %s' % self.departing[num])
      else:
        print('|')

  def _prompt(self):
    input("Press enter to continue...")
