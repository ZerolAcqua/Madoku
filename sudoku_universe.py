# -*- coding=utf-8 -*-

from manimlib.imports import *
from mydemo.Madoku.package_color import *
from mydemo.Madoku.package_motion import *
from sudoku import *


class SudokuScene(Scene):
    CONFIG = {
        "camera_config": {
            "background_color": WHITE,
        },
    }

    def construct(self):
        pass

    def 各种动画函数(self, 其他可能的参数):
        pass

    @staticmethod
    def 各种对数独进行基本操作的函数(Sudoku, 其他参数):
        pass


class SudokuUniverseScene(SudokuScene):
    def construct(self):
        # 标题
        title = list()
        title = [
            ImageMobject("宇1.png").scale(0.5).shift(UP * 0 + LEFT * 2.5).set_color(ORANGE),
            ImageMobject("宇2.png").scale(0.5).shift(UP * 0 + LEFT * 2.5).set_color(ORANGE),
            ImageMobject("宙1.png").scale(0.5).shift(UP * 0).set_color(ORANGE),
            ImageMobject("宙2.png").scale(0.5).shift(UP * 0).set_color(ORANGE),
            ImageMobject("法1.png").scale(0.5).shift(UP * 0 + RIGHT * 2.5).set_color(ORANGE),
            ImageMobject("法2.png").scale(0.5).shift(UP * 0 + RIGHT * 2.5).set_color(ORANGE)
        ]

        title[0].save_state()
        title[1].save_state()

        def anim1(obj, alpha):
            obj.restore()
            obj.rotate((1 - alpha) * PI)
            obj.set_color(interpolate_color(WHITE, ORANGE, alpha))

        def anim2(obj, alpha):
            obj.restore()
            obj.rotate(-(1 - alpha) * PI)
            obj.set_color(interpolate_color(WHITE, ORANGE, alpha))

        self.play(
            LaggedStart(AnimationGroup(UpdateFromAlphaFunc(title[0], anim1), UpdateFromAlphaFunc(title[1], anim2)),
                        AnimationGroup(FadeInFrom(title[2], DL), FadeInFrom(title[3], UR)),
                        AnimationGroup(FadeInFrom(title[4], DR), FadeInFrom(title[5], UL)),
                        run_time=4,
                        rate_func=rush_into,
                        lag_ratio=0.2))
        self.wait(0.5)

        self.play(FadeOut(title[0]),
                  FadeOut(title[1]),
                  FadeOut(title[2]),
                  FadeOut(title[3]),
                  FadeOut(title[4]),
                  FadeOut(title[5]))

        self.wait(0.5)

        sudoku = Sudoku(center_of_squares=3.5 * LEFT,
                        num_str='.37658..4....34.764..1.75.32..3.5..88.......55..8.6..16.84.2..734.76....7..58346.')
        self.play(Write(sudoku))
        self.wait(0.5)

        sudoku1 = sudoku.deepcopy()
        sudoku1.save_state()

        def animSudokuRotation(obj, alpha):
            obj.restore()
            obj.rotate(alpha * PI)
            obj.shift(7 * alpha * RIGHT)
            for i in range(81):
                VGroup(*obj.init_cands_list[i]).rotate(-alpha * PI)
            for i in range(81):
                obj.nums_list[i].rotate(-alpha * PI)

        self.play(UpdateFromAlphaFunc(sudoku1, animSudokuRotation),
                  run_time=6,
                  rate_func=smooth,
                  lag_ratio=0.2)

        self.wait()
