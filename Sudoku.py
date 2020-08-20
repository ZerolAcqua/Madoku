from manimlib.imports import *
import copy


class Sudoku_Manim(Scene):

    def construct(self):

        ## 函数

        ## 填入数字，row和col从0起算
        def solve(row, col, num):
            num_text = TextMobject("%d" % num, color=WHITE)
            num_text.shift(square_list[row * 9 + col].get_center())
            num_group.add(num_text)
            self.play(Write(num_text))

        ## 强调
        ## 填入数字，row\col\box从0起算
        def row_highlight(row):
            self.play(ApplyMethod(row_list[row].set_fill, RED, 0.7))
            self.play(ApplyMethod(row_list[row].set_fill, RED, 0))

        def col_highlight(col):
            self.play(ApplyMethod(col_list[col].set_fill, YELLOW, 0.7))
            self.play(ApplyMethod(col_list[col].set_fill, YELLOW, 0))

        def box_highlight(box):
            self.play(ApplyMethod(box_list[box].set_fill, GREEN, 0.7))
            self.play(ApplyMethod(box_list[box].set_fill, GREEN, 0))

        ## 摒除
        ## type: 1=row 2=col    dir：0=向左/向下 1=向右/向上
        def note(row=0, col=0, type=1, dir=0):
            note_group = VGroup()
            if (type == 1):
                circle = Circle(color=RED, fill_opacity=0)
                circle.scale(size)
                circle.shift(square_list[row * 9 + col].get_center())
                if (dir == 0):
                    line = Line(square_list[row * 9 + col].get_center(), square_list[row * 9 + 0].get_center(),
                                color=RED)
                else:
                    line = Line(square_list[row * 9 + col].get_center(), square_list[row * 9 + 8].get_center(),
                                color=RED)
            else:
                circle = Circle(color=YELLOW, fill_opacity=0)
                circle.scale(size)
                circle.shift(square_list[row * 9 + col].get_center())
                if (dir == 0):
                    line = Line(square_list[row * 9 + col].get_center(), square_list[8 * 9 + col].get_center(),
                                color=YELLOW)
                else:
                    line = Line(square_list[row * 9 + col].get_center(), square_list[0 * 9 + col].get_center(),
                                color=YELLOW)

            note_group.add(circle)
            note_group.add(line)
            note_list.append((note_group))

        def show():
            tmp = VGroup()
            for i in range(len(note_list)):
                tmp.add(note_list[i])
            self.play(Write(tmp))
            note_list.clear()
            note_list.append(tmp)

        def erase():
            for i in range(len(note_list)):
                self.play(FadeOut(note_list[i]))
            note_list.clear()

        ## 文件读取

        f1 = open('../test.txt', 'r')
        data = f1.readline()

        ## 设置物体

        size = 0.35
        bias = 0.03
        grid_group = VGroup()
        line_group = VGroup()  ##存放宫线

        num_group = VGroup()
        square_list = []  ## 存放格子
        row_list = []  ## 存放行
        col_list = []  ## 存放列
        box_list = []  ## 存放宫
        note_list = []  ##存放标记

        rectangle = Rectangle()

        ## 文字
        introdution = TextMobject("一、认识数独盘面", tex_to_color_map={"数独": BLUE})

        rule_title = TextMobject("二、数独的规则", tex_to_color_map={"数独": BLUE})
        rule_text01 = TextMobject("规则1：数独的每行、每列，以及每个宫",
                                  tex_to_color_map={"数独": BLUE, "行": RED, "列": YELLOW, "宫": GREEN})
        rule_text02 = TextMobject("都有1-9九个数字，不能重复也不能缺少",
                                  tex_to_color_map={"1-9": PINK, "重复": ORANGE, "缺少": ORANGE})
        rule_text03 = TextMobject("规则2：一个正确的数独题目有唯一解", tex_to_color_map={"数独": BLUE, "唯一": ORANGE})
        rule_text04 = TextMobject("不存在无解或多解的情况",
                                  tex_to_color_map={"不存在": PINK, "无解": ORANGE, "多解": ORANGE})

        explain_title = TextMobject("三、数独解法简介", tex_to_color_map={"数独": BLUE})
        explain_text01 = TextMobject("根据规则1，第四行已经有8个数字", tex_to_color_map={"第四行": RED})
        explain_text02 = TextMobject("只剩下数字8未出现")
        explain_text03 = TextMobject("因而第四行空缺的格子应填8", tex_to_color_map={"第四行": RED})
        explain_text04 = TextMobject("同理,第五宫空缺的格子应填3", tex_to_color_map={"第五宫": GREEN})

        explain_text05 = TextMobject("摒除：再看第七宫，还需填1、9两数", tex_to_color_map={"第七宫": GREEN})
        explain_text06 = TextMobject("由于一行中每个数字只能出现一次", tex_to_color_map={"行": RED})
        explain_text07 = TextMobject("而第八行已经有1", tex_to_color_map={"第八行": RED})
        explain_text08 = TextMobject("所以，第七宫只有一格能填1", tex_to_color_map={"第七宫": GREEN})
        explain_text09 = TextMobject("同理，也有几次摒除同时使用的")

        explain_text10 = TextMobject("解题中…")
        explain_text11 = TextMobject("完成！")

        thanks_text = TextMobject("感谢观看")
        name_text = TextMobject("By Zerol Acqua", tex_to_color_map={"Zerol Acqua": BLUE})

        row_text = TextMobject("行", tex_to_color_map={"行": RED})
        col_text = TextMobject("列", tex_to_color_map={"列": YELLOW})
        box_text = TextMobject("宫", tex_to_color_map={"宫": GREEN})

        ## 行
        for i in range(9):
            row_group = VGroup()
            for j in range(9):
                square_ij = Square(color=BLUE, fill_opacity=0)
                square_ij.scale(size)
                square_ij.shift(np.array([j * 2 * size - 8 * size, -i * 2 * size + 9 * size, 0]))
                square_list.append(square_ij)
                row_group.add(square_ij)
            row_list.append(row_group)
            grid_group.add(row_group)

        ## 数字
        for i in range(81):
            if (data[i] != '.'):
                num_text = TextMobject(data[i])
                num_text.set_color(BLUE)
                num_text.shift(square_list[i].get_center())
                num_group.add(num_text)
        f1.close()

        ## 列
        for j in range(9):
            col_group = VGroup()
            for i in range(9):
                col_group.add(square_list[i * 9 + j])
            col_list.append(col_group)

        ## 宫
        for i in range(3):
            for j in range(3):
                box_group = VGroup()
                for k in range(3):
                    box_group.add(square_list[i * 3 * 9 + j * 3 + k * 9])
                    box_group.add(square_list[i * 3 * 9 + j * 3 + k * 9 + 1])
                    box_group.add(square_list[i * 3 * 9 + j * 3 + k * 9 + 2])
                box_list.append(box_group)

        ## 宫线
        line01 = Line(np.array([-3 * size - bias, 10 * size, 0]), np.array([-3 * size - bias, -8 * size, 0]))
        line01.set_color(BLUE)
        line02 = Line(np.array([3 * size - bias, 10 * size, 0]), np.array([3 * size - bias, -8 * size, 0]))
        line02.set_color(BLUE)
        line03 = Line(np.array([-9 * size, 4 * size - bias, 0]), np.array([9 * size, 4 * size - bias, 0]))
        line03.set_color(BLUE)
        line04 = Line(np.array([-9 * size, -2 * size - bias, 0]), np.array([9 * size, -2 * size - bias, 0]))
        line04.set_color(BLUE)
        line05 = Line(np.array([-3 * size + bias, 10 * size, 0]), np.array([-3 * size + bias, -8 * size, 0]))
        line05.set_color(BLUE)
        line06 = Line(np.array([3 * size + bias, 10 * size, 0]), np.array([3 * size + bias, -8 * size, 0]))
        line06.set_color(BLUE)
        line07 = Line(np.array([-9 * size, 4 * size + bias, 0]), np.array([9 * size, 4 * size + bias, 0]))
        line07.set_color(BLUE)
        line08 = Line(np.array([-9 * size, -2 * size + bias, 0]), np.array([9 * size, -2 * size + bias, 0]))
        line08.set_color(BLUE)

        line_group.add(line01)
        line_group.add(line02)
        line_group.add(line03)
        line_group.add(line04)
        line_group.add(line05)
        line_group.add(line06)
        line_group.add(line07)
        line_group.add(line08)

        sudoku_group = VGroup(grid_group, line_group, num_group)

        # soduku_group02=copy.deepcopy(sudoku_group)

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

        row_text.shift(np.array([-10 * size, 4 * size, 0]))
        col_text.shift(np.array([2 * size, 10 * size, 0]))
        box_text.shift(np.array([-6 * size, -9 * size, 0]))

        ## 动画

        ## 格子
        self.play(Write(grid_group))
        self.play(GrowFromCenter(line01), GrowFromCenter(line05), GrowFromCenter(line02), GrowFromCenter(line06),
                  GrowFromCenter(line03), GrowFromCenter(line07), GrowFromCenter(line04), GrowFromCenter(line08))

        ## 数字
        self.play(Write(num_group))

        ## 盘面介绍
        self.play(ApplyMethod(sudoku_group.next_to, introdution.get_edge_center(DOWN), DOWN))
        self.play(Write(introdution))
        self.wait(2)

        ## 行
        self.play(Transform(introdution, row_text),
                  ApplyMethod(sudoku_group.next_to, row_text.get_edge_center(RIGHT) + np.array([0, -4 * size, 0]),
                              RIGHT))
        row_highlight(2)

        ## 列
        self.play(Transform(introdution, col_text),
                  ApplyMethod(sudoku_group.next_to, col_text.get_edge_center(DOWN) + np.array([-2 * size, 0, 0]),
                              DOWN))
        col_highlight(5)

        ## 宫
        self.play(Transform(introdution, box_text),
                  ApplyMethod(sudoku_group.next_to, box_text.get_edge_center(UP) + np.array([6 * size, 0, 0]),
                              UP))
        box_highlight(6)

        ## 规则介绍
        self.play(Transform(introdution, rule_title),
                  ApplyMethod(sudoku_group.next_to, rule_title.get_edge_center(DOWN), DOWN))
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
                  ApplyMethod(sudoku_group.next_to, explain_title.get_edge_center(DOWN), DOWN))
        self.wait(2)
        self.play(FadeOut(rule_text03))

        self.play(Write(explain_text01))
        self.wait(1)
        self.play(Transform(explain_text01, explain_text02))
        self.wait(1)
        self.play(Transform(explain_text01, explain_text03))
        self.wait(1)
        row_highlight(3)
        solve(3, 1, 8)
        self.play(FadeOut(explain_text01))

        self.play(Write(explain_text04))
        self.wait(1)
        box_highlight(4)
        solve(4, 4, 3)
        self.play(FadeOut(explain_text04))

        self.play(Write(explain_text05))
        self.wait(1)
        box_highlight(6)
        self.play(Transform(explain_text05, explain_text06))
        self.wait(1)
        self.play(Transform(explain_text05, explain_text07))
        self.wait(1)
        self.play(Transform(explain_text05, explain_text08))
        note(7, 8, 1, 0)
        show()
        solve(6, 1, 1)
        erase()
        self.wait(1)
        self.play(FadeOut(explain_text05))

        self.play(Write(explain_text09))
        self.wait(1)
        box_highlight(5)
        note(7, 7, 2, 1)
        note(1, 6, 2, 0)
        note(5, 0, 1, 1)
        show()
        solve(4, 8, 7)
        erase()

        self.wait(1)
        self.play(Transform(explain_text09, explain_text10))
        box_highlight(6)
        solve(7, 1, 9)

        note(8, 0, 1, 1)
        show()
        box_highlight(8)
        solve(6, 7, 8)
        erase()

        solve(8, 7, 9)

        note(4, 3, 1, 1)
        show()
        col_highlight(6)
        solve(5, 6, 8)
        erase()

        solve(4, 6, 9)

        note(4, 4, 1, 1)
        show()
        box_highlight(5)
        solve(5, 8, 3)
        erase()

        solve(4, 7, 4)

        row_highlight(5)
        solve(5, 1, 4)

        note(0, 1, 2, 0)
        note(6, 0, 2, 1)
        show()
        box_highlight(3)
        solve(4, 2, 6)
        erase()

        note(1, 0, 2, 0)
        show()
        solve(4, 1, 2)
        erase()

        solve(4, 0, 1)

        col_highlight(0)
        solve(0, 0, 4)

        col_highlight(1)
        solve(1, 1, 5)

        col_highlight(2)
        solve(0, 2, 9)

        note(1, 1, 1, 1)
        show()
        col_highlight(7)
        solve(2, 7, 5)
        erase()

        solve(1, 7, 1)

        note(3, 5, 2, 1)
        note(4, 5, 2, 1)
        show()
        row_highlight(0)
        solve(0, 5, 1)
        erase()

        note(0, 5, 2, 0)
        note(4, 5, 2, 0)
        show()
        row_highlight(8)
        solve(8, 5, 2)
        erase()

        note(5, 3, 2, 0)
        show()
        row_highlight(8)
        solve(8, 4, 1)
        erase()

        solve(8, 3, 5)

        note(8, 3, 2, 1)
        show()
        row_highlight(0)
        solve(0, 4, 5)
        erase()

        solve(0, 3, 7)

        note(0, 3, 2, 0)
        show()
        row_highlight(6)
        solve(6, 4, 7)
        erase()

        solve(6, 3, 9)

        note(3, 3, 2, 1)
        note(8, 5, 2, 1)
        note(1, 0, 1, 1)
        show()
        box_highlight(1)
        solve(2, 4, 2)
        erase()

        note(1, 2, 1, 1)
        show()
        col_highlight(4)
        solve(7, 4, 8)
        erase()

        solve(1, 4, 9)

        note(1, 4, 1, 1)
        show()
        col_highlight(8)
        solve(2, 8, 9)
        erase()

        solve(1, 8, 4)

        note(4, 3, 2, 1)
        show()
        row_highlight(2)
        solve(2, 5, 8)
        erase()

        solve(2, 3, 4)

        note(1, 8, 1, 0)
        show()
        col_highlight(5)
        solve(7, 5, 4)
        erase()

        solve(1, 5, 6)

        box_highlight(1)
        solve(1, 3, 3)

        box_highlight(7)
        solve(7, 3, 6)

        self.wait(1)
        self.play(Transform(explain_text09, explain_text11))
        self.wait(1)
        self.play(FadeOut(explain_text09))

        self.play(Transform(sudoku_group, thanks_text))
        self.wait(1)
        self.play(Transform(sudoku_group, name_text))
        self.wait(1)
