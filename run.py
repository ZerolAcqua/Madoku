import os

f = open('run_manim.bat', 'w')

py_file_name = 'Sudoku.py'
classname = 'Sudoku_start'
pl = ' -pl'
pm = ' -pm'
str01 = 'python -m manim ' + py_file_name + ' ' + classname + pl

f.write(str01)
f.close()

os.system('run_manim.bat')