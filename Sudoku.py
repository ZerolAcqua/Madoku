from manimlib.imports import *
import copy


class Sudoku_scene(Scene):
    CONFIG = {
        'board_color': BLUE,  # 格子的颜色
        'solve_color': WHITE,  # 填写数字的颜色
        'row_color': RED,  # 行的颜色
        'col_color': YELLOW,  # 列的颜色
        'box_color': GREEN,  # 宫的颜色
        'scale': 0.35,  # 格子的比例
    }

    num_check = False  # 盘面是否有数字
    cand_check = False  # 是否使用候选数

    line_group = VGroup()  # 存放宫线
    grid_group = VGroup()  # 网格汇总
    num_group = VGroup()  # 已知数
    cand_group = VGroup()  # 候选数
    sudoku_group = VGroup()  # 数独盘面

    square_list = []  # 存放格子
    row_list = []  # 存放行
    col_list = []  # 存放列
    box_list = []  # 存放宫
    line_list = []  # 存放宫线
    note_list = []  # 存放标记
    highlight_list = []  # 存放强调格子
    cand_list = []  # 存放81个格子对应的候选数
    cand_del_list = []  # 存放被删掉的候选数

    def create_board(self, file_name=None, cand_check=False):
        self.cand_check = cand_check
        ## 行
        for i in range(9):
            row_group = VGroup()
            for j in range(9):
                square_ij = Square(color=self.board_color, fill_opacity=0)
                square_ij.scale(self.scale)
                square_ij.shift(
                    np.array([j * 2 * self.scale - 8 * self.scale, -i * 2 * self.scale + 9 * self.scale, 0]))
                self.square_list.append(square_ij)
                row_group.add(square_ij)
            self.row_list.append(row_group)
            self.grid_group.add(row_group)

        ## 列
        for j in range(9):
            col_group = VGroup()
            for i in range(9):
                col_group.add(self.square_list[i * 9 + j])
            self.col_list.append(col_group)

        ## 宫
        for i in range(3):
            for j in range(3):
                box_group = VGroup()
                for k in range(3):
                    box_group.add(self.square_list[i * 3 * 9 + j * 3 + k * 9])
                    box_group.add(self.square_list[i * 3 * 9 + j * 3 + k * 9 + 1])
                    box_group.add(self.square_list[i * 3 * 9 + j * 3 + k * 9 + 2])
                self.box_list.append(box_group)

        ## 宫线
        line01 = Line(np.array([-3 * self.scale, 10 * self.scale, 0]),
                      np.array([-3 * self.scale, -8 * self.scale, 0]))
        line01.set_color(self.board_color)
        line01.set_stroke(width=9)
        line02 = Line(np.array([3 * self.scale, 10 * self.scale, 0]),
                      np.array([3 * self.scale, -8 * self.scale, 0]))
        line02.set_color(self.board_color)
        line02.set_stroke(width=9)
        line03 = Line(np.array([-9 * self.scale, 4 * self.scale, 0]),
                      np.array([9 * self.scale, 4 * self.scale, 0]))
        line03.set_color(self.board_color)
        line03.set_stroke(width=9)
        line04 = Line(np.array([-9 * self.scale, -2 * self.scale, 0]),
                      np.array([9 * self.scale, -2 * self.scale, 0]))
        line04.set_color(self.board_color)
        line04.set_stroke(width=9)

        self.line_group.add(line01)
        self.line_group.add(line02)
        self.line_group.add(line03)
        self.line_group.add(line04)

        self.line_list.append(line01)
        self.line_list.append(line02)
        self.line_list.append(line03)
        self.line_list.append(line04)

        ## 数字
        ## 文件读取

        if (file_name != None):
            with open(file_name, 'r') as f1:
                data = f1.readline()
                for i in range(81):
                    if (data[i] != '.'):
                        num_text = TextMobject(data[i])
                        num_text.set_color(self.board_color)
                        num_text.shift(self.square_list[i].get_center())
                        self.num_group.add(num_text)
                self.num_check = True

        self.sudoku_group = VGroup(self.grid_group, self.line_group, self.num_group)

        if (self.cand_check):
            self.cand_mark()
            self.sudoku_group.add(self.cand_group)

    ## 函数部分

    ## 盘面
    def show_grid(self):
        self.play(Write(self.grid_group))
        self.play(GrowFromCenter(self.line_list[0]),
                  GrowFromCenter(self.line_list[1]),
                  GrowFromCenter(self.line_list[2]),
                  GrowFromCenter(self.line_list[3]))

    ## 返回该格中心的位矢
    def get_grid_center(self, row, col):
        return self.square_list[row * 9 + col].get_center()

    ## 初始数字

    ## 设置初始数字
    def init_num(self, file_name):
        if (file_name == None or self.num_check == True):
            return
        with open(file_name, 'r') as f1:
            data = f1.readline()
            for i in range(81):
                if (data[i] != '.'):
                    num_text = TextMobject(data[i])
                    num_text.set_color(self.board_color)
                    num_text.shift(self.square_list[i].get_center())
                    self.num_group.add(num_text)
            self.num_check = True

    ## 展示初始数字
    def show_num(self):
        if (self.num_check):
            self.play(Write(self.num_group))

    ## 清除数字
    def clear_num(self):
        if (self.cand_check == True):
            self.reset_cand()
        if (self.num_check == True):
            self.play(Uncreate(self.num_group))
            self.num_check = False

    ## 更改数字
    def change_num(self, file_name):
        self.clear_num()
        self.init_num(file_name)

    ## 候选数
    ## 使用候选数
    def cand_mark(self):
        self.cand_check = True
        rate = 2 / 3 - 0.1
        for i in range(81):
            tmp = self.square_list[i].get_center()
            cand_num_list = []  # 存放一个格子对应的候选数
            num = 1
            for j in [1, 0, -1]:
                for k in [-1, 0, 1]:
                    num_text = TextMobject("%d" % num)
                    num_text.set_color(self.solve_color)
                    num_text.set_opacity(0)
                    num_text.scale(self.scale * 1.3)
                    num_text.shift(tmp + rate * j * self.scale * UP + rate * k * self.scale * RIGHT)
                    self.cand_group.add(num_text)
                    cand_num_list.append(num_text)
                    num += 1
            self.cand_list.append(cand_num_list)

    ## 设置并显示该格候选数
    def set_show_cand(self, row, col, array):
        tmp = self.set_cand(row, col, array)
        self.play(Write(tmp))

    ## 设置候选数
    def load_cand(self, file_name):
        if (file_name == None or self.cand_check == False):
            return
        with open(file_name, 'r') as f1:
            for data in f1.readlines():
                tmp_list = list(data.strip('\n'))
                tmp_list = list(map(int, tmp_list))
                row = tmp_list[0]
                col = tmp_list[1]
                array = tmp_list[2:]
                self.set_cand(row, col, array)

    def set_cand(self, row, col, array):
        if (self.cand_check == False):
            return
        tmp = VGroup()
        for num in array:
            if (num >= 1 and num <= 9):
                self.cand_list[row * 9 + col][num - 1].set_opacity(1)
                tmp.add(self.cand_list[row * 9 + col][num - 1])
        return tmp

    ## 显示全部候选数
    def show_cand(self):
        if (self.cand_check == False):
            return
        self.play(Write(self.cand_group))

    ## 清除候选数
    def reset_cand(self):
        if (self.cand_check == True):
            self.play(ApplyMethod(self.cand_group.set_opacity, 0))

    ## 删除某个候选数
    ## 注意候选数和num是一样的，row和col与盘面是差一的
    def del_cand(self, row, col, num, show=True):
        if (self.cand_check == False):
            return
        if (show == True):
            self.play(ApplyMethod(self.cand_list[row * 9 + col][num - 1].set_opacity, 0))
        else:
            self.cand_del_list.append(self.cand_list[row * 9 + col][num - 1])

    def show_del_cand_then_clear(self):
        tmp = VGroup()
        for i in self.cand_del_list:
            tmp.add(i)
        self.play(ApplyMethod(tmp.set_opacity, 0))
        self.cand_del_list.clear()

    ## 删除某格的除了except_cand的候选数
    def show_del_square_cand_then_clear(self, row, col, except_cand=0):
        if (self.cand_check == False):
            return
        for i in range(1, 10):
            if (i != except_cand):
                self.del_cand(row, col, i, False)
        self.show_del_cand_then_clear()

    ## 添加某个候选数
    ## 注意候选数和num是一样的，row和col与盘面是差一的
    def add_cand(self, row, col, num):
        if (self.cand_check == False):
            return
        self.play(ApplyMethod(self.cand_list[row * 9 + col][num - 1].set_opacity, 1))

    ## 解题&讲解&标注&强调

    ## 填入数字 row和col从0起算
    def solve(self, row, col, num):
        num_text = TextMobject("%d" % num, color=self.solve_color)
        num_text.shift(self.square_list[row * 9 + col].get_center())
        self.num_group.add(num_text)
        self.play(Write(num_text))

    ## 从候选数得到数字
    def solve_from_cand(self, row, col, num):
        if (self.cand_check == False):
            self.solve(row, col, num)
        else:
            num_text = TextMobject("%d" % num, color=self.solve_color)
            num_text.shift(self.square_list[row * 9 + col].get_center())
            self.play(ReplacementTransform(self.cand_list[row * 9 + col][num - 1].copy(), num_text),
                      ApplyMethod(self.cand_list[row * 9 + col][0].set_opacity, 0),
                      ApplyMethod(self.cand_list[row * 9 + col][1].set_opacity, 0),
                      ApplyMethod(self.cand_list[row * 9 + col][2].set_opacity, 0),
                      ApplyMethod(self.cand_list[row * 9 + col][3].set_opacity, 0),
                      ApplyMethod(self.cand_list[row * 9 + col][4].set_opacity, 0),
                      ApplyMethod(self.cand_list[row * 9 + col][5].set_opacity, 0),
                      ApplyMethod(self.cand_list[row * 9 + col][6].set_opacity, 0),
                      ApplyMethod(self.cand_list[row * 9 + col][7].set_opacity, 0),
                      ApplyMethod(self.cand_list[row * 9 + col][8].set_opacity, 0),
                      )
            self.num_group.add(num_text)

    ## 强调候选数或者是特定格子，如果num是0，强调此格子
    ## 录入
    def add_num_highlight(self, row, col, num=0):
        if (num <= 0):
            tmp = self.square_list[row * 9 + col].copy()
            tmp.set_fill(color=PURPLE)

            self.highlight_list.append(tmp)
        elif (num <= 9 and self.cand_check == True):
            cen = self.cand_list[row * 9 + col][num - 1].get_center()
            tmp = Square(color=PURPLE)
            tmp.scale((1 / 3 - 0.1) * self.scale)
            tmp.shift(cen)
            self.highlight_list.append(tmp)

    ## 展示
    def show_num_highlight(self):
        tmp = VGroup()
        for i in self.highlight_list:
            tmp.add(i)
        self.highlight_list.clear()
        self.play(ApplyMethod(tmp.set_opacity, 0.7))

        self.highlight_list.append(tmp)

    ## 清除
    def erase_num_highlight(self):
        for i in self.highlight_list:
            self.play(ApplyMethod(i.set_opacity, 0))
        self.highlight_list.clear()

    ## 强调
    ## 填入数字，row\col\box从0起算
    def row_highlight(self, row):
        self.play(ApplyMethod(self.row_list[row].set_fill, self.row_color, 0.7))
        self.play(ApplyMethod(self.row_list[row].set_fill, self.row_color, 0))

    def col_highlight(self, col):
        self.play(ApplyMethod(self.col_list[col].set_fill, self.col_color, 0.7))
        self.play(ApplyMethod(self.col_list[col].set_fill, self.col_color, 0))

    def box_highlight(self, box):
        self.play(ApplyMethod(self.box_list[box].set_fill, self.box_color, 0.7))
        self.play(ApplyMethod(self.box_list[box].set_fill, self.box_color, 0))

    ## 摒除
    ## 录入标记
    ## type: 1=row 2=col    dir：0=向左/向下 1=向右/向上
    def note(self, row=0, col=0, type=1, dir=0):
        note_group = VGroup()
        if (type == 1):
            circle = Circle(color=self.row_color, fill_opacity=0)
            circle.scale(self.scale)
            circle.shift(self.square_list[row * 9 + col].get_center())
            if (dir == 0):
                line = Line(self.square_list[row * 9 + col].get_center(),
                            self.square_list[row * 9 + 0].get_center(),
                            color=self.row_color)
            else:
                line = Line(self.square_list[row * 9 + col].get_center(),
                            self.square_list[row * 9 + 8].get_center(),
                            color=self.row_color)
        else:
            circle = Circle(color=self.col_color, fill_opacity=0)
            circle.scale(self.scale)
            circle.shift(self.square_list[row * 9 + col].get_center())
            if (dir == 0):
                line = Line(self.square_list[row * 9 + col].get_center(),
                            self.square_list[8 * 9 + col].get_center(),
                            color=self.col_color)
            else:
                line = Line(self.square_list[row * 9 + col].get_center(),
                            self.square_list[0 * 9 + col].get_center(),
                            color=self.col_color)

        note_group.add(circle)
        note_group.add(line)
        self.note_list.append((note_group))

        return note_group

    def show_note(self):
        tmp = VGroup()
        for i in self.note_list:
            tmp.add(i)
        self.play(Write(tmp))
        self.note_list.clear()
        self.note_list.append(tmp)

    def erase_note(self):
        for i in self.note_list:
            self.play(FadeOut(i))
        self.note_list.clear()

    def clear_note(self):
        self.note_list.clear()
