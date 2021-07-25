# -*- coding=utf-8 -*-

from manimlib.imports import*
from sudoku import*


class TestScene(Scene):
    CONFIG = {
        "camera_config": {
            "background_color": WHITE,
        },
    }

    def construct(self):
        Sudoku1 = Sudoku(num_str='..6...72.43......6.5.9.2.....1549...8.......5...8213.....1.7.5.5......39.83...4..')
        self.wait()
        # self.play(Write(Sudoku1.squares))
        # self.play(Write(Sudoku1.nums))
        # self.play(Write(Sudoku1.cands))

        self.play(Write(Sudoku1[0]))
        self.play(Write(Sudoku1[1]))
        self.play(Write(Sudoku1[2]))
        Sudoku1.save_state()
        self.play(FadeOutWithParticles(Sudoku1.cands[1],run_time=6),FadeOutWithParticles(Sudoku1.cands[5],parti_color=PINK)
                  ,FadeOutWithParticles(Sudoku1.cands[10],parti_color=YELLOW_B,squares=10))

        self.play(Sudoku1.cands[1].set_opacity,1)
        self.play(Sudoku1.shift,RIGHT*3)
        wave(self, Sudoku1.squares[15])
        self.play(Sudoku1.scale,0.5)
        self.play(Sudoku1.restore)

        self.play(Sudoku1[0].set_colors_by_radial_gradient,
                  {'radius': 3.5, 'inner_color': YELLOW_B, 'outer_color': BLUE_B})
        Sudoku3=Sudoku1.copy()

        # self.play(Sudoku1.scale,0.5)
        Sudoku2 = Sudoku(num_str='1.92...4.67.9.8....85......7..15.......8.7.......69..5......27....7.4.36.5...64.1',
                         center_of_squares=[3, 0],square_color=YELLOW_B)
        self.play(Transform(Sudoku1,Sudoku2))
        self.wait(3)
        self.play(Transform(Sudoku1,Sudoku3))
        self.wait()

        # self.play(FadeOut(Sudoku1))
        # Sudoku2=Sudoku1.copy()
        # Sudoku2.shift(RIGHT*2)
        # self.play(Write(Sudoku1))
        # self.play(Write(Sudoku2))

class TestScene1(Scene):
    CONFIG = {
        "camera_config": {
            "background_color": WHITE,
        },
    }
    def construct(self):
        Sl1=SquareLoop(color=PURPLE)
        self.play(Write(Sl1))


class TestScene2(Scene):
    def construct(self):
        self.num_str='1..4..6..2..1.....5...7..9.......9.8....647.........5.62...3..443.85..6...9..1..7'
        temp = SudokuLine(self.num_str[9 * 1 + 1 - 10], color=ORANGE,
                          plot_depth=2, size=1)
        self.play(Write(temp))


class TestScene3(Scene):
    def construct(self):
        title=Title("候选数初步.....",match_underline_width_to_text=True).move_to(UP*2.5)
        contents=BulletedList(
                "唯余",
                "区块排除",
                "死锁/互补思路",
                "数对数组（显性隐性）",
                "两种流派的辨析"
        ).next_to(title,DOWN)

        title.set_color(WHITE)
        self.wait()
        self.play(Write(title))
        self.wait()
        self.play(Write(contents))

class TestScene4(Scene):
    CONFIG = {
        "camera_config": {
            "background_color": WHITE,
        },
    }
    def construct(self):
        # 这里是要显示的文字
        hidden_subset=TextMobject("隐性数组",plot_depth=2,background_stroke_color=WHITE)
        self.play(ShowCreation(hidden_subset))

        # 这里是文字的背景矩形
        # hidden_subset.add_background_rectangle(opacity=0)
        hidden_subset.add_background_rectangle()
        hidden_subset.background_rectangle.set_opacity(0)
        rectangle= hidden_subset.background_rectangle.copy()
        # 把矩形不透明度改为1，
        rectangle.shift(LEFT*3+UP*0.1).set_plot_depth(1).set_fill(color=BLUE)
        rectangle.set_opacity(1)

        # 下面是将最终位置变到文字所在处的动画（关系不大）
        self.play(FadeIn(rectangle))
        self.play(rectangle.shift,RIGHT*2)
        self.play(rectangle.shift,RIGHT*2+DOWN*0.5)
        self.play(rectangle.move_to,hidden_subset.get_center())
        self.wait()

class TestScene5(Scene):
    # CONFIG = {
    #     "camera_config": {
    #         "background_color": WHITE,
    #     },
    # }
    def construct(self):
        text=Text("1234",plot_depth=1)
        square=Square(fill_color=BLUE,fill_opacity=1,stroke_color=RED)
        self.play(FadeIn(text))
        self.play(FadeIn(square))
        self.wait()
        self.play(FadeIn(text))
        print(text.get_plot_depth(),square.get_plot_depth())
        self.wait()

class TestScene6(Scene):
    CONFIG = {
        "camera_config": {
            "background_color": GRAY,
        },
    }
    def construct(self):
        print(Sudoku.rows_index_list)
        print(Sudoku.cols_index_list)
        print(Sudoku.blocks_index_list)
        print(Sudoku.except_list)

        sudoku1 = Sudoku(num_str = '1..4..6..2..1.....5...7..9.......9.8....647.........5.62...3..443.85..6...9..1..7',center_of_squares=3.5*LEFT)
        self.play(Write(sudoku1))
        sudoku2 = Sudoku(num_str='.314...78...1.........6...34....1.3..7.6.9.5..2.3....97...2.........6...69...542.',center_of_squares=3.5*RIGHT)
        self.play(Write(sudoku2))
        self.wait(1)
        self.play(sudoku1.init_cands.shift,RIGHT)


