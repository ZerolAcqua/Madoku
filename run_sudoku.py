import os

f = open('run_manim.bat', 'w')

py_file_name = 'Test.py'
classname = 'TestScene'

# -l 最低画质 480P15
# -m 中等画质 720P30
# –high_quality18 高画质 1080P60
# -w 导出 (最高) 画质 1440P60(2K)
# -uhd 超高清 4K120fps(B站最高,MK版本)

pl = ' -pl'
pm = ' -pm'
ph = ' -p --high_quality'
pw = ' -pw'              # "最高"

t = ' -t'               # 透明
n = ' -n 200'

str01 = 'python -m manim ' + py_file_name + ' ' + classname + pm ;

f.write(str01)
f.close()

os.system('run_manim.bat')
