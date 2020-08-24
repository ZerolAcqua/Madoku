import os

f = open('run_manim.bat', 'w')

py_file_name = 'Show_Sudoku.py'
classname = 'Sudoku_basic'
pl = ' -pl'
pm = ' -pm'
str01 = 'python -m manim ' + py_file_name + ' ' + classname + pl

f.write(str01)
f.close()

os.system('run_manim.bat')
