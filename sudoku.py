# -*- coding=utf-8 -*-

from manimlib.imports import*
from mydemo.Madoku.package_color import*
from mydemo.Madoku.package_motion import*


# @ZerolAcqua
# SudokuLine类，参考了@cigar666的CodeLine类
# 可以用于代替TexMObject
class SudokuLine(Text):
    CONFIG = {
        't2c': {
            '1': GREY_BROWN,
            '2': GREY_BROWN,
            '3': GREY_BROWN,
            '4': GREY_BROWN,
            '5': GREY_BROWN,
            '6': GREY_BROWN,
            '7': GREY_BROWN,
            '8': GREY_BROWN,
            '9': GREY_BROWN,
            '行': RED,
            '第一行': RED,
            '第二行': RED,
            '第三行': RED,
            '第四行': RED,
            '第五行': RED,
            '第六行': RED,
            '第七行': RED,
            '第八行': RED,
            '第九行': RED,
            'r1': RED,
            'r2': RED,
            'r3': RED,
            'r4': RED,
            'r5': RED,
            'r6': RED,
            'r7': RED,
            'r8': RED,
            'r9': RED,
            '列': YELLOW_B,
            '第一列': YELLOW_B,
            '第二列': YELLOW_B,
            '第三列': YELLOW_B,
            '第四列': YELLOW_B,
            '第五列': YELLOW_B,
            '第六列': YELLOW_B,
            '第七列': YELLOW_B,
            '第八列': YELLOW_B,
            '第九列': YELLOW_B,
            'c1': YELLOW_B,
            'c2': YELLOW_B,
            'c3': YELLOW_B,
            'c4': YELLOW_B,
            'c5': YELLOW_B,
            'c6': YELLOW_B,
            'c7': YELLOW_B,
            'c8': YELLOW_B,
            'c9': YELLOW_B,
            '宫': GREEN,
            '第一宫': GREEN,
            '第二宫': GREEN,
            '第三宫': GREEN,
            '第四宫': GREEN,
            '第五宫': GREEN,
            '第六宫': GREEN,
            '第七宫': GREEN,
            '第八宫': GREEN,
            '第九宫': GREEN,
            'b1': GREEN,
            'b2': GREEN,
            'b3': GREEN,
            'b4': GREEN,
            'b5': GREEN,
            'b6': GREEN,
            'b7': GREEN,
            'b8': GREEN,
            'b9': GREEN,
            '数独': GOLD,
            '无解': GOLD,
            '多解': GOLD,
            '候选数': ORANGE,
            '区块': ORANGE,
            '数对': ORANGE,
            '数组': ORANGE,
            '链': ORANGE,

            'Zerol': BLUE_B,
            'Acqua': BLUE_B,
            '丘卡': BLUE_B,
            '零醇丘卡': BLUE_B,
            'Naxi-s': BLUE_B,
            'tucoconum': BLUE_B,
            '~': WHITE,  # 随便搞个不常用的字符设成白色，以便在有时不能用空格占位时（比如涉及Transform）当空格用
        },
        'font': 'Consolas',
        'size': 0.36,
        'color': DARK_GRAY,
        'plot_depth': 2,
    }

    def __init__(self, text, **kwargs):
        Text.__init__(self, text, **kwargs)

# @Naxi-s
# 数独场景类，用于创建一个含有数字和候选数的盘面
# Acqua所做的修改有：① 封装成类（并不严格，其实只是把常量放在CONFIG里面，加了一堆self，把函数放在一个类里面了，封太死了反而不太方便）
#                 ② 删去了不必要的local()字典的调用
#                 ③ 使用replace字符串替换函数，兼容另一种数独的字符串表示(带"."的表示可以从HoDoKu中直接导出)
#                 ④ 将TextMobject换成了自定义的Text类——SudokuLine
# Todo:①能否改成重复使用的盘面呢，有时需要更换数独的题目，这时就只要求改变数独的数字了
# Todo:②已知数和填写的数字能否分别开来显示
class Sudoku(VGroup):
    # 这里是一些常量
    CONFIG = {
        # 可以更改的一些盘面参数
        'center_of_squares': [-3, 0],   # 盘面的位置
        'side_lenth_of_squares': 0.6,   # 正方形边长
        'distance_of_squares': 2 / 3,   # 正方形间距（按照中心距离算）
        'gap_of_sections': 0.04,        # 宫间距增量
        'square_color': BLUE,           # 正方形颜色

        # 关于数字元素的一些参数
        'nums_color': BLACK,            # 初始数颜色
        'num_scale': 1,                 # 初始数缩放
        'cand_color': BLACK,            # 候选数颜色
        'cand_scale': 0.4,              # 候选数缩放
        'gap_of_cand': 0.2,             # 候选数间距增量

        # 已知数
        'num_str' :\
            '.........' \
            '.........' \
            '.........' \
            '.........' \
            '.........' \
            '.........' \
            '.........' \
            '.........' \
            '.........',
    
        # ------------------------------------------------------ #
        # Acqua版本的一些参数
        'row_color': RED,               # 代表行的颜色
        'col_color': YELLOW_B,          # 代表列的颜色
        'box_color': GREEN,             # 代表宫的颜色

    }





    def __init__(self, **kwargs):
        VGroup.__init__(self, **kwargs)
        # ------组织数独类中的Object,对象的属性------

        # 关于运行数独方法基于的一些数据类型
        self.domain_num_list = []               # 存储81个int类型数据的列表，是初始盘面的数字
        self.domain_num_list_changing = []      # 存储81个int类型数据的列表，是当前数独盘面的数字
        self.domain_cand_list = []              # 存储81个列表，每个列表对应一个格子的int类型候选数，代表最初始的没有排除过的候选数的元素
        self.domain_cand_list_changing = []     # 存储81个列表，每个列表对应一个格子的int类型候选数，代表当前盘面的候选数的元素

        # 一些元素的列表
        self.squares_list = []      # 存储81个Square
        self.rows_list = []         # 存储9个列表，每个列表对应一行的Square
        self.cols_list = []         # 存储9个列表，每个列表对应一列的Square
        self.boxes_list = []        # 存储9个列表，每个列表对应一宫的Square
        self.nums_list = []         # 存储VMobject已知数的列表
        self.init_cands_list = []   # 存储81个列表，每个列表对应一个格子的VMobject候选数，代表最初始的没有排除过的候选数的元素
        self.cands_list = []        # 存储81个列表，每个列表对应一个格子的VMobject候选数，代表当前盘面的候选数的元素


        # 编号的列表
        self.rows_index_list = []   # 存储9个列表，每个列表对应一行的Square的下标
        self.cols_index_list = []   # 存储9个列表，每个列表对应一列的Square的下标
        self.boxes_index_list = []  # 存储9个列表，每个列表对应一宫的Square的下标
        self.except_list = []       # 存储81个列表，每个列表对一个格子所能排除的9+6+6=21个Square的下标


        # 一些元素的VGroup或VGroup的列表
        self.squares = VGroup()     # 存储81个Square的VGroup
        self.rows_v_list = []       # 存储9个VGroup，每个VGroup组织一行的Square
        self.cols_v_list = []       # 存储9个VGroup，每个VGroup组织一列的Square
        self.boxes_v_list = []      # 存储9个VGroup，每个VGroup组织一宫的Square
        self.nums = VGroup()        # 组织VMobject已知数的VGroup
        self.init_cands = VGroup()  # 包括81个子VGroup,每个VGroup包含一个格子的VMobject候选数，代表最初始的没有排除过的候选数的元素？？？
        self.cands = VGroup()       # 所有的81*（0,9）的VMobject候选数
        self.__create_borad()


    def __create_borad(self):
        for i in range(81):
            self.squares_list.append(Square(side_length= self.side_lenth_of_squares,
                                            color= self.square_color,
                                            fill_color= self.square_color,
                                            fill_opacity= 1,
                                            plot_depth= -1))
        t = 0
        for i in self.squares_list:
            i.move_to(RIGHT * (self.distance_of_squares * (t % 9 + 1) - 5 * self.distance_of_squares + (
                        ((t % 9) - (t % 9) % 3) / 3 - 1) * self.gap_of_sections) + DOWN * (
                            self.distance_of_squares * ((t - (t % 9)) / 9 + 1) - 5 * self.distance_of_squares + (
                            ((t - t % 9) / 9 - ((t - t % 9) / 9) % 3) / 3 - 1) * self.gap_of_sections) + (
                    self.center_of_squares[0]) * RIGHT + self.center_of_squares[1] * UP)
            t = t + 1
    
        # 行、列、宫的编号的列表
        for i in [0, 9, 18, 27, 36, 45, 54, 63, 72]:
            useless_list = []
            for j in range(0, 81):
                if self.row_check(i, j) == 1:
                    useless_list.append(j)
            self.rows_index_list.append(useless_list)
        for i in range(0, 9):
            useless_list = []
            for j in range(0, 81):
                if self.col_check(i, j) == 1:
                    useless_list.append(j)
            self.cols_index_list.append(useless_list)
        for i in [0, 3, 6, 27, 30, 33, 54, 57, 60]:
            useless_list = []
            for j in range(0, 81):
                if self.box_check(i, j) == 1:
                    useless_list.append(j)
            self.boxes_index_list.append(useless_list)
    
        # 排除域列表
        for i in range(0, 81):
            useless_list = []
            for j in self.rows_index_list:
                if i in j:
                    for k in j:
                        if k in useless_list:
                            pass
                        else:
                            useless_list.append(k)
            for j in self.cols_index_list:
                if i in j:
                    for k in j:
                        if k in useless_list:
                            pass
                        else:
                            useless_list.append(k)
            for j in self.boxes_index_list:
                if i in j:
                    for k in j:
                        if k in useless_list:
                            pass
                        else:
                            useless_list.append(k)
            self.except_list.append(useless_list)
    
        # 正方形行、列、宫对应的列表
        for i in self.rows_index_list:
            useless_list = []
            for j in i:
                useless_list.append(self.squares_list[j])
            self.rows_list.append(useless_list)
        for i in self.cols_index_list:
            useless_list = []
            for j in i:
                useless_list.append(self.squares_list[j])
            self.cols_list.append(useless_list)
        for i in self.boxes_index_list:
            useless_list = []
            for j in i:
                useless_list.append(self.squares_list[j])
            self.boxes_list.append(useless_list)
    
        # 初始数字列表和运行数字列表
        self.num_str=self.num_str.replace('.','0')  # 将字符串中的'.'转化'0'
        for i in range(1, 10):
            for j in range(1, 10):
                self.domain_num_list.append(int(self.num_str[9 * i + j - 10]))
                temp = SudokuLine(self.num_str[9 * i + j - 10], color=self.nums_color,
                                                                        plot_depth=2,size=self.num_scale)
                self.nums_list.append(temp)
                if self.num_str[9 * i + j - 10] == '0' :
                    temp.set_opacity(0)
        t = 0
        for i in self.nums_list:
            i.move_to(RIGHT * (self.distance_of_squares * (t % 9 + 1) - 5 * self.distance_of_squares + (
                        ((t % 9) - (t % 9) % 3) / 3 - 1) * self.gap_of_sections) + DOWN * (
                            self.distance_of_squares * ((t - (t % 9)) / 9 + 1) - 5 * self.distance_of_squares + (
                            ((t - t % 9) / 9 - ((t - t % 9) / 9) % 3) / 3 - 1) * self.gap_of_sections) + (
                    self.center_of_squares[0]) * RIGHT + (self.center_of_squares[1]) * UP)
            t = t + 1
        self.domain_num_list_changing = [i for i in self.domain_num_list]
    
        # 候选数列表和运行候选数列表
        # 下面两个for循环是用来确实候选数的位置的
        for i in range(0, 81):
            useless_list = []
            for t in range(1, 10):
                u = 9 * i + int(t) - 1
                temp= SudokuLine(str(t), color=self.cand_color, plot_depth=2,size=self.cand_scale)
                temp.shift(RIGHT * (u % 3 - 1) * self.gap_of_cand + DOWN * ((u % 9 - u % 3) / 3 - 1) * self.gap_of_cand)
                useless_list.append(temp)
            self.init_cands_list.append(useless_list)
        t = 0
        for i in self.init_cands_list:
            VGroup(*i).move_to(RIGHT * (self.distance_of_squares * (t % 9 + 1) - 5 * self.distance_of_squares + (
                        ((t % 9) - (t % 9) % 3) / 3 - 1) * self.gap_of_sections) + DOWN * (
                            self.distance_of_squares * ((t - (t % 9)) / 9 + 1) - 5 * self.distance_of_squares + (
                            ((t - t % 9) / 9 - ((t - t % 9) / 9) % 3) / 3 - 1) * self.gap_of_sections) + (
                    self.center_of_squares[0]) * RIGHT + (self.center_of_squares[1]) * UP)
            t = t + 1
        for i in self.init_cands_list:
            self.init_cands.add(VGroup(*i))
        useless_list1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for i in range(0, 81):
            # 如果此格有已知/已填数
            if self.domain_num_list[i] != 0:
                for j in self.init_cands_list[i]:
                    j.set_opacity(0)    # 候选数全部消失
            # 如果此格没有数
            if self.domain_num_list[i] == 0:
                useless_list = []
                useless_list2 = []
                useless_list3 = []
                # 对此格的排除域的每个格子
                for j in self.except_list[i]:
                    # 获取排除域的所有已知/已填数
                    useless_list.append(self.domain_num_list[j])
                # 找出候选数需要保留的下标
                for j in useless_list1:
                    if j in useless_list:
                        pass
                    else:
                        useless_list2.append(j - 1)
                # 将筛选后的候选数加入cands_list
                for j in useless_list2:
                    self.cands_list.append(self.init_cands_list[i][j])
                for j in useless_list1:
                    if (j - 1) in useless_list2:
                        pass
                    else:
                        useless_list3.append(j - 1)
                for j in useless_list3:
                    self.init_cands_list[i][j].set_opacity(0)   # ？
        self.cands = VGroup(*self.cands_list)
    
        # ------建立基本元素或群组的VGroup------
    
        # 正方形行、列、宫对应的VGroup列表
        self.squares = VGroup(*self.squares_list)
        self.squares.set_plot_depth(-1)
        for i in self.rows_list:
            useless_list = VGroup(*i)
            self.rows_v_list.append(useless_list)
        for i in self.cols_list:
            useless_list = VGroup(*i)
            self.cols_v_list.append(useless_list)
        for i in self.boxes_list:
            useless_list = VGroup(*i)
            self.boxes_v_list.append(useless_list)
        self.nums = VGroup(*self.nums_list)
    
        # 所有元素
        self.add(self.squares, self.nums, self.init_cands)



    # ------用于建立元素模型的辅助函数（可以不仅仅用于模型建造）------

    # 下面三个函数用于检查两个编号对应的格子是否在同一行、列、宫
    @staticmethod
    def row_check(index1, index2):
        if index1 - index1 % 9 == index2 - index2 % 9:
            return 1
        else:
            return 0

    @staticmethod
    def col_check(index1, index2):
        if (index1 - index2) % 9 == 0:
            return 1
        else:
            return 0

    @staticmethod
    def box_check(index1, index2):
        if ((index1 - index1 % 9) / 9) - ((index1 - index1 % 9) / 9) % 3 == ((index2 - index2 % 9) / 9) - (
                (index2 - index2 % 9) / 9) % 3 and (index1 % 9) - (index1 % 9) % 3 == (
                index2 % 9) - (index2 % 9) % 3:
            return 1
        else:
            return 0


