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

        # 一些讲解标注用的东西

        # --------- 标题 -----------
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
        self.wait(5)

        # -------- 第一部分 引入 ---------
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

        # 标题淡出
        self.play(FadeOut(title[0]),
                  FadeOut(title[1]),
                  FadeOut(title[2]),
                  FadeOut(title[3]),
                  FadeOut(title[4]),
                  FadeOut(title[5]))

        self.wait(5)

        # 数独显示
        sudoku = Sudoku(center_of_squares=2.5 * LEFT + 0.2 * UP,
                        num_str='.37658..4....34.764..1.75.32..3.5..88.......55..8.6..16.84.2..734.76....7..58346.')
        self.play(Write(sudoku))
        self.wait(5)

        # Unfair 1044
        def difficulty_anim1(obj, alpha):
            obj.become(SudokuLine(str(round(1104 * alpha)), font='ZCOOL Addict Italic 01', size=1))
            obj.next_to(VGroup(*explains_mob[0:2])).shift(0.05 * UP)
            obj.set_color(interpolate_color(GREY_BROWN, RED, alpha))

        self.play(FadeIn(VGroup(*explains_mob[0:2])),
                  UpdateFromAlphaFunc(number, difficulty_anim1))
        self.wait(5)

        # 通常要使用到不少的技巧才能解出
        self.play(ApplyMethod(VGroup(VGroup(*explains_mob[0:2]), number).shift, 2.5 * UP))
        explains_mob[5].next_to(explains_mob[0], RIGHT)
        self.wait(5)

        # 常规解法演示
        # 用于标注的两个函数
        def set_note(sudoku, note_group, unit_cands_list):
            for i in unit_cands_list:
                circle = Circle(stroke_color=WHITE,
                                stroke_opacity=0.8,
                                stroke_width=2,
                                fill_color=GREEN,
                                fill_opacity=0.5,
                                arc_center=sudoku.get_cand_unit(*i).get_center(),
                                radius=sudoku.cand_scale * 0.25
                                )
                note_group.add(circle)

        def set_delete(sudoku, delete_group, unit_cands_list):
            for i in unit_cands_list:
                circle = Circle(stroke_color=WHITE,
                                stroke_opacity=0.8,
                                stroke_width=2,
                                fill_color=RED,
                                fill_opacity=0.5,
                                arc_center=sudoku.get_cand_unit(*i).get_center(),
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
        self.wait(5)
        # 简易的区块摒除1
        self.play(ShowPassingFlashAround(VGroup(*sudoku.blocks_list[2])))
        note_group = VGroup()
        delete_group = VGroup()
        unit_cands_list = [
            [1, 7, 2],
            [1, 8, 2],
        ]
        set_note(sudoku, note_group, unit_cands_list)
        unit_cands_list = [
            [2, 7, 2],
            [3, 8, 2],
        ]
        set_delete(sudoku, delete_group, unit_cands_list)
        self.play(FadeIn(VGroup(note_group, delete_group)))
        FlashFade(VGroup(
            sudoku.get_cand_unit(2, 7, 2),
            sudoku.get_cand_unit(3, 8, 2)
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
        set_note(sudoku, note_group, unit_cands_list)
        unit_cands_list = [
            [7, 2, 1],
            [8, 3, 1],
        ]
        set_delete(sudoku, delete_group, unit_cands_list)
        self.play(FadeIn(VGroup(note_group, delete_group)))
        FlashFade(VGroup(
            sudoku.get_cand_unit(7, 2, 1),
            sudoku.get_cand_unit(8, 3, 1)
        ))
        self.play(FadeOut(VGroup(note_group, delete_group)))

        # 数组
        explains_mob[2].save_state()

        def locked_anim(obj, alpha):
            obj.restore()
            obj.shift(alpha * UP)
            obj.set_opacity(1 - alpha * 0.6)

        self.play(UpdateFromAlphaFunc(explains_mob[2], locked_anim), FadeInFromDown(explains_mob[3]))
        self.wait(5)
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
        set_note(sudoku, note_group, unit_cands_list)
        unit_cands_list = [
            [2, 2, 1],
            [2, 3, 1],
            [2, 2, 9],
            [2, 3, 9],
            [3, 2, 9],
            [3, 3, 9],
        ]
        set_delete(sudoku, delete_group, unit_cands_list)
        self.play(FadeIn(VGroup(note_group, delete_group)))
        FlashFade(VGroup(
            sudoku.get_cand_unit(2, 2, 1),
            sudoku.get_cand_unit(2, 3, 1),
            sudoku.get_cand_unit(2, 2, 9),
            sudoku.get_cand_unit(2, 3, 9),
            sudoku.get_cand_unit(3, 2, 9),
            sudoku.get_cand_unit(3, 3, 9),
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
        set_note(sudoku, note_group, unit_cands_list)
        unit_cands_list = [
            [8, 7, 2],
            [8, 8, 2],
            [7, 7, 9],
            [7, 8, 9],
            [8, 7, 9],
            [8, 8, 9],
        ]
        set_delete(sudoku, delete_group, unit_cands_list)
        self.play(FadeIn(VGroup(note_group, delete_group)))
        FlashFade(VGroup(
            sudoku.get_cand_unit(8, 7, 2),
            sudoku.get_cand_unit(8, 8, 2),
            sudoku.get_cand_unit(7, 7, 9),
            sudoku.get_cand_unit(7, 8, 9),
            sudoku.get_cand_unit(8, 7, 9),
            sudoku.get_cand_unit(8, 8, 9),
        ))
        self.play(FadeOut(VGroup(note_group, delete_group)))

        # 标准链
        # 用于标注链的函数
        def set_chain(sudoku, note_group, node_list):
            count = 0
            last_node = None
            for cand in node_list:
                current_node = sudoku.get_cand_unit(*cand)
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
        self.wait(5)

        # 简单的双线风筝1
        note_group = VGroup()
        delete_group = VGroup()
        node_list = [
            [3, 8, 9],
            [3, 5, 9],
            [2, 4, 9],
            [5, 4, 9]
        ]
        set_chain(sudoku, note_group, node_list)
        self.play(Write(note_group))
        set_delete(sudoku, delete_group, [[5, 8, 9]])
        self.play(FadeIn(delete_group))
        FlashFade(VGroup(
            sudoku.get_cand_unit(5, 8, 9),
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
        set_chain(sudoku, note_group, node_list)
        self.play(Write(note_group))
        set_delete(sudoku, delete_group, [[5, 2, 9]])
        self.play(FadeIn(delete_group))
        FlashFade(VGroup(
            sudoku.get_cand_unit(5, 2, 9),
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
        set_chain(sudoku, note_group, node_list)
        self.play(Write(note_group))
        unit_cands_list = [
            [2, 4, 2],
            [3, 2, 2],
            [3, 3, 2],
        ]
        set_delete(sudoku, delete_group, unit_cands_list)
        self.play(FadeIn(delete_group))
        FlashFade(VGroup(
            sudoku.get_cand_unit(2, 4, 2),
            sudoku.get_cand_unit(3, 2, 2),
            sudoku.get_cand_unit(3, 3, 2)
        ))
        self.play(FadeOut(VGroup(note_group, delete_group)))
        self.wait(5)

        # Easy 164
        explains_mob[1].save_state()

        def difficulty_anim2(obj, alpha):
            obj.become(SudokuLine(str(round(1104 - (1104 - 164) * alpha)), font='ZCOOL Addict Italic 01', size=1))
            obj.next_to(explains_mob[1]).shift(0.05 * UP)
            obj.set_color(interpolate_color(RED, GREY_BROWN, alpha))

        self.play(Transform(explains_mob[1], explains_mob[5]), UpdateFromAlphaFunc(number, difficulty_anim2))
        self.wait(5)

        # 但今天要讲解的神奇方法……
        # 恢复盘面
        def difficulty_anim3(obj, alpha):
            obj.become(SudokuLine(str(round(164 + (1104 - 164) * alpha)), font='ZCOOL Addict Italic 01', size=1))
            obj.next_to(explains_mob[1]).shift(0.05 * UP)
            obj.set_color(interpolate_color(GREY_BROWN, RED, alpha))

        self.play(FadeOut(VGroup(*explains_mob[2:5])),
                  sudoku.restore,
                  explains_mob[1].restore,
                  UpdateFromAlphaFunc(number, difficulty_anim3),
                  run_time=2)
        self.wait(5)

        # 宇宙法（Gurth's Symmetrical Placement）
        def difficulty_anim4(obj, alpha):
            obj.become(SudokuLine(str(round(1104 - (1104 - 160) * alpha)), font='ZCOOL Addict Italic 01', size=1))
            obj.next_to(explains_mob[1]).shift(0.05 * UP)
            obj.set_color(interpolate_color(RED, GREY_BROWN, alpha))

        self.play(FadeIn(VGroup(*explains_mob[6:9])))
        self.wait(5)

        self.play(Transform(explains_mob[1], explains_mob[5]),
                  UpdateFromAlphaFunc(number, difficulty_anim4)
                  )
        self.wait(5)

        self.play(FadeOut(VGroup(VGroup(*explains_mob[0:2], number),
                                 VGroup(*explains_mob[6:9]))),
                  sudoku.move_to, 3.5 * RIGHT + 0.2 * UP
                  )
        self.wait(5)
        explains_mob[1].restore()

        # --------- 第二部分 替换 ----------
        sudoku1 = sudoku.deepcopy()
        sudoku1.move_to(3.5 * LEFT + 0.2 * UP)
        sudoku1.save_state()
        sudoku1.scale(0.7).to_edge(LEFT, buff=1.2)
        sudoku.save_state()

        # 用于将数字替换为其他符号   target     数字   字符串
        def replace_num_with(target_sudoku, ori, des):
            for row in range(9):
                for col in range(9):
                    if (target_sudoku.domain_nums_list[row * 9 + col] == ori):
                        temp = SudokuLine(des, color=GREY_BROWN, size=target_sudoku.num_scale).move_to(
                            target_sudoku.nums_list[row * 9 + col].get_center()
                        )
                        target_sudoku.nums_list[row * 9 + col].become(temp)

                    if (target_sudoku.domain_cands_list[row * 9 + col][ori - 1]
                            and target_sudoku.domain_nums_list[row * 9 + col] == 0):
                        temp = SudokuLine(des, color=GREY_BROWN, size=target_sudoku.cand_scale).move_to(
                            target_sudoku.cands_list[row * 9 + col][ori - 1].get_center()
                        ).set_opacity(target_sudoku.cands_list[row * 9 + col][ori - 1].get_fill_opacity())
                        target_sudoku.cands_list[row * 9 + col][ori - 1].become(temp)

        # 替换1
        target_sudoku = sudoku.generate_target(use_deepcopy=True)
        replace_num_with(target_sudoku, 1, 'A')
        replace_num_with(target_sudoku, 2, 'B')
        replace_num_with(target_sudoku, 3, 'C')
        replace_num_with(target_sudoku, 4, 'D')
        replace_num_with(target_sudoku, 5, 'E')
        replace_num_with(target_sudoku, 6, 'F')
        replace_num_with(target_sudoku, 7, 'G')
        replace_num_with(target_sudoku, 8, 'H')
        replace_num_with(target_sudoku, 9, 'I')
        mapping = [
            '1 --> A',
            '2 --> B',
            '3 --> C',
            '4 --> D',
            '5 --> E',
            '6 --> F',
            '7 --> G',
            '8 --> H',
            '9 --> I'
        ]
        mappings_mob1 = VGroup(
            *[
                SudokuLine(map, font='站酷小薇LOGO体', size=1)
                for map in mapping
            ]
        ).arrange(DOWN, aligned_edge=LEFT).next_to(sudoku, 2 * LEFT)
        self.play(MoveToTarget(sudoku),
                  FadeIn(sudoku1),
                  AnimationGroup(*[FadeInFromDown(mob) for mob in mappings_mob1], lag_ratio=0.1, run_time=1))
        self.wait(5)

        # 替换2
        mapping = [
            '1 --> 一',
            '2 --> 二',
            '3 --> 三',
            '4 --> 四',
            '5 --> 五',
            '6 --> 六',
            '7 --> 七',
            '8 --> 八',
            '9 --> 九'
        ]
        mappings_mob2 = VGroup(
            *[
                SudokuLine(map, font='站酷小薇LOGO体', size=1)
                for map in mapping
            ]
        ).arrange(DOWN, aligned_edge=LEFT).next_to(sudoku, 2 * LEFT)
        replace_num_with(target_sudoku, 1, '一')
        replace_num_with(target_sudoku, 2, '二')
        replace_num_with(target_sudoku, 3, '三')
        replace_num_with(target_sudoku, 4, '四')
        replace_num_with(target_sudoku, 5, '五')
        replace_num_with(target_sudoku, 6, '六')
        replace_num_with(target_sudoku, 7, '七')
        replace_num_with(target_sudoku, 8, '八')
        replace_num_with(target_sudoku, 9, '九')
        self.play(MoveToTarget(sudoku),
                  AnimationGroup(*[FadeOutAndShift(mob, UP) for mob in mappings_mob1], lag_ratio=0.1, run_time=1),
                  AnimationGroup(*[FadeInFromDown(mob) for mob in mappings_mob2], lag_ratio=0.1, run_time=1))
        self.wait(5)

        # 替换3
        mappings_mob1 = mappings_mob2
        mapping = [
            '1 --> 三',
            '2 --> 连',
            '3 --> 投',
            '4 --> 币',
            '5 --> 点',
            '6 --> 赞',
            '7 --> 和',
            '8 --> 收',
            '9 --> 藏'
        ]
        mappings_mob2 = VGroup(
            *[
                SudokuLine(map, font='站酷小薇LOGO体', size=1)
                for map in mapping
            ]
        ).arrange(DOWN, aligned_edge=LEFT).next_to(sudoku, 2 * LEFT)
        replace_num_with(target_sudoku, 1, '三')
        replace_num_with(target_sudoku, 2, '连')
        replace_num_with(target_sudoku, 3, '投')
        replace_num_with(target_sudoku, 4, '币')
        replace_num_with(target_sudoku, 5, '点')
        replace_num_with(target_sudoku, 6, '赞')
        replace_num_with(target_sudoku, 7, '和')
        replace_num_with(target_sudoku, 8, '收')
        replace_num_with(target_sudoku, 9, '藏')
        self.play(MoveToTarget(sudoku),
                  AnimationGroup(*[FadeOutAndShift(mob, UP) for mob in mappings_mob1], lag_ratio=0.1, run_time=1),
                  AnimationGroup(*[FadeInFromDown(mob) for mob in mappings_mob2], lag_ratio=0.1, run_time=1))
        self.wait(5)

        # 替换4
        mappings_mob1 = mappings_mob2
        mapping = [
            '1 --> !',
            '2 --> @',
            '3 --> #',
            '4 --> $',
            '5 --> %',
            '6 --> ^',
            '7 --> &',
            '8 --> *',
            '9 --> ('
        ]
        mappings_mob2 = VGroup(
            *[
                SudokuLine(map, font='站酷小薇LOGO体', size=1)
                for map in mapping
            ]
        ).arrange(DOWN, aligned_edge=LEFT).next_to(sudoku, 2 * LEFT)
        replace_num_with(target_sudoku, 1, '!')
        replace_num_with(target_sudoku, 2, '@')
        replace_num_with(target_sudoku, 3, '#')
        replace_num_with(target_sudoku, 4, '$')
        replace_num_with(target_sudoku, 5, '%')
        replace_num_with(target_sudoku, 6, '^')
        replace_num_with(target_sudoku, 7, '&')
        replace_num_with(target_sudoku, 8, '*')
        replace_num_with(target_sudoku, 9, '(')
        self.play(MoveToTarget(sudoku),
                  AnimationGroup(*[FadeOutAndShift(mob, UP) for mob in mappings_mob1], lag_ratio=0.1, run_time=1),
                  AnimationGroup(*[FadeInFromDown(mob) for mob in mappings_mob2], lag_ratio=0.1, run_time=1))
        self.wait(5)

        self.play(sudoku1.restore,
                  FadeOut(mappings_mob2))
        sudoku1.restore_scale()

        note_group = VGroup()
        delete_group = VGroup()
        unit_cands_list = [
            [1, 7, 2],
            [1, 8, 2],
        ]
        set_note(sudoku, note_group, unit_cands_list)
        set_note(sudoku1, note_group, unit_cands_list)
        unit_cands_list = [
            [2, 7, 2],
            [3, 8, 2],
        ]
        set_delete(sudoku, delete_group, unit_cands_list)
        set_delete(sudoku1, delete_group, unit_cands_list)
        self.play(FadeIn(VGroup(note_group, delete_group)))
        sudoku1.save_state()
        FlashFade(VGroup(
            sudoku.get_cand_unit(2, 7, 2),
            sudoku.get_cand_unit(3, 8, 2),
            sudoku1.get_cand_unit(2, 7, 2),
            sudoku1.get_cand_unit(3, 8, 2)
        ))
        self.play(FadeOut(VGroup(note_group, delete_group)))
        self.wait(5)

        self.play(sudoku.restore, FadeOut(sudoku1))
        self.wait(5)

        sudoku1.move_to(sudoku.get_center())
        sudoku1.generate_target(use_deepcopy=True).scale(0.7).to_edge(LEFT, buff=1.2)
        target_sudoku = sudoku.generate_target(use_deepcopy=True)

        # 替换5
        mapping = [
            '1 --> 2',
            '2 --> 1',
            '3 --> 6',
            '4 --> 7',
            '5 --> 8',
            '6 --> 3',
            '7 --> 4',
            '8 --> 5',
            '9 --> 9'
        ]
        mappings_mob2 = VGroup(
            *[
                SudokuLine(map, font='站酷小薇LOGO体', size=1)
                for map in mapping
            ]
        ).arrange(DOWN, aligned_edge=LEFT).next_to(sudoku, 2 * LEFT)
        replace_num_with(target_sudoku, 1, '2')
        replace_num_with(target_sudoku, 2, '1')
        replace_num_with(target_sudoku, 3, '6')
        replace_num_with(target_sudoku, 4, '7')
        replace_num_with(target_sudoku, 5, '8')
        replace_num_with(target_sudoku, 6, '3')
        replace_num_with(target_sudoku, 7, '4')
        replace_num_with(target_sudoku, 8, '5')
        self.play(MoveToTarget(sudoku),
                  AnimationGroup(*[FadeInFromDown(mob) for mob in mappings_mob2], lag_ratio=0.1, run_time=1),
                  MoveToTarget(sudoku1))
        self.wait(5)

        # 填数1
        sudoku.save_state()
        sudoku1.save_state()
        temp, cand = sudoku.solve([5, 5, 1], update_board=False)
        num, temp = sudoku.solve([5, 5, 2], update_board=False)
        num1, cand1 = sudoku1.solve([5, 5, 1], update_board=False)
        self.play(
            cand.set_opacity, 0,
            cand1.set_opacity, 0,
            *[
                Write(obj)
                for obj in num
            ],
            *[
                Write(obj)
                for obj in num1
            ],
            ShowPassingFlashAround(mappings_mob2[0])
        )
        self.wait(5)
        self.play(sudoku.restore, sudoku1.restore)
        self.wait(5)

        # 填数2
        temp, cand = sudoku.solve([5, 5, 2], update_board=False)
        num, temp = sudoku.solve([5, 5, 1], update_board=False)
        num1, cand1 = sudoku1.solve([5, 5, 2], update_board=False)
        self.play(
            cand.set_opacity, 0,
            cand1.set_opacity, 0,
            *[
                Write(obj)
                for obj in num
            ],
            *[
                Write(obj)
                for obj in num1
            ],
            ShowPassingFlashAround(mappings_mob2[1])
        )
        self.wait(5)
        self.play(sudoku.restore, sudoku1.restore)
        self.wait(5)

        # 填数3
        temp, cand = sudoku.solve([5, 5, 4], update_board=False)
        num, temp = sudoku.solve([5, 5, 7], update_board=False)
        num1, cand1 = sudoku1.solve([5, 5, 4], update_board=False)
        self.play(
            cand.set_opacity, 0,
            cand1.set_opacity, 0,
            *[
                Write(obj)
                for obj in num
            ],
            *[
                Write(obj)
                for obj in num1
            ],
            ShowPassingFlashAround(mappings_mob2[3])
        )
        self.wait(5)
        self.play(sudoku.restore, sudoku1.restore)
        self.wait(5)

        # 填数4
        temp, cand = sudoku.solve([5, 5, 7], update_board=False)
        num, temp = sudoku.solve([5, 5, 4], update_board=False)
        num1, cand1 = sudoku1.solve([5, 5, 7], update_board=False)
        self.play(
            cand.set_opacity, 0,
            cand1.set_opacity, 0,
            *[
                Write(obj)
                for obj in num
            ],
            *[
                Write(obj)
                for obj in num1
            ],
            ShowPassingFlashAround(mappings_mob2[6])
        )
        self.wait(5)
        self.play(sudoku.restore, sudoku1.restore)
        self.wait(5)

        # --------- 第三部分 旋转 ----------
        def symmetry_group(sudoku):
            num_group = VGroup()
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
                if (sudoku.domain_nums_list[i] != 0):
                    num_group.add(sudoku.nums_list[i], sudoku.nums_list[80 - i])
            return num_group

        self.wait(5)
        num_group = symmetry_group(sudoku)
        num_group.save_state()
        num_group1 = symmetry_group(sudoku1)
        num_group1.save_state()

        self.play(AnimationGroup(*[ApplyMethod(obj.set_color, YELLOW) for obj in num_group], lag_ratio=0.1),
                  AnimationGroup(*[ApplyMethod(obj.set_color, YELLOW) for obj in num_group1], lag_ratio=0.1),
                  run_time=3)
        self.wait(5)

        self.play(num_group.restore,
                  num_group1.restore)
        self.wait(5)

        def animSudokuRotation(obj, alpha):
            obj.restore()
            obj.rotate(-alpha * PI)
            for i in range(81):
                VGroup(*obj.cands_list[i]).rotate(alpha * PI)
            for i in range(81):
                obj.nums_list[i].rotate(alpha * PI)

        sudoku.save_state()
        self.play(UpdateFromAlphaFunc(sudoku, animSudokuRotation),
                  run_time=6,
                  rate_func=smooth,
                  lag_ratio=0.2)
        self.wait(5)

        # 错误填数1
        sudoku.save_state()
        sudoku1.save_state()
        target = sudoku.generate_target(use_deepcopy=True)
        target1 = sudoku1.generate_target(use_deepcopy=True)

        temp, cand = target.solve([5, 5, 1], update_board=False)
        num, temp = target.solve([5, 5, 2], update_board=False)
        num1, cand1 = target1.solve([5, 5, 1], update_board=False)
        num.set_color(RED)
        num1.set_color(RED)

        cand.set_opacity(0)
        cand1.set_opacity(0)

        self.play(
            MoveToTarget(sudoku),
            MoveToTarget(sudoku1),
            ShowPassingFlashAround(mappings_mob2[0], surrounding_rectangle_config={'color': RED})
        )
        self.wait(5)

        # 错误填数2
        target.become(sudoku.saved_state.deepcopy())
        target1.become(sudoku1.saved_state.deepcopy())
        temp, cand = target.solve([5, 5, 2], update_board=False)
        num, temp = target.solve([5, 5, 1], update_board=False)
        num1, cand1 = target1.solve([5, 5, 2], update_board=False)
        num.set_color(RED)
        num1.set_color(RED)

        cand.set_opacity(0)
        cand1.set_opacity(0)

        self.play(
            MoveToTarget(sudoku),
            MoveToTarget(sudoku1),
            ShowPassingFlashAround(mappings_mob2[1], surrounding_rectangle_config={'color': RED})
        )
        self.wait(5)

        # 错误填数3
        target.become(sudoku.saved_state.deepcopy())
        target1.become(sudoku1.saved_state.deepcopy())
        temp, cand = target.solve([5, 5, 4], update_board=False)
        num, temp = target.solve([5, 5, 7], update_board=False)
        num1, cand1 = target1.solve([5, 5, 4], update_board=False)
        num.set_color(RED)
        num1.set_color(RED)

        cand.set_opacity(0)
        cand1.set_opacity(0)

        self.play(
            MoveToTarget(sudoku),
            MoveToTarget(sudoku1),
            ShowPassingFlashAround(mappings_mob2[3], surrounding_rectangle_config={'color': RED})
        )
        self.wait(5)

        # 错误填数4
        target.become(sudoku.saved_state.deepcopy())
        target1.become(sudoku1.saved_state.deepcopy())
        temp, cand = target.solve([5, 5, 7], update_board=False)
        num, temp = target.solve([5, 5, 4], update_board=False)
        num1, cand1 = target1.solve([5, 5, 7], update_board=False)
        num.set_color(RED)
        num1.set_color(RED)

        cand.set_opacity(0)
        cand1.set_opacity(0)

        self.play(
            MoveToTarget(sudoku),
            MoveToTarget(sudoku1),
            ShowPassingFlashAround(mappings_mob2[6], surrounding_rectangle_config={'color': RED})
        )
        self.wait(5)

        # 正确填数5
        target.become(sudoku.saved_state.deepcopy())
        target1.become(sudoku1.saved_state.deepcopy())
        temp, cand = target.solve([5, 5, 9], update_board=False)
        num, temp = target.solve([5, 5, 9], update_board=False)
        num1, cand1 = target1.solve([5, 5, 9], update_board=False)
        num.set_color(YELLOW)
        num1.set_color(YELLOW)

        cand.set_opacity(0)
        cand1.set_opacity(0)

        self.play(
            MoveToTarget(sudoku),
            MoveToTarget(sudoku1),
            ShowPassingFlashAround(mappings_mob2[8], surrounding_rectangle_config={'color': YELLOW})
        )
        self.wait(5)

        # 说明
        sudoku3 = Sudoku(center_of_squares=0.2 * UP,
                         num_str='.37658..4....34.764..1.75.32..3.5..88.......55..8.6..16.84.2..734.76....7..58346.')
        self.play(sudoku.scale, 0,
                  sudoku1.become, sudoku3,
                  FadeOut(mappings_mob2))
        self.add(sudoku3)
        self.remove(sudoku1)
        self.wait(5)

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

        sudoku3.save_state()
        color_num1(sudoku3)
        self.play(AnimationGroup(
            *[
                MoveToTarget(sudoku3.nums_list[i])
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
                    MoveToTarget(sudoku3.nums_list[80 - i])
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
        # 填数
        num, cand = sudoku3.solve([5, 5, 9], update_board=False)
        num.set_color(YELLOW)
        self.play(
            cand.set_opacity, 0,
            *[
                Write(obj)
                for obj in num
            ]
        )
        self.wait(5)

        # --------- 第四部分 其他类型 ----------
        explains = [
            "中心对称",
            "轴对称"
        ]
        explains_mob = VGroup(
            *[
                SudokuLine(exp, font='站酷小薇LOGO体', size=1)
                for exp in explains
            ]
        )

        # 轴对称
        sudoku4 = Sudoku(center_of_squares=0.2 * UP + 3.5 * RIGHT,
                         num_str='1...5...2.2...93....37...1...4...2678.....534.6....891.3.2851....1936.2.2..471..3')

        explains_mob[0].next_to(sudoku3, DOWN).shift(3.5 * LEFT)
        explains_mob[1].next_to(sudoku4, DOWN)
        self.play(AnimationGroup(
            ApplyMethod(sudoku3.move_to, 3.5 * LEFT + 0.2 * UP),
            FadeIn(sudoku4),
            FadeInFrom(explains_mob[0], UP),
            FadeIn(explains_mob[1]),
            lag_ratio=0.6)
        )

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
        self.wait(5)

        def animSudokuFlip(obj, alpha):
            obj.restore()
            obj.rotate(-alpha * PI, axis=DR)
            for i in range(81):
                VGroup(*obj.cands_list[i]).rotate(alpha * PI, axis=DR)
            for i in range(81):
                obj.nums_list[i].rotate(alpha * PI, axis=DR)

        sudoku4.save_state()
        self.play(UpdateFromAlphaFunc(sudoku4, animSudokuFlip),
                  run_time=6,
                  rate_func=smooth,
                  lag_ratio=0.2)
        self.wait(5)

        cand_group = sudoku4.remove_cand([
            [4, 4, 5],
            [4, 4, 8],
            [5, 5, 6],
            [5, 5, 9],
            [6, 6, 4],
            [6, 6, 7],
        ], update_board=False)

        self.play(cand_group.set_opacity, 0)
        cand_group = sudoku4.remove_cand([
            [4, 5, 1],
            [4, 6, 3],
            [5, 4, 1],
            [5, 6, 2],
            [6, 4, 3],
            [6, 5, 2],
        ], update_board=False)
        self.play(cand_group.set_opacity, 0)
        self.wait(5)

        self.play(FadeOut(VGroup(explains_mob, sudoku3, sudoku4)))
        self.remove(sudoku3)

        # 小图标
        icon1 = VGroup()
        icon2 = VGroup()
        icon3 = VGroup()
        icon4 = VGroup()
        icon5 = VGroup()
        cross = VGroup()

        icon1.add(
            Square(side_length=2,
                   color=BLUE,
                   fill_color=BLUE,
                   fill_opacity=1,
                   ),
            Dot(color=YELLOW,
                fill_color=YELLOW))

        icon2.add(
            Square(side_length=2,
                   color=BLUE,
                   fill_color=BLUE,
                   fill_opacity=1,
                   ),
            Line(UL,
                 DR,
                 color=YELLOW,
                 fill_color=YELLOW))

        icon3.add(
            Square(side_length=2,
                   color=BLUE,
                   fill_color=BLUE,
                   fill_opacity=1,
                   ),
            Line(UR,
                 DL,
                 color=YELLOW,
                 fill_color=YELLOW))

        icon4.add(
            Square(side_length=2,
                   color=BLUE,
                   fill_color=BLUE,
                   fill_opacity=1,
                   ),
            Line(UP,
                 DOWN,
                 color=YELLOW,
                 fill_color=YELLOW))

        icon5.add(
            Square(side_length=2,
                   color=BLUE,
                   fill_color=BLUE,
                   fill_opacity=1,
                   ),
            Line(LEFT,
                 RIGHT,
                 color=YELLOW,
                 fill_color=YELLOW))
        cross.add(
            Line(3 * LEFT + UP,
                 3 * RIGHT + DOWN,
                 color=RED,
                 fill_color=RED,
                 stroke_width=5
                 ),
            Line(3 * RIGHT + UP,
                 3 * LEFT + DOWN,
                 color=RED,
                 fill_color=RED,
                 stroke_width=5
                 ))

        icon1.shift(3 * LEFT)
        icon3.shift(3 * RIGHT)
        icon4.shift(2 * LEFT + 1.5 * DOWN).set_opacity(0.3)
        icon5.shift(2 * RIGHT + 1.5 * DOWN).set_opacity(0.3)
        cross.shift(1.5 * DOWN)

        def update_anim1(obj, dt):
            obj.rotate(-dt)

        def update_anim2(obj, dt):
            obj.rotate(dt, axis=UL)

        def update_anim3(obj, dt):
            obj.rotate(dt, axis=DL)

        def update_anim4(obj, dt):
            obj.rotate(dt, axis=UP)

        def update_anim5(obj, dt):
            obj.rotate(dt, axis=RIGHT)

        icon1.add_updater(update_anim1)
        icon2.add_updater(update_anim2)
        icon3.add_updater(update_anim3)
        icon4.add_updater(update_anim4)
        icon5.add_updater(update_anim5)

        self.play(FadeIn(VGroup(icon1, icon2, icon3)))
        self.wait(4.5)

        self.play(VGroup(icon1, icon2, icon3).shift, 1.5 * UP,
                  FadeInFrom(VGroup(icon4, icon5), UP))

        self.wait(3)
        self.play(Write(cross))
        self.wait(4)
        self.play(FadeOut(VGroup(icon1, icon2, icon3, icon4, icon5, cross)))
        self.wait(5)

        self.play(Write(SudokuLine("感 谢 观 看",size=3)))
        self.wait(5)