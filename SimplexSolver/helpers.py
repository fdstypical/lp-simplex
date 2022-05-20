import os
import csv

def clear():
  return os.system('cls' if os.name == 'nt' else 'clear')
