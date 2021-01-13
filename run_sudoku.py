import os

f = open('run_manim.bat', 'w')

py_file_name = 'Sudoku_subset.py'
classname = 'Sudoku_subset'
pl = ' -pl'
pm = ' -pm'
ph = ' -p --high_quality'
t = ' -t'
str01 = 'python -m manim ' + py_file_name + ' ' + classname + pl

f.write(str01)
f.close()

os.system('run_manim.bat')
