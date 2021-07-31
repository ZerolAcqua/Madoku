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
        dt = 1 / self.camera.frame_rate

        # 字幕等讲解内容
        captions = [
            "这是一个数独",
            "在HoDoKu中的难度为Unfair",
            "通常要使用到不少的技巧才能解出",
            "一通操作后，难度降至164",
            "但今天要讲解的神奇方法……",
            "一着即可将此题解决"
        ]
        captions_mob = VGroup(
            *[
                SudokuLine(cap, font='站酷小薇LOGO体', size=1)
                for cap in captions
            ]
        )
        for i in range(6):
            captions_mob[i].to_edge(DOWN * 0.7)

        # 一些讲解标注用的东西
        explains = [
            "rating: ",
            "Unfair",
            "区块",
            "数对",
            "标准链",
            "Easy",
            "宇宙法",
            "Gurth's Symmetrical",
            "Placement",
        ]
        explains_mob = VGroup(
            *[
                SudokuLine(exp, font='站酷小薇LOGO体', size=1)
                for exp in explains
            ]
        )
        explains_mob[0].move_to(RIGHT * 2)
        explains_mob[1].next_to(explains_mob, RIGHT)
        explains_mob[2].move_to(RIGHT * 3.5)
        explains_mob[3].move_to(RIGHT * 3.5)
        explains_mob[4].move_to(RIGHT * 3.5 + DOWN)
        explains_mob[5].move_to(RIGHT * 2.5)
        explains_mob[6].move_to(RIGHT * 3.5 + UP * 0.5).set_color(ORANGE)
        explains_mob[7].next_to(explains_mob[6], DOWN).set_color(ORANGE)
        explains_mob[8].next_to(explains_mob[7], DOWN).set_color(ORANGE)

        number = SudokuLine('0')

        # 标题
        title = list()
        title = [
            ImageMobject("宇1.png").scale(0.5).shift(UP * 0.5 + LEFT * 2.5).set_color(ORANGE),
            ImageMobject("宇2.png").scale(0.5).shift(UP * 0.5 + LEFT * 2.5).set_color(ORANGE),
            ImageMobject("宙1.png").scale(0.5).shift(UP * 0.5).set_color(ORANGE),
            ImageMobject("宙2.png").scale(0.5).shift(UP * 0.5).set_color(ORANGE),
            ImageMobject("法1.png").scale(0.5).shift(UP * 0.5 + RIGHT * 2.5).set_color(ORANGE),
            ImageMobject("法2.png").scale(0.5).shift(UP * 0.5 + RIGHT * 2.5).set_color(ORANGE)
        ]

        title[0].save_state()
        title[1].save_state()

        def title_anim1(obj, alpha):
            obj.restore()
            obj.rotate((1 - alpha) * PI)
            obj.set_color(interpolate_color(WHITE, ORANGE, alpha))

        def title_anim2(obj, alpha):
            obj.restore()
            obj.rotate(-(1 - alpha) * PI)
            obj.set_color(interpolate_color(WHITE, ORANGE, alpha))

        self.play(
            LaggedStart(
                AnimationGroup(UpdateFromAlphaFunc(title[0], title_anim1), UpdateFromAlphaFunc(title[1], title_anim2)),
                AnimationGroup(FadeInFrom(title[2], DL), FadeInFrom(title[3], UR)),
                AnimationGroup(FadeInFrom(title[4], DR), FadeInFrom(title[5], UL)),
                run_time=4,
                rate_func=rush_into,
                lag_ratio=0.2))
        self.wait(0.5)

        # 标题淡出
        self.play(FadeOut(title[0]),
                  FadeOut(title[1]),
                  FadeOut(title[2]),
                  FadeOut(title[3]),
                  FadeOut(title[4]),
                  FadeOut(title[5]))

        self.wait(0.5)

        # 数独显示
        sudoku = Sudoku(center_of_squares=2.5 * LEFT + 0.2 * UP,
                        num_str='.37658..4....34.764..1.75.32..3.5..88.......55..8.6..16.84.2..734.76....7..58346.')
        self.play(Write(sudoku))
        self.wait(0.5)

        self.play(FadeInFromDown(captions_mob[0]))
        self.wait()

        # Unfair 1044
        def difficulty_anim1(obj, alpha):
            obj.become(SudokuLine(str(round(1104 * alpha)), font='ZCOOL Addict Italic 01', size=1))
            obj.next_to(VGroup(*explains_mob[0:2])).shift(0.05 * UP)
            obj.set_color(interpolate_color(GREY_BROWN, RED, alpha))

        self.play(FadeOutAndShift(captions_mob[0], direction=UP),
                  FadeInFromDown(captions_mob[1]),
                  FadeIn(VGroup(*explains_mob[0:2])),
                  UpdateFromAlphaFunc(number, difficulty_anim1))
        self.wait()

        # 通常要使用到不少的技巧才能解出
        self.play(FadeOutAndShift(captions_mob[1], direction=UP),
                  FadeInFromDown(captions_mob[2]),
                  ApplyMethod(VGroup(VGroup(*explains_mob[0:2]), number).shift, 2.5 * UP))
        explains_mob[5].next_to(explains_mob[0], RIGHT)
        self.wait()

        # 常规解法演示
        # 用于标注的两个函数
        def SetNote(note_group, unit_cands_list):
            for i in unit_cands_list:
                circle = Circle(stroke_color=WHITE,
                                stroke_opacity=0.8,
                                stroke_width=2,
                                fill_color=GREEN,
                                fill_opacity=0.5,
                                arc_center=sudoku.unit_cand(*i).get_center(),
                                radius=sudoku.cand_scale * 0.25
                                )
                note_group.add(circle)

        def SetDelete(delete_group, unit_cands_list):
            for i in unit_cands_list:
                circle = Circle(stroke_color=WHITE,
                                stroke_opacity=0.8,
                                stroke_width=2,
                                fill_color=RED,
                                fill_opacity=0.5,
                                arc_center=sudoku.unit_cand(*i).get_center(),
                                radius=sudoku.cand_scale * 0.25
                                )
                delete_group.add(circle)

        def FlashFade(group):
            self.play(
                *[
                    Flash(obj, color=PURPLE, flash_radius=0.5)
                    for obj in group
                ],
                *[
                    ApplyMethod(obj.set_opacity, 0)
                    for obj in group
                ]
            )

        sudoku.save_state()
        # 区块
        self.play(FadeIn(explains_mob[2]))
        self.wait()
        # 简易的区块摒除1
        self.play(ShowPassingFlashAround(VGroup(*sudoku.blocks_list[2])))
        note_group = VGroup()
        delete_group = VGroup()
        unit_cands_list = [
            [1, 7, 2],
            [1, 8, 2],
        ]
        SetNote(note_group, unit_cands_list)
        unit_cands_list = [
            [2, 7, 2],
            [3, 8, 2],
        ]
        SetDelete(delete_group, unit_cands_list)
        self.play(FadeIn(VGroup(note_group, delete_group)))
        FlashFade(VGroup(
            sudoku.unit_cand(2, 7, 2),
            sudoku.unit_cand(3, 8, 2)
        ))
        self.play(FadeOut(VGroup(note_group, delete_group)))
        # 简易的区块摒除2
        self.play(ShowPassingFlashAround(VGroup(*sudoku.blocks_list[6])))
        note_group = VGroup()
        delete_group = VGroup()
        unit_cands_list = [
            [9, 2, 1],
            [9, 3, 1],
        ]
        SetNote(note_group, unit_cands_list)
        unit_cands_list = [
            [7, 2, 1],
            [8, 3, 1],
        ]
        SetDelete(delete_group, unit_cands_list)
        self.play(FadeIn(VGroup(note_group, delete_group)))
        FlashFade(VGroup(
            sudoku.unit_cand(7, 2, 1),
            sudoku.unit_cand(8, 3, 1)
        ))
        self.play(FadeOut(VGroup(note_group, delete_group)))

        # 数组
        explains_mob[2].save_state()

        def locked_anim(obj, alpha):
            obj.restore()
            obj.shift(alpha * UP)
            obj.set_opacity(1 - alpha * 0.6)

        self.play(UpdateFromAlphaFunc(explains_mob[2], locked_anim), FadeInFromDown(explains_mob[3]))
        self.wait()
        # 简易的数组1
        self.play(ShowPassingFlashAround(VGroup(*sudoku.blocks_list[0])))
        note_group = VGroup()
        delete_group = VGroup()
        unit_cands_list = [
            [1, 1, 1],
            [2, 1, 1],
            [1, 1, 9],
            [2, 1, 9],
        ]
        SetNote(note_group, unit_cands_list)
        unit_cands_list = [
            [2, 2, 1],
            [2, 3, 1],
            [2, 2, 9],
            [2, 3, 9],
            [3, 2, 9],
            [3, 3, 9],
        ]
        SetDelete(delete_group, unit_cands_list)
        self.play(FadeIn(VGroup(note_group, delete_group)))
        FlashFade(VGroup(
            sudoku.unit_cand(2, 2, 1),
            sudoku.unit_cand(2, 3, 1),
            sudoku.unit_cand(2, 2, 9),
            sudoku.unit_cand(2, 3, 9),
            sudoku.unit_cand(3, 2, 9),
            sudoku.unit_cand(3, 3, 9),
        ))
        self.play(FadeOut(VGroup(note_group, delete_group)))
        # 简易的数组1
        self.play(ShowPassingFlashAround(VGroup(*sudoku.blocks_list[8])))
        note_group = VGroup()
        delete_group = VGroup()
        unit_cands_list = [
            [8, 9, 2],
            [9, 9, 2],
            [8, 9, 9],
            [9, 9, 9],
        ]
        SetNote(note_group, unit_cands_list)
        unit_cands_list = [
            [8, 7, 2],
            [8, 8, 2],
            [7, 7, 9],
            [7, 8, 9],
            [8, 7, 9],
            [8, 8, 9],
        ]
        SetDelete(delete_group, unit_cands_list)
        self.play(FadeIn(VGroup(note_group, delete_group)))
        FlashFade(VGroup(
            sudoku.unit_cand(8, 7, 2),
            sudoku.unit_cand(8, 8, 2),
            sudoku.unit_cand(7, 7, 9),
            sudoku.unit_cand(7, 8, 9),
            sudoku.unit_cand(8, 7, 9),
            sudoku.unit_cand(8, 8, 9),
        ))
        self.play(FadeOut(VGroup(note_group, delete_group)))

        # 标准链
        # 用于标注链的函数
        def SetChain(note_group, node_list):
            count = 0
            last_node = None
            for cand in node_list:
                current_node = sudoku.unit_cand(*cand)
                if (last_node != None):
                    if (count % 2 == 1):
                        line = Line(
                            last_node.get_center(),
                            current_node.get_center(),
                            color=MAROON_B,
                            buff=0.1,
                            path_arc=20 / 180 * PI
                        )
                    else:
                        line = DashedLine(
                            last_node.get_center(),
                            current_node.get_center(),
                            color=LIGHT_GRAY,
                            buff=0.1,
                            path_arc=20 / 180 * PI
                        )
                    note_group.add(line)
                if (count % 2 == 0):
                    circle = Circle(stroke_color=WHITE,
                                    stroke_opacity=0.8,
                                    stroke_width=2,
                                    fill_color=PURPLE,
                                    fill_opacity=0.5,
                                    arc_center=current_node.get_center(),
                                    radius=sudoku.cand_scale * 0.25
                                    )
                else:
                    circle = Circle(stroke_color=WHITE,
                                    stroke_opacity=0.8,
                                    stroke_width=2,
                                    fill_color=GREEN,
                                    fill_opacity=0.5,
                                    arc_center=current_node.get_center(),
                                    radius=sudoku.cand_scale * 0.25
                                    )
                note_group.add(circle)

                last_node = current_node
                count += 1

        self.play(ApplyMethod(explains_mob[3].set_opacity, 0.4), FadeInFrom(explains_mob[4], UP))
        self.wait()

        # 简单的双线风筝1
        note_group = VGroup()
        delete_group = VGroup()
        node_list = [
            [3, 8, 9],
            [3, 5, 9],
            [2, 4, 9],
            [5, 4, 9]
        ]
        SetChain(note_group, node_list)
        self.play(Write(note_group))
        SetDelete(delete_group, [[5, 8, 9]])
        self.play(FadeIn(delete_group))
        FlashFade(VGroup(
            sudoku.unit_cand(5, 8, 9),
        ))
        self.play(FadeOut(VGroup(note_group, delete_group)))
        # 简单的双线风筝2
        note_group = VGroup()
        delete_group = VGroup()
        node_list = [
            [7, 2, 9],
            [7, 5, 9],
            [8, 6, 9],
            [5, 6, 9]
        ]
        SetChain(note_group, node_list)
        self.play(Write(note_group))
        SetDelete(delete_group, [[5, 2, 9]])
        self.play(FadeIn(delete_group))
        FlashFade(VGroup(
            sudoku.unit_cand(5, 2, 9),
        ))
        self.play(FadeOut(VGroup(note_group, delete_group)))
        # AIC
        note_group = VGroup()
        delete_group = VGroup()
        node_list = [
            [2, 3, 2],
            [2, 3, 5],
            [2, 2, 5],
            [7, 2, 5],
            [7, 2, 9],
            [7, 5, 9],
            [3, 5, 9],
            [3, 5, 2],
        ]
        SetChain(note_group, node_list)
        self.play(Write(note_group))
        unit_cands_list = [
            [2, 4, 2],
            [3, 2, 2],
            [3, 3, 2],
        ]
        SetDelete(delete_group, unit_cands_list)
        self.play(FadeIn(delete_group))
        FlashFade(VGroup(
            sudoku.unit_cand(2, 4, 2),
            sudoku.unit_cand(3, 2, 2),
            sudoku.unit_cand(3, 3, 2)
        ))
        self.play(FadeOut(VGroup(note_group, delete_group)))
        self.wait()
        # 经过一通操作后
        self.play(ReplacementTransform(captions_mob[2], captions_mob[3]))

        # Easy 164
        explains_mob[1].save_state()

        def difficulty_anim2(obj, alpha):
            obj.become(SudokuLine(str(round(1104 - (1104 - 164) * alpha)), font='ZCOOL Addict Italic 01', size=1))
            obj.next_to(explains_mob[1]).shift(0.05 * UP)
            obj.set_color(interpolate_color(RED, GREY_BROWN, alpha))

        self.play(Transform(explains_mob[1], explains_mob[5]), UpdateFromAlphaFunc(number, difficulty_anim2))
        self.wait(2)

        # 但今天要讲解的神奇方法……
        # 恢复盘面
        def difficulty_anim3(obj, alpha):
            obj.become(SudokuLine(str(round(164 + (1104 - 164) * alpha)), font='ZCOOL Addict Italic 01', size=1))
            obj.next_to(explains_mob[1]).shift(0.05 * UP)
            obj.set_color(interpolate_color(GREY_BROWN, RED, alpha))

        self.play(FadeOut(captions_mob[3]),
                  FadeIn(captions_mob[4]),
                  FadeOut(VGroup(*explains_mob[2:5])),
                  sudoku.restore,
                  explains_mob[1].restore,
                  UpdateFromAlphaFunc(number, difficulty_anim3),
                  run_time=2)
        self.wait()

        # 宇宙法（Gurth's Symmetrical Placement）
        def difficulty_anim4(obj, alpha):
            obj.become(SudokuLine(str(round(1104 - (1104 - 160) * alpha)), font='ZCOOL Addict Italic 01', size=1))
            obj.next_to(explains_mob[1]).shift(0.05 * UP)
            obj.set_color(interpolate_color(RED, GREY_BROWN, alpha))

        self.play(FadeIn(VGroup(*explains_mob[6:9])))
        self.wait()

        self.play(ReplacementTransform(captions_mob[4], captions_mob[5]),
                  Transform(explains_mob[1], explains_mob[5]),
                  UpdateFromAlphaFunc(number, difficulty_anim4)
                  )
        self.wait()

        self.play(sudoku.move_to, 3.5 * LEFT + 0.2 * UP,
                  FadeOut(VGroup(captions_mob[5],
                                 VGroup(*explains_mob[0:2],number),
                                 VGroup(*explains_mob[6:9]))))
        self.wait()
        explains_mob[1].restore()
        sudoku.save_state()


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
