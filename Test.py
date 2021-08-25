# -*- coding=utf-8 -*-

from manimlib.imports import *
from sudoku import *


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
        # self.play(Write(Sudoku1.cands_group))

        self.play(Write(Sudoku1[0]))
        self.play(Write(Sudoku1[1]))
        self.play(Write(Sudoku1[2]))
        Sudoku1.save_state()
        self.play(FadeOutWithParticles(Sudoku1.cands_group[1], run_time=6),
                  FadeOutWithParticles(Sudoku1.cands_group[5], parti_color=PINK)
                  , FadeOutWithParticles(Sudoku1.cands_group[10], parti_color=YELLOW_B, squares=10))

        self.play(Sudoku1.cands_group[1].set_opacity, 1)
        self.play(Sudoku1.shift, RIGHT * 3)
        wave(self, Sudoku1.squares[15])
        self.play(Sudoku1.scale, 0.5)
        self.play(Sudoku1.restore)

        self.play(Sudoku1[0].set_colors_by_radial_gradient,
                  {'radius': 3.5, 'inner_color': YELLOW_B, 'outer_color': BLUE_B})
        Sudoku3 = Sudoku1.copy()

        # self.play(Sudoku1.scale,0.5)
        Sudoku2 = Sudoku(num_str='1.92...4.67.9.8....85......7..15.......8.7.......69..5......27....7.4.36.5...64.1',
                         center_of_squares=[3, 0], square_color=YELLOW_B)
        self.play(Transform(Sudoku1, Sudoku2))
        self.wait(3)
        self.play(Transform(Sudoku1, Sudoku3))
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
        Sl1 = SquareLoop(color=PURPLE)
        self.play(Write(Sl1))


class TestScene2(Scene):
    def construct(self):
        self.num_str = '1..4..6..2..1.....5...7..9.......9.8....647.........5.62...3..443.85..6...9..1..7'
        temp = SudokuLine(self.num_str[9 * 1 + 1 - 10], color=ORANGE,
                          plot_depth=2, size=1)
        self.play(Write(temp))


class TestScene3(Scene):
    def construct(self):
        title = Title("候选数初步.....", match_underline_width_to_text=True).move_to(UP * 2.5)
        contents = BulletedList(
            "唯余",
            "区块排除",
            "死锁/互补思路",
            "数对数组（显性隐性）",
            "两种流派的辨析"
        ).next_to(title, DOWN)

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
        hidden_subset = TextMobject("隐性数组", plot_depth=2, background_stroke_color=WHITE)
        self.play(ShowCreation(hidden_subset))

        # 这里是文字的背景矩形
        # hidden_subset.add_background_rectangle(opacity=0)
        hidden_subset.add_background_rectangle()
        hidden_subset.background_rectangle.set_opacity(0)
        rectangle = hidden_subset.background_rectangle.copy()
        # 把矩形不透明度改为1，
        rectangle.shift(LEFT * 3 + UP * 0.1).set_plot_depth(1).set_fill(color=BLUE)
        rectangle.set_opacity(1)

        # 下面是将最终位置变到文字所在处的动画（关系不大）
        self.play(FadeIn(rectangle))
        self.play(rectangle.shift, RIGHT * 2)
        self.play(rectangle.shift, RIGHT * 2 + DOWN * 0.5)
        self.play(rectangle.move_to, hidden_subset.get_center())
        self.wait()


class TestScene5(Scene):
    # CONFIG = {
    #     "camera_config": {
    #         "background_color": WHITE,
    #     },
    # }
    def construct(self):
        text = Text("1234", plot_depth=1)
        square = Square(fill_color=BLUE, fill_opacity=1, stroke_color=RED)
        self.play(FadeIn(text))
        self.play(FadeIn(square))
        self.wait()
        self.play(FadeIn(text))
        print(text.get_plot_depth(), square.get_plot_depth())
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

        sudoku1 = Sudoku(num_str='1..4..6..2..1.....5...7..9.......9.8....647.........5.62...3..443.85..6...9..1..7',
                         center_of_squares=3.5 * LEFT)
        self.play(Write(sudoku1))
        sudoku2 = Sudoku(num_str='.314...78...1.........6...34....1.3..7.6.9.5..2.3....97...2.........6...69...542.',
                         center_of_squares=3.5 * RIGHT)
        self.play(Write(sudoku2))
        self.wait(1)
        self.play(sudoku1.cands_group.shift, RIGHT)


class TestScene7(Scene):
    def construct(self):
        sudoku1 = Sudoku(num_str='1..4..6..2..1.....5...7..9.......9.8....647.........5.62...3..443.85..6...9..1..7',
                         center_of_squares=3.5 * LEFT)
        sudoku1.save_state(use_deepcopy=True)
        print("original")
        print(sudoku1.side_lenth_of_squares)

        print(sudoku1.scale, 0.5)
        sudoku1.change_scale(0.5)
        print("Scale()")
        print(sudoku1.side_lenth_of_squares)
        self.play(sudoku1.restore)
        print("restore()")
        print(sudoku1.side_lenth_of_squares)
        sudoku1.restore()
        print("restore()")
        print(sudoku1.side_lenth_of_squares)


class TestScene7(Scene):
    CONFIG = {
        "camera_config": {
            "background_color": WHITE,
        },
    }

    def construct(self):
        sudoku1 = Sudoku(num_str='.37658..4....34.764..1.75.32..3.5..88.......55..8.6..16.84.2..734.76....7..58346.',
                         center_of_squares=3.5 * LEFT)
        sudoku1.save_state()
        self.play(FadeIn(sudoku1))
        self.play(FadeOut(sudoku1.remove_cand([
            [1, 1, 9],
            [2, 2, 1],
            [2, 2, 2],
            [2, 2, 5],
            [2, 2, 8],
        ])))
        print(sudoku1.domain_cands_list[1 * 9 + 1 - 10])
        print(sudoku1.domain_cands_list[2 * 9 + 2 - 10])
        self.wait()


class TestScene8(Scene):
    CONFIG = {
        "camera_config": {
            "background_color": WHITE,
        },
    }

    def construct(self):
        sudoku = Sudoku(num_str='.37658..4....34.764..1.75.32..3.5..88.......55..8.6..16.84.2..734.76....7..58346.',
                        center_of_squares=3.5 * LEFT)

        def symmetry_group(sudoku):
            square_group = VGroup()
            all_group = VGroup()
            for i in [
                0, 1, 2, 3, 4, 5, 6, 7, 8,
                17, 26, 35, 44, 53, 62, 71,
                70, 69, 68, 67, 66, 65, 64,
                55, 46, 37, 28, 19,
                20, 21, 22, 23, 24,
                33, 42, 51,
                50, 49, 48,
                39,
                40
            ]:
                all_group.add(sudoku.nums_list[i].save_state(), sudoku.nums_list[80 - i].save_state())
                if (sudoku.domain_nums_list[i] != 0):
                    square_group.add(sudoku.nums_list[i], sudoku.nums_list[80 - i])
            return all_group, square_group

        self.play(FadeIn(sudoku))
        self.wait()
        all_group, square_group = symmetry_group(sudoku)
        square_group.save_state()

        self.play(
            AnimationGroup(*[ApplyMethod(obj.set_color, YELLOW) for obj in square_group], lag_ratio=0.1, run_time=3))
        self.wait()

        self.play(*[obj.restore for obj in square_group])
        self.wait()


class TestScene9(Scene):
    CONFIG = {
        "camera_config": {
            "background_color": WHITE,
        },
    }

    def construct(self):
        sudoku = Sudoku(center_of_squares=0.2 * UP,
                        num_str='.37658..4....34.764..1.75.32..3.5..88.......55..8.6..16.84.2..734.76....7..58346.')
        self.play(FadeIn(sudoku))

        def color_num(sudoku):
            for i in range(81):
                sudoku.nums_list[i].generate_target()
                if (sudoku.domain_nums_list[i] == 1 or sudoku.domain_nums_list[i] == 2):
                    sudoku.nums_list[i].target.set_color(MAROON_B)
                if (sudoku.domain_nums_list[i] == 3 or sudoku.domain_nums_list[i] == 6):
                    sudoku.nums_list[i].target.set_color(RED)
                if (sudoku.domain_nums_list[i] == 4 or sudoku.domain_nums_list[i] == 7):
                    sudoku.nums_list[i].target.set_color(ORANGE)
                if (sudoku.domain_nums_list[i] == 5 or sudoku.domain_nums_list[i] == 8):
                    sudoku.nums_list[i].target.set_color(GOLD_B)
                if (sudoku.domain_nums_list[i] == 9):
                    sudoku.nums_list[i].target.set_color(YELLOW)

        sudoku.save_state()
        color_num(sudoku)
        self.play(AnimationGroup(
            *[
                MoveToTarget(sudoku.nums_list[i])
                for i in [
                    0, 1, 2, 3, 4, 5, 6, 7, 8,
                    17, 26, 35, 44, 53, 62, 71,
                    70, 69, 68, 67, 66, 65, 64,
                    55, 46, 37, 28, 19,
                    20, 21, 22, 23, 24,
                    33, 42, 51,
                    50, 49, 48,
                    39,
                    40
                ]
            ], lag_ratio=0.1),
            AnimationGroup(
                *[
                    MoveToTarget(sudoku.nums_list[80 - i])
                    for i in [
                        0, 1, 2, 3, 4, 5, 6, 7, 8,
                        17, 26, 35, 44, 53, 62, 71,
                        70, 69, 68, 67, 66, 65, 64,
                        55, 46, 37, 28, 19,
                        20, 21, 22, 23, 24,
                        33, 42, 51,
                        50, 49, 48,
                        39,
                        40
                    ]
                ], lag_ratio=0.1),
            run_time=3
        )

        num, cand = sudoku.solve([5, 5, 9], update_board=False)
        num.set_color(YELLOW)
        self.play(
            cand.set_opacity, 0,
            *[
                Write(obj)
                for obj in num
            ]
        )
        self.wait(5)


class TestScene10(Scene):
    CONFIG = {
        "camera_config": {
            "background_color": WHITE,
        },
    }

    def construct(self):
        sudoku = Sudoku(center_of_squares=0.2 * UP,
                        num_str='1...5...2.2...93....37...1...4...2678.....534.6....891.3.2851....1936.2.2..471..3')
        self.play(FadeIn(sudoku))

        def animSudokuFlip1(obj, alpha):
            obj.restore()
            obj.rotate(-alpha * PI, axis=DR)
            for i in range(81):
                VGroup(*obj.cands_list[i]).rotate(alpha * PI, axis=DR)
            for i in range(81):
                obj.nums_list[i].rotate(alpha * PI, axis=DR)

        sudoku.save_state()
        self.play(UpdateFromAlphaFunc(sudoku, animSudokuFlip1),
                  run_time=6,
                  rate_func=smooth,
                  lag_ratio=0.2)
        self.wait(5)

        def animSudokuFlip2(obj, alpha):
            obj.restore()
            obj.rotate(-alpha * PI, axis=UP)
            for i in range(81):
                VGroup(*obj.cands_list[i]).rotate(alpha * PI, axis=UP)
            for i in range(81):
                obj.nums_list[i].rotate(alpha * PI, axis=UP)

        sudoku.restore()
        self.play(UpdateFromAlphaFunc(sudoku, animSudokuFlip2),
                  run_time=6,
                  rate_func=smooth,
                  lag_ratio=0.2)
        self.wait(5)


class TestScene11(Scene):
    CONFIG = {
        "camera_config": {
            "background_color": WHITE,
        },
    }

    def construct(self):

        sudoku4 = Sudoku(num_str='1...5...2.2...93....37...1...4...2678.....534.6....891.3.2851....1936.2.2..471..3')

        self.play(FadeIn(sudoku4))

        def color_num2(sudoku):
            for i in range(81):
                sudoku.nums_list[i].generate_target()
                if (sudoku.domain_nums_list[i] == 6 or sudoku.domain_nums_list[i] == 9):
                    sudoku.nums_list[i].target.set_color(RED)
                if (sudoku.domain_nums_list[i] == 4
                        or sudoku.domain_nums_list[i] == 7):
                    sudoku.nums_list[i].target.set_color(ORANGE)
                if (sudoku.domain_nums_list[i] == 5
                        or sudoku.domain_nums_list[i] == 8):
                    sudoku.nums_list[i].target.set_color(GOLD_B)
                if (sudoku.domain_nums_list[i] == 1
                        or sudoku.domain_nums_list[i] == 2
                        or sudoku.domain_nums_list[i] == 3):
                    sudoku.nums_list[i].target.set_color(YELLOW)

        sudoku4.save_state()
        color_num2(sudoku4)
        self.play(AnimationGroup(
            *[
                MoveToTarget(sudoku4.nums_list[i])
                for i in [
                    0,
                    1,
                    10, 2,
                    11, 3,
                    20, 12, 4,
                    21, 13, 5,
                    30, 22, 14, 6,
                    31, 23, 15, 7,
                    40, 32, 24, 16, 8,
                    41, 33, 25, 17,
                    50, 42, 34, 26,
                    51, 43, 35,
                    60, 52, 44,
                    61, 53,
                    70, 62,
                    71,
                    80
                ]
            ], lag_ratio=0.1),
            AnimationGroup(
                *[
                    MoveToTarget(sudoku4.nums_list[i])
                    for i in [
                        0,
                        9,
                        10, 18,
                        19, 27,
                        20, 28, 36,
                        29, 37, 45,
                        30, 38, 46, 54,
                        39, 47, 55, 63,
                        40, 48, 56, 64, 72,
                        49, 57, 65, 73,
                        50, 42, 34, 26,
                        59, 67, 75,
                        60, 68, 76,
                        69, 77,
                        70, 78,
                        79,
                        80
                    ]
                ], lag_ratio=0.1),
            run_time=3
        )
        self.wait(1)


class TestScene12(Scene):
    CONFIG = {
        "camera_config": {
            "background_color": WHITE,
        },
    }

    def construct(self):
        self.play(Write(SudokuLine("感 谢 观 看", size=3)))
        self.wait()


class TestScene13(Scene):
    CONFIG = {
        "camera_config": {
            "background_color": WHITE,
        },
    }

    def construct(self):
        sudoku = Sudoku(num_str='.37658..4....34.764..1.75.32..3.5..88.......55..8.6..16.84.2..734.76....7..58346.')
        self.play(FadeIn(sudoku))

        def color_num1(sudoku):
            for i in range(81):
                sudoku.nums_list[i].generate_target()
                if (sudoku.domain_nums_list[i] == 1 or sudoku.domain_nums_list[i] == 2):
                    sudoku.nums_list[i].target.set_color(MAROON_B)
                if (sudoku.domain_nums_list[i] == 3 or sudoku.domain_nums_list[i] == 6):
                    sudoku.nums_list[i].target.set_color(RED)
                if (sudoku.domain_nums_list[i] == 4 or sudoku.domain_nums_list[i] == 7):
                    sudoku.nums_list[i].target.set_color(ORANGE)
                if (sudoku.domain_nums_list[i] == 5 or sudoku.domain_nums_list[i] == 8):
                    sudoku.nums_list[i].target.set_color(GOLD_B)
                if (sudoku.domain_nums_list[i] == 9):
                    sudoku.nums_list[i].target.set_color(YELLOW)

        sudoku.save_state()
        color_num1(sudoku)
        self.play(AnimationGroup(
            *[
                MoveToTarget(sudoku.nums_list[i])
                for i in [
                    0, 1, 2, 3, 4, 5, 6, 7, 8,
                    17, 26, 35, 44, 53, 62, 71,
                    70, 69, 68, 67, 66, 65, 64,
                    55, 46, 37, 28, 19,
                    20, 21, 22, 23, 24,
                    33, 42, 51,
                    50, 49, 48,
                    39,
                    40
                ]
            ], lag_ratio=0.1),
            AnimationGroup(
                *[
                    MoveToTarget(sudoku.nums_list[80 - i])
                    for i in [
                        0, 1, 2, 3, 4, 5, 6, 7, 8,
                        17, 26, 35, 44, 53, 62, 71,
                        70, 69, 68, 67, 66, 65, 64,
                        55, 46, 37, 28, 19,
                        20, 21, 22, 23, 24,
                        33, 42, 51,
                        50, 49, 48,
                        39,
                        40
                    ]
                ], lag_ratio=0.1),
            run_time=3
        )
        self.wait(1)


class TestScene14(Scene):
    CONFIG = {
        "camera_config": {
            "background_color": WHITE,
        },
    }

    def construct(self):
        sudoku4 = Sudoku(num_str='1...5...2.2...93....37...1...4...2678.....534.6....891.3.2851....1936.2.2..471..3')
        self.play(FadeIn(sudoku4))

        def color_num2(sudoku):
            for i in range(81):
                sudoku.nums_list[i].generate_target()
                if (sudoku.domain_nums_list[i] == 6 or sudoku.domain_nums_list[i] == 9):
                    sudoku.nums_list[i].target.set_color(RED)
                if (sudoku.domain_nums_list[i] == 4
                        or sudoku.domain_nums_list[i] == 7):
                    sudoku.nums_list[i].target.set_color(ORANGE)
                if (sudoku.domain_nums_list[i] == 5
                        or sudoku.domain_nums_list[i] == 8):
                    sudoku.nums_list[i].target.set_color(GOLD_B)
                if (sudoku.domain_nums_list[i] == 1
                        or sudoku.domain_nums_list[i] == 2
                        or sudoku.domain_nums_list[i] == 3):
                    sudoku.nums_list[i].target.set_color(YELLOW)

        sudoku4.save_state()
        color_num2(sudoku4)
        self.play(AnimationGroup(
            *[
                MoveToTarget(sudoku4.nums_list[i])
                for i in [
                    0,
                    1,
                    10, 2,
                    11, 3,
                    20, 12, 4,
                    21, 13, 5,
                    30, 22, 14, 6,
                    31, 23, 15, 7,
                    40, 32, 24, 16, 8,
                    41, 33, 25, 17,
                    50, 42, 34, 26,
                    51, 43, 35,
                    60, 52, 44,
                    61, 53,
                    70, 62,
                    71,
                    80
                ]
            ], lag_ratio=0.1),
            AnimationGroup(
                *[
                    MoveToTarget(sudoku4.nums_list[i])
                    for i in [
                        0,
                        9,
                        10, 18,
                        19, 27,
                        20, 28, 36,
                        29, 37, 45,
                        30, 38, 46, 54,
                        39, 47, 55, 63,
                        40, 48, 56, 64, 72,
                        49, 57, 65, 73,
                        50, 58, 66, 74,
                        59, 67, 75,
                        60, 68, 76,
                        69, 77,
                        70, 78,
                        79,
                        80
                    ]
                ], lag_ratio=0.1),
            run_time=3
        )
        self.wait(1)


class CodeLine(Text):
    CONFIG = {
        't2c': {
            '~': WHITE
        },
        'font': '庞门正道标题体',
        'size': 0.36,
        'color': DARK_GRAY,
        'plot_depth': 2,
    }

    def __init__(self, text, **kwargs):
        Text.__init__(self, text, **kwargs)


class TestScene15(Scene):
    CONFIG = {
        "camera_config": {
            "background_color": WHITE,
        },
    }

    def construct(self):
        title = CodeLine("参 考 资 料", size=2).to_edge(UP, buff=0.9)

        captions = [
            "[1] SunnieShine的标准数独技巧教程文档（2020.7.1版本）",
            "    https://share.weiyun.com/XiFZVXZ0",

            "[2] The Riddle of Sho : Advanced solving techniques ",
            "    http://forum.enjoysudoku.com/the-riddle-of-sho-t4392.html",

            "[3] 数独吧——利用对称性，把骨灰题难度降为直观可解",
            "    https://tieba.baidu.com/p/5008085327?red_tag=3031462126",

            "[4] Hodoku",
            "    http://hodoku.sourceforge.net/en/",

        ]
        cap_mob = VGroup(
            *[
                CodeLine(cap, size=0.8)
                for cap in captions
            ]
        ).arrange(DOWN).next_to(title, DOWN, buff=0.5)

        for cap in cap_mob:
            cap.to_edge(LEFT, buff=1.5)

        self.play(FadeIn(title))
        self.play(FadeIn(cap_mob))
        self.wait(2)
        self.play(FadeOut(VGroup(title,cap_mob)))

        title = CodeLine("特 别 感 谢", size=2).to_edge(UP, buff=0.9)

        captions = [
            "@tucoconum 贡献的基础代码",
            "~",
            "@15162428 的配音和字幕",
            "~",
            "@SunnieShine 的指点",
            "~",
            "以及,所有给予过支持和鼓励的朋友",


        ]
        cap_mob = VGroup(
            *[
                CodeLine(cap, size=0.8)
                for cap in captions
            ]
        ).arrange(DOWN).next_to(title, DOWN, buff=1)

        for cap in cap_mob:
            cap.to_edge(LEFT, buff=3.5)

        self.play(FadeIn(title))
        self.play(FadeIn(cap_mob))
        self.wait(2)
        self.play(FadeOut(VGroup(title,cap_mob)))