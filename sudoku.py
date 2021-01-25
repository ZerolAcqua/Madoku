# -*- coding=utf-8 -*-
from manimlib.imports import*
from package_color import*

# ------参数调节------

# 可以更改的一些盘面参数，分别是盘面的位置、正方形边长、正方形间距（按照中心距离算）、宫间距增量、正方形颜色
center_of_squares = [-3, 0]
side_lenth_of_squares = 0.6
distance_of_squares = 2 / 3
gap_of_sections = 0.04
square_color = GREEN

# 关于数字元素的一些参数，包括初始数字的字符串、初始数的颜色、初始数的缩放
string1 = '041020000500006000008007240000009480906050302027300000053100900000600008000090130'
nums_color = BLACK
num_scale = 1
cand_color = BLACK
cand_scale = 0.4
gap_of_cand = 0.2

# ------名词汇总------

# 关于运行数独方法基于的一些数据类型
domain_num_list = []
domain_num_list_changing = []
domain_cand_list = []
domain_cand_list_changing = []

# 一些元素的列表
squares_list = []
rows_list = []
cols_list = []
boxes_list = []
nums_list = []
init_cands_list = []   # 这个是代表最初始的没有排除过的候选数的元素
cands_list = []

# 编号的列表
rows_index_list = []
cols_index_list = []
boxes_index_list = []
except_list = []

# 一些元素的VGroup或VGroup的列表
squares = VGroup()
rows_v_list = []
cols_v_list = []
boxes_v_list = []
nums = VGroup()
init_cands = VGroup()   # 这个是代表最初始的没有排除过的候选数的元素
cands = VGroup()
all_v = VGroup()


# ------用于建立元素模型的辅助函数（可以不仅仅用于模型建造）------

# 下面三个函数用于检查两个编号对应的格子是否在同一行、列、宫
def row_check(index1, index2):
    if index1 - index1 % 9 == index2 - index2 % 9:
        return 1
    else:
        return 0


def col_check(index1, index2):
    if (index1 - index2) % 9 == 0:
        return 1
    else:
        return 0


def box_check(index1, index2):
    if ((index1 - index1 % 9) / 9) - ((index1 - index1 % 9) / 9) % 3 == ((index2 - index2 % 9) / 9) - (
            (index2 - index2 % 9) / 9) % 3 and (index1 % 9) - (index1 % 9) % 3 == (
            index2 % 9) - (index2 % 9) % 3:
        return 1
    else:
        return 0


# ------建立基本元素或群组的列表------

# 正方形列表和位置调节
for i in range(1, 10):
    for j in range(1, 10):
        locals()['squ' + str(i) + 'squ' + str(j)] = Square(side_length=side_lenth_of_squares,
                                                           color=square_color,
                                                           fill_color=square_color,
                                                           fill_opacity=1,
                                                           plot_depth=-1)
        squares_list.append(locals()['squ' + str(i) + 'squ' + str(j)])
t = 0
for i in squares_list:
    i.move_to(RIGHT * (distance_of_squares * (t % 9 + 1) - 5 * distance_of_squares + (
                ((t % 9) - (t % 9) % 3) / 3 - 1) * gap_of_sections) + DOWN * (
                    distance_of_squares * ((t - (t % 9)) / 9 + 1) - 5 * distance_of_squares + (
                    ((t - t % 9) / 9 - ((t - t % 9) / 9) % 3) / 3 - 1) * gap_of_sections) + (
            center_of_squares[0]) * RIGHT + center_of_squares[1] * UP)
    t = t + 1

# 行、列、宫的编号的列表
for i in [0, 9, 18, 27, 36, 45, 54, 63, 72]:
    useless_list = []
    for j in range(0, 81):
        if row_check(i, j) == 1:
            useless_list.append(j)
    rows_index_list.append(useless_list)
for i in range(0, 9):
    useless_list = []
    for j in range(0, 81):
        if col_check(i, j) == 1:
            useless_list.append(j)
    cols_index_list.append(useless_list)
for i in [0, 3, 6, 27, 30, 33, 54, 57, 60]:
    useless_list = []
    for j in range(0, 81):
        if box_check(i, j) == 1:
            useless_list.append(j)
    boxes_index_list.append(useless_list)

# 排除域列表
for i in range(0, 81):
    useless_list = []
    for j in rows_index_list:
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
    for j in boxes_index_list:
        if i in j:
            for k in j:
                if k in useless_list:
                    pass
                else:
                    useless_list.append(k)
    except_list.append(useless_list)

# 正方形行、列、宫对应的列表
for i in rows_index_list:
    useless_list = []
    for j in i:
        useless_list.append(squares_list[j])
    rows_list.append(useless_list)
for i in cols_index_list:
    useless_list = []
    for j in i:
        useless_list.append(squares_list[j])
    cols_list.append(useless_list)
for i in boxes_index_list:
    useless_list = []
    for j in i:
        useless_list.append(squares_list[j])
    boxes_list.append(useless_list)

# 初始数字列表和运行数字列表
for i in range(1, 10):
    for j in range(1, 10):
        domain_num_list.append(int(string1[9 * i + j - 10]))
        locals()['num' + str(i) + 'num' + str(j)] = TextMobject(string1[9 * i + j - 10], color=nums_color,
                                                                plot_depth=2).scale(num_scale)
        nums_list.append(locals()['num' + str(i) + 'num' + str(j)])
        if int(string1[9 * i + j - 10]) == 0:
            locals()['num' + str(i) + 'num' + str(j)].set_opacity(0)
t = 0
for i in nums_list:
    i.move_to(RIGHT * (distance_of_squares * (t % 9 + 1) - 5 * distance_of_squares + (
                ((t % 9) - (t % 9) % 3) / 3 - 1) * gap_of_sections) + DOWN * (
                    distance_of_squares * ((t - (t % 9)) / 9 + 1) - 5 * distance_of_squares + (
                    ((t - t % 9) / 9 - ((t - t % 9) / 9) % 3) / 3 - 1) * gap_of_sections) + (
            center_of_squares[0]) * RIGHT + (center_of_squares[1]) * UP)
    t = t + 1
domain_num_list_changing = [i for i in domain_num_list]

# 候选数列表和运行候选数列表
for i in range(0, 81):
    useless_list = []
    for t in range(1, 10):
        u = 9 * i + int(t) - 1
        locals()['little_num' + str(i + 1) + 'little_num' + str(t)] = TextMobject(str(t), color=cand_color, plot_depth=2).scale(
            cand_scale)
        locals()['little_num' + str(i + 1) + 'little_num' + str(t)].shift(
            RIGHT * (u % 3 - 1) * gap_of_cand + DOWN * ((u % 9 - u % 3) / 3 - 1) * gap_of_cand)
        useless_list.append(locals()['little_num' + str(i + 1) + 'little_num' + str(t)])
    init_cands_list.append(useless_list)
t = 0
for i in init_cands_list:
    VGroup(*i).move_to(RIGHT * (distance_of_squares * (t % 9 + 1) - 5 * distance_of_squares + (
                ((t % 9) - (t % 9) % 3) / 3 - 1) * gap_of_sections) + DOWN * (
                    distance_of_squares * ((t - (t % 9)) / 9 + 1) - 5 * distance_of_squares + (
                    ((t - t % 9) / 9 - ((t - t % 9) / 9) % 3) / 3 - 1) * gap_of_sections) + (
            center_of_squares[0]) * RIGHT + (center_of_squares[1]) * UP)
    t = t + 1
for i in init_cands_list:
    init_cands.add(VGroup(*i))
useless_list1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
for i in range(0, 81):
    if domain_num_list[i] == 0:
        useless_list = []
        useless_list2 = []
        for j in except_list[i]:
            useless_list.append(domain_num_list[j])
        for j in useless_list1:
            if j in useless_list:
                pass
            else:
                useless_list2.append(j - 1)
        for j in useless_list2:
            cands_list.append(init_cands_list[i][j])
cands = VGroup(*cands_list)

# ------建立基本元素或群组的VGroup------

# 正方形行、列、宫对应的VGroup列表
squares = VGroup(*squares_list)
squares.set_plot_depth(-1)
for i in rows_list:
    useless_list = VGroup(*i)
    rows_v_list.append(useless_list)
for i in cols_list:
    useless_list = VGroup(*i)
    cols_v_list.append(useless_list)
for i in boxes_list:
    useless_list = VGroup(*i)
    boxes_v_list.append(useless_list)
nums = VGroup(*nums_list)

# 所有元素
all_v = VGroup(squares, nums, init_cands)


# ------动画制作------

class TestScene(ThreeDScene):

    def construct(self):
        self.wait()
        self.play(Write(squares))
        self.play(Write(nums))
        self.play(Write(cands))
        self.play(all_v.scale, 0.5)
        self.wait()