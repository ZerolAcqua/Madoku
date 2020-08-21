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

    grid_group = VGroup()
    line_group = VGroup()  ##存放宫线
    num_group = VGroup()
    num_check = False  # 盘面是否有数字

    square_list = []  # 存放格子
    row_list = []  # 存放行
    col_list = []  # 存放列
    box_list = []  # 存放宫
    line_list = []  # 存放宫线
    note_list = []  # 存放标记
    sudoku_group = VGroup()  # 数独盘面

    def create_board(self, file_name=None):
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

    ## 函数部分
    ## 填入数字，row和col从0起算
    def solve(self, row, col, num):
        num_text = TextMobject("%d" % num, color=self.solve_color)
        num_text.shift(self.square_list[row * 9 + col].get_center())
        self.num_group.add(num_text)
        self.play(Write(num_text))

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

    def show(self):
        tmp = VGroup()
        for i in range(len(self.note_list)):
            tmp.add(self.note_list[i])
        self.play(Write(tmp))
        self.note_list.clear()
        self.note_list.append(tmp)

    def erase(self):
        for i in range(len(self.note_list)):
            self.play(FadeOut(self.note_list[i]))
        self.note_list.clear()


class Sudoku_start(Sudoku_scene):
    def construct(self):
        ## 设置物体

        ## 文字
        introdution = TextMobject("一、认识数独盘面", tex_to_color_map={"数独": self.board_color})

        rule_title = TextMobject("二、数独的规则", tex_to_color_map={"数独": self.board_color})
        rule_text01 = TextMobject("规则1：数独的每行、每列，以及每个宫",
                                  tex_to_color_map={"数独": self.board_color, "行": self.row_color, "列": self.col_color,
                                                    "宫": self.box_color})
        rule_text02 = TextMobject("都有1-9九个数字，不能重复也不能缺少",
                                  tex_to_color_map={"1-9": PINK, "重复": ORANGE, "缺少": ORANGE})
        rule_text03 = TextMobject("规则2：一个正确的数独题目有唯一解", tex_to_color_map={"数独": self.board_color, "唯一": ORANGE})
        rule_text04 = TextMobject("不存在无解或多解的情况",
                                  tex_to_color_map={"不存在": PINK, "无解": ORANGE, "多解": ORANGE})

        explain_title = TextMobject("三、数独解法简介", tex_to_color_map={"数独": self.board_color})
        explain_text01 = TextMobject("根据规则1，第四行已经有8个数字", tex_to_color_map={"第四行": self.row_color})
        explain_text02 = TextMobject("只剩下数字8未出现")
        explain_text03 = TextMobject("因而第四行空缺的格子应填8", tex_to_color_map={"第四行": self.row_color})
        explain_text04 = TextMobject("同理,第五宫空缺的格子应填3", tex_to_color_map={"第五宫": self.box_color})

        explain_text05 = TextMobject("摒除：再看第七宫，还需填1、9两数", tex_to_color_map={"第七宫": self.box_color})
        explain_text06 = TextMobject("由于一行中每个数字只能出现一次", tex_to_color_map={"行": self.row_color})
        explain_text07 = TextMobject("而第八行已经有1", tex_to_color_map={"第八行": self.row_color})
        explain_text08 = TextMobject("所以，第七宫只有一格能填1", tex_to_color_map={"第七宫": self.box_color})
        explain_text09 = TextMobject("同理，也有几次摒除同时使用的")

        explain_text10 = TextMobject("解题中…")
        explain_text11 = TextMobject("完成！")

        thanks_text = TextMobject("感谢观看")
        name_text = TextMobject("By Zerol Acqua", tex_to_color_map={"Zerol Acqua": self.board_color})

        row_text = TextMobject("行", tex_to_color_map={"行": self.row_color})
        col_text = TextMobject("列", tex_to_color_map={"列": self.col_color})
        box_text = TextMobject("宫", tex_to_color_map={"宫": self.box_color})

        ## 盘面
        self.create_board("test.txt")

        ## 控制位置
        introdution.to_edge(UP)
        rule_title.to_edge(UP)
        rule_text01.to_edge(UP)
        rule_text02.to_edge(UP)
        rule_text03.to_edge(UP)
        rule_text04.to_edge(UP)
        explain_title.to_edge(UP)
        explain_text01.to_edge(UP)
        explain_text02.to_edge(UP)
        explain_text03.to_edge(UP)
        explain_text04.to_edge(UP)
        explain_text05.to_edge(UP)
        explain_text06.to_edge(UP)
        explain_text07.to_edge(UP)
        explain_text08.to_edge(UP)
        explain_text09.to_edge(UP)
        explain_text10.to_edge(UP)
        explain_text11.to_edge(UP)

        row_text.shift(np.array([-10 * self.scale, 4 * self.scale, 0]))
        col_text.shift(np.array([2 * self.scale, 10 * self.scale, 0]))
        box_text.shift(np.array([-6 * self.scale, -9 * self.scale, 0]))

        ## 动画

        ## 格子
        self.play(Write(self.grid_group))
        self.play(GrowFromCenter(self.line_list[0]),
                  GrowFromCenter(self.line_list[1]),
                  GrowFromCenter(self.line_list[2]),
                  GrowFromCenter(self.line_list[3]))

        ## 数字
        if (self.num_check):
            self.play(Write(self.num_group))

        ## 盘面介绍
        self.play(ApplyMethod(self.sudoku_group.next_to, introdution.get_edge_center(DOWN), DOWN))
        self.play(Write(introdution))
        self.wait(2)

        ## 行
        self.play(Transform(introdution, row_text),
                  ApplyMethod(self.sudoku_group.next_to,
                              row_text.get_edge_center(RIGHT) + np.array([0, -4 * self.scale, 0]),
                              RIGHT))
        self.row_highlight(2)

        ## 列
        self.play(Transform(introdution, col_text),
                  ApplyMethod(self.sudoku_group.next_to,
                              col_text.get_edge_center(DOWN) + np.array([-2 * self.scale, 0, 0]),
                              DOWN))
        self.col_highlight(5)

        ## 宫
        self.play(Transform(introdution, box_text),
                  ApplyMethod(self.sudoku_group.next_to,
                              box_text.get_edge_center(UP) + np.array([6 * self.scale, 0, 0]),
                              UP))
        self.box_highlight(6)

        ## 规则介绍
        self.play(Transform(introdution, rule_title),
                  ApplyMethod(self.sudoku_group.next_to, rule_title.get_edge_center(DOWN), DOWN))
        self.wait(2)
        self.play(FadeOut(introdution))

        self.play(Write(rule_text01))
        self.wait(1)
        self.play(Transform(rule_text01, rule_text02))
        self.wait(1)
        self.play(FadeOut(rule_text01))

        self.play(Write(rule_text03))
        self.wait(1)
        self.play(Transform(rule_text03, rule_text04))
        self.wait(1)

        ## 解法简介
        self.play(Transform(rule_text03, explain_title),
                  ApplyMethod(self.sudoku_group.next_to, explain_title.get_edge_center(DOWN), DOWN))
        self.wait(2)
        self.play(FadeOut(rule_text03))

        self.play(Write(explain_text01))
        self.wait(1)
        self.play(Transform(explain_text01, explain_text02))
        self.wait(1)
        self.play(Transform(explain_text01, explain_text03))
        self.wait(1)
        self.row_highlight(3)
        self.solve(3, 1, 8)
        self.play(FadeOut(explain_text01))

        self.play(Write(explain_text04))
        self.wait(1)
        self.box_highlight(4)
        self.solve(4, 4, 3)
        self.play(FadeOut(explain_text04))

        self.play(Write(explain_text05))
        self.wait(1)
        self.box_highlight(6)
        self.play(Transform(explain_text05, explain_text06))
        self.wait(1)
        self.play(Transform(explain_text05, explain_text07))
        self.wait(1)
        self.play(Transform(explain_text05, explain_text08))
        self.note(7, 8, 1, 0)
        self.show()
        self.solve(6, 1, 1)
        self.erase()
        self.wait(1)
        self.play(FadeOut(explain_text05))

        self.play(Write(explain_text09))
        self.wait(1)
        self.box_highlight(5)
        self.note(7, 7, 2, 1)
        self.note(1, 6, 2, 0)
        self.note(5, 0, 1, 1)
        self.show()
        self.solve(4, 8, 7)
        self.erase()

        self.wait(1)
        self.play(Transform(explain_text09, explain_text10))
        self.box_highlight(6)
        self.solve(7, 1, 9)

        self.note(8, 0, 1, 1)
        self.show()
        self.box_highlight(8)
        self.solve(6, 7, 8)
        self.erase()

        self.solve(8, 7, 9)

        self.note(4, 3, 1, 1)
        self.show()
        self.col_highlight(6)
        self.solve(5, 6, 8)
        self.erase()

        self.solve(4, 6, 9)

        self.note(4, 4, 1, 1)
        self.show()
        self.box_highlight(5)
        self.solve(5, 8, 3)
        self.erase()

        self.solve(4, 7, 4)

        self.row_highlight(5)
        self.solve(5, 1, 4)

        self.note(0, 1, 2, 0)
        self.note(6, 0, 2, 1)
        self.show()
        self.box_highlight(3)
        self.solve(4, 2, 6)
        self.erase()

        self.note(1, 0, 2, 0)
        self.show()
        self.solve(4, 1, 2)
        self.erase()

        self.solve(4, 0, 1)

        self.col_highlight(0)
        self.solve(0, 0, 4)

        self.col_highlight(1)
        self.solve(1, 1, 5)

        self.col_highlight(2)
        self.solve(0, 2, 9)

        self.note(1, 1, 1, 1)
        self.show()
        self.col_highlight(7)
        self.solve(2, 7, 5)
        self.erase()

        self.solve(1, 7, 1)

        self.note(3, 5, 2, 1)
        self.note(4, 5, 2, 1)
        self.show()
        self.row_highlight(0)
        self.solve(0, 5, 1)
        self.erase()

        self.note(0, 5, 2, 0)
        self.note(4, 5, 2, 0)
        self.show()
        self.row_highlight(8)
        self.solve(8, 5, 2)
        self.erase()

        self.note(5, 3, 2, 0)
        self.show()
        self.row_highlight(8)
        self.solve(8, 4, 1)
        self.erase()

        self.solve(8, 3, 5)

        self.note(8, 3, 2, 1)
        self.show()
        self.row_highlight(0)
        self.solve(0, 4, 5)
        self.erase()

        self.solve(0, 3, 7)

        self.note(0, 3, 2, 0)
        self.show()
        self.row_highlight(6)
        self.solve(6, 4, 7)
        self.erase()

        self.solve(6, 3, 9)

        self.note(3, 3, 2, 1)
        self.note(8, 5, 2, 1)
        self.note(1, 0, 1, 1)
        self.show()
        self.box_highlight(1)
        self.solve(2, 4, 2)
        self.erase()

        self.note(1, 2, 1, 1)
        self.show()
        self.col_highlight(4)
        self.solve(7, 4, 8)
        self.erase()

        self.solve(1, 4, 9)

        self.note(1, 4, 1, 1)
        self.show()
        self.col_highlight(8)
        self.solve(2, 8, 9)
        self.erase()

        self.solve(1, 8, 4)

        self.note(4, 3, 2, 1)
        self.show()
        self.row_highlight(2)
        self.solve(2, 5, 8)
        self.erase()

        self.solve(2, 3, 4)

        self.note(1, 8, 1, 0)
        self.show()
        self.col_highlight(5)
        self.solve(7, 5, 4)
        self.erase()

        self.solve(1, 5, 6)

        self.box_highlight(1)
        self.solve(1, 3, 3)

        self.box_highlight(7)
        self.solve(7, 3, 6)

        self.wait(1)
        self.play(Transform(explain_text09, explain_text11))
        self.wait(1)
        self.play(FadeOut(explain_text09))

        self.play(Transform(self.sudoku_group, thanks_text))
        self.wait(1)
        self.play(Transform(self.sudoku_group, name_text))
        self.wait(1)
