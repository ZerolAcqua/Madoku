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
            'r': RED,
            'r1': RED,
            'r2': RED,
            'r3': RED,
            'r4': RED,
            'r5': RED,
            'r6': RED,
            'r7': RED,
            'r8': RED,
            'r9': RED,
            'row': RED,
            '列': YELLOW_D,
            '第一列': YELLOW_D,
            '第二列': YELLOW_D,
            '第三列': YELLOW_D,
            '第四列': YELLOW_D,
            '第五列': YELLOW_D,
            '第六列': YELLOW_D,
            '第七列': YELLOW_D,
            '第八列': YELLOW_D,
            '第九列': YELLOW_D,
            'c': YELLOW_D,
            'c1': YELLOW_D,
            'c2': YELLOW_D,
            'c3': YELLOW_D,
            'c4': YELLOW_D,
            'c5': YELLOW_D,
            'c6': YELLOW_D,
            'c7': YELLOW_D,
            'c8': YELLOW_D,
            'c9': YELLOW_D,
            'column': YELLOW_D,
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
            'b': GREEN,
            'b1': GREEN,
            'b2': GREEN,
            'b3': GREEN,
            'b4': GREEN,
            'b5': GREEN,
            'b6': GREEN,
            'b7': GREEN,
            'b8': GREEN,
            'b9': GREEN,
            'block': GREEN,
            '数独': GOLD,
            '无解': GOLD,
            '多解': GOLD,
            '候选数': ORANGE,
            '单元格': ORANGE,
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
        'font': '庞门正道标题体',
        'size': 0.36,
        'color': DARK_GRAY,
        'plot_depth': 2,
    }

    def __init__(self, text, **kwargs):
        Text.__init__(self, text, **kwargs)

# @Naxi-s & @Acqua
# 数独场景类，用于创建一个含有数字和候选数的盘面
# Acqua所做的修改有：① 封装成类（其实只是把常量放在CONFIG里面，加了一堆self，把函数放在一个类里面了，封太死了反而不太方便）
#                 ② 删去了不必要的local()字典的调用
#                 ③ 使用replace字符串替换函数，兼容另一种数独的字符串表示(带"."的表示可以从HoDoKu中直接导出)
#                 ④ 将TextMobject换成了自定义的Text类——SudokuLine
# Todo:①能否改成重复使用的盘面呢，有时需要更换数独的题目，这时就只要求改变数独的数字了（再创建一个Sudoku类）
# Todo:②已知数和填写的数字能否分别开来显示（暂时解决）
# Todo:③不显示整个盘面的候选数，便于局部方法的讲解
class Sudoku(VGroup):
    # 这里是一些常量
    CONFIG = {
        # 可以更改的一些盘面参数
        'center_of_squares': [0, 0 ,0],   # 盘面的位置
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
        'col_color': YELLOW_D,          # 代表列的颜色
        'block_color': GREEN,             # 代表宫的颜色

    }

    # ------用于构建的辅助函数------

    # 下面三个函数用于检查两个编号对应的格子是否在同一行、列、宫
    @staticmethod
    def row_check(index1, index2):
        if index1 - index1 % 9 == index2 - index2 % 9:
            return True
        else:
            return False

    @staticmethod
    def col_check(index1, index2):
        if (index1 - index2) % 9 == 0:
            return True
        else:
            return False

    @staticmethod
    def block_check(index1, index2):
        if ((index1 - index1 % 9) / 9) - ((index1 - index1 % 9) / 9) % 3 == ((index2 - index2 % 9) / 9) - (
                (index2 - index2 % 9) / 9) % 3 and (index1 % 9) - (index1 % 9) % 3 == (
                index2 % 9) - (index2 % 9) % 3:
            return True
        else:
            return False


    # -------类属性及属性绑定--------
    # 编号的列表 TODO：其实这个编号是每个数独类公有的
    rows_index_list  = []  # 存储9个列表，每个列表对应一行的Square的下标
    cols_index_list = []  # 存储9个列表，每个列表对应一列的Square的下标
    blocks_index_list = []  # 存储9个列表，每个列表对应一宫的Square的下标
    except_list = []  # 存储81个列表，每个列表对应一个格子所能排除的9+6+6=21个Square的下标
    
    # 行、列、宫的编号的列表
    for i in [0, 9, 18, 27, 36, 45, 54, 63, 72]:
        useless_list = []
        for j in range(0, 81):
            if row_check.__func__(i, j) == 1:
                useless_list.append(j)
        rows_index_list .append(useless_list)
    for i in range(0, 9):
        useless_list = []
        for j in range(0, 81):
            if col_check.__func__(i, j) == 1:
                useless_list.append(j)
        cols_index_list.append(useless_list)
    for i in [0, 3, 6, 27, 30, 33, 54, 57, 60]:
        useless_list = []
        for j in range(0, 81):
            if block_check.__func__(i, j) == 1:
                useless_list.append(j)
        blocks_index_list.append(useless_list)

    # 排除域编号列表
    for i in range(0, 81):
        useless_list = []
        for j in rows_index_list :
            if i in j:
                for k in j:
                    if k in useless_list:
                        pass
                    else:
                        useless_list.append(k)
        for j in cols_index_list:
            if i in j:
                for k in j:
                    if k in useless_list:
                        pass
                    else:
                        useless_list.append(k)
        for j in blocks_index_list:
            if i in j:
                for k in j:
                    if k in useless_list:
                        pass
                    else:
                        useless_list.append(k)
        except_list.append(useless_list)

    

    def __init__(self, **kwargs):
        VGroup.__init__(self, **kwargs)
        # ------组织数独类中的Object,对象的属性------

        # 关于运行数独方法基于的一些数据类型
        self.domain_num_list = []               # 存储81个int类型数据的列表，是初始盘面的数字（不会改变）
        self.domain_num_list_changing = []      # 存储81个int类型数据的列表，是当前数独盘面的数字（会改变）
        self.domain_cand_list = []              #Todo: 存储81个列表，每个列表对应一个格子的int类型候选数，代表最初始的被提示数排除过的候选数的元素（不会改变）
        self.domain_cand_list_changing = []     #Todo: 存储81个列表，每个列表对应一个格子的int类型候选数，代表当前盘面的候选数的元素（会改变）

        # 一些元素的列表
        self.squares_list = []      # 存储81个Square
        self.rows_list = []         # 存储9个列表，每个列表对应一行的Square
        self.cols_list = []         # 存储9个列表，每个列表对应一列的Square
        self.blocks_list = []       # 存储9个列表，每个列表对应一宫的Square

        self.init_nums_list = []    # 存储VMobject已知数的列表,代表最初始的题目所给的提示数（不会改变）
        self.nums_list = []         # 存储VMobject已知数的列表,代表推导所得的已知数（会改变）
        self.init_cands_list = []   # 存储81个列表，每个列表对应一个格子的VMobject候选数，代表最初始的被提示数排除过的候选数的元素（不会改变）
        self.cands_list = []        # 存储81个列表，每个列表对应一个格子的VMobject候选数，代表当前盘面的候选数的元素（会改变）
                                    ## TODO【感觉这两个List控制的也是同一组VMonject啊？？？？除非用copy再复制一份候选数VMoject】


        # 一些元素的VGroup或VGroup的列表
        self.squares = VGroup()     # 存储81个Square的VGroup
        self.rows_v_list = []       # 存储9个VGroup，每个VGroup组织一行的Square
        self.cols_v_list = []       # 存储9个VGroup，每个VGroup组织一列的Square
        self.blocks_v_list = []     # 存储9个VGroup，每个VGroup组织一宫的Square
        self.nums = VGroup()        # 组织VMobject已知数的VGroup
        self.init_cands = VGroup()  # 包括81个子VGroup,每个VGroup包含一个格子的VMobject候选数，TODO【代表最初始的没有排除过的候选数的元素？？？】
        self.cands = VGroup()       # 所有的81*（0,9）的VMobject候选数，TODO【不过我感觉这两个VGroup控制的是同一组VMonject啊？？？？不如和init_cands合并了】
        self.__create_borad()


    def __create_borad(self):
        # 构造正方形
        for i in range(81):
            self.squares_list.append(Square(side_length= self.side_lenth_of_squares,
                                            color= self.square_color,
                                            fill_color= self.square_color,
                                            fill_opacity= 1,
                                            plot_depth= -1))
        # 排布成数独盘面
        t = 0
        for i in self.squares_list:
            i.move_to(RIGHT * (self.distance_of_squares * (t % 9 + 1) - 5 * self.distance_of_squares + (
                        ((t % 9) - (t % 9) % 3) / 3 - 1) * self.gap_of_sections) + DOWN * (
                            self.distance_of_squares * ((t - (t % 9)) / 9 + 1) - 5 * self.distance_of_squares + (
                            ((t - t % 9) / 9 - ((t - t % 9) / 9) % 3) / 3 - 1) * self.gap_of_sections) + (
                    self.center_of_squares[0]) * RIGHT + self.center_of_squares[1] * UP)
            t = t + 1



        # 行、列、宫正方形对应的列表
        for i in Sudoku.rows_index_list :
            useless_list = []
            for j in i:
                useless_list.append(self.squares_list[j])
            self.rows_list.append(useless_list)
        for i in Sudoku.cols_index_list:
            useless_list = []
            for j in i:
                useless_list.append(self.squares_list[j])
            self.cols_list.append(useless_list)
        for i in Sudoku.blocks_index_list:
            useless_list = []
            for j in i:
                useless_list.append(self.squares_list[j])
            self.blocks_list.append(useless_list)

        # 初始数字列表和运行数字列表
        self.num_str=self.num_str.replace('.','0')  # 将字符串中的'.'转化'0'
        for i in range(1, 10):
            for j in range(1, 10):
                self.domain_num_list.append(int(self.num_str[9 * i + j - 10]))
                temp = SudokuLine(self.num_str[9 * i + j - 10], color=self.nums_color,
                                plot_depth=2,size=self.num_scale,stroke_width=1)
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
        # 下面两个for循环是用来确定候选数的位置的
        # TODO:怎么没有初始化存储int型候选数的列表呢？
        for i in range(0, 81):
            useless_list = []
            for t in range(1, 10):
                u = 9 * i + int(t) - 1
                temp= SudokuLine(str(t), color=self.cand_color, plot_depth=2,size=self.cand_scale)
                temp.shift(RIGHT * (u % 3 - 1) * self.gap_of_cand + DOWN * ((u % 9 - u % 3) / 3 - 1) * self.gap_of_cand)
                useless_list.append(temp)
            self.init_cands_list.append(useless_list)
            # self.domain_cand_list.append([1,2,3,4,5,6,7,8,9])

        t = 0
        # 我猜这个地方是将一个单元格里的候选数整体移动到该正方形里，不过有getCenter相关的函数为什么不用呢？？
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
                for j in Sudoku.except_list[i]:
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
                    self.cands_list.append(self.init_cands_list[i][j])  # wtf? 似乎和我想的又不太一样，居然不是由81个列表组成的列表？
                for j in useless_list1:
                    if (j - 1) in useless_list2:
                        pass
                    else:
                        useless_list3.append(j - 1)
                for j in useless_list3:
                    self.init_cands_list[i][j].set_opacity(0)   # 使在已知数给出的条件下排除的候选数消失
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
        for i in self.blocks_list:
            useless_list = VGroup(*i)
            self.blocks_v_list.append(useless_list)
        self.nums = VGroup(*self.nums_list)



        # 所有元素
        self.add(self.squares, self.nums, self.init_cands)



  


# SudokuWithKnownNum@Acqua为了用于回溯之前视频的数独进度写的一个类，
# 用于将一些提示数变为填写的数字
# 如果里面的函数有用，可以迁移到之后的类中
class SudokuWithKnownNum(Sudoku):
    CONFIG = {
        'known_num_color':GRAY
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # 将最初的num_str设置的初始数，一部分改成非提示数的已知数（即填入的数字）
    def SetKnownNum(self,known_num_str):
        known_num_str = known_num_str.replace('.', '0')  # 将字符串中的'.'转化'0'
        for i in range(1, 10):
            for j in range(1, 10):
                if int(known_num_str[9 * i + j - 10])==0:
                    continue
                elif self.domain_num_list[9 * i + j - 10] == int(known_num_str[9 * i + j - 10]):
                    pos=self.nums_list[9 * i + j - 10].get_center()
                    self.nums_list[9 * i + j - 10].become(
                            SudokuLine(known_num_str[9 * i + j - 10],
                                plot_depth=2, size=self.num_scale, font='ZCOOL Addict Italic 01',strock_width=4)
                    )
                    self.nums_list[9 * i + j - 10].move_to(pos).set_color(self.known_num_color)


# 这个SudokuWithTag类是@Acqua为了展示数独行列宫的编号的，基本上只有sudoku_subset这一期视频会用到
class SudokuWithTag(SudokuWithKnownNum):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tag=VGroup(
            *[
                SudokuLine("r" + str(i + 1),size=self.num_scale).next_to(self.rows_v_list[i], LEFT)
                for i in range(9)
            ],
            *[
                SudokuLine("c" + str(i + 1),size=self.num_scale).next_to(self.cols_v_list[i], UP)
                for i in range(9)
            ],
            *[
                SudokuLine("b" + str(i + 1),size=self.num_scale).add_background_rectangle(color=WHITE, buff=0.2)\
                .move_to(self.blocks_v_list[i])
                for i in range(9)
            ]
        )
        self.tag.set_opacity(0)
        self.add(self.tag)


    # TODO:这个函数会返回等于指定数的候选数VGroup
    # TODO:最好用存储候选数int数据的列表来做
    def GetCertainCand(self,num=[1,2,3,4,5,6,7,8,9]):
        for n in num:
            for i in range(81):
                pass
