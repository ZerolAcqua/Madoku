# -*- coding=utf-8 -*-

from manimlib.imports import*
from mydemo.Madoku.package_color import*
from mydemo.Madoku.package_motion import*
from sudoku import*



class SudokuScene(ThreeDScene):
    CONFIG = {
        "camera_config": {
            "background_color": WHITE,
        },
    }

    def construct(self):
        pass


    def 各种动画函数(self,其他可能的参数):
        pass


    @staticmethod
    def 各种对数独进行基本操作的函数(Sudoku,其他参数):
        pass


class SudokuLockedCandScene(SudokuScene):

    def construct(self):
        # 字幕等讲解内容
        captions = [
            "在之前Acqua的视频中，我们还有一个坑要填，就是它:",
            "咳咳，不过稍安勿躁，有一些术语还是需要说明一下的",
            "为兼顾直观和理论性，我们需要引入记号",
            "具体的某个行列宫，就用rcb加上数字表示",
            "用行和列就可以确定一个格子（单元格）",
            "言归正传，我们开始吧"
        ]
        captions_mob = VGroup(
            *[
                SudokuLine(cap, font='站酷小薇LOGO体', size=1)
                for cap in captions
            ]
        )

        for i in [2,3,4]:
            captions_mob[i].to_edge(DOWN*0.5)

        for i in [5]:
            captions_mob[i].move_to(RIGHT*3.5)






        # 之前剩下没做完的数独
        Sudoku1=SudokuWithTag(num_str='1..4..6..2..1.....5...7..9.......9.8....647.........5.62...3..443.85..6...9..1..7',
                       plot_depth=-2,center_of_squares=[0,0])
        bgSquare = Square(side_length=40, fill_color=WHITE, fill_opacity=0.96)




        # "在之前Acqua的视频中，我们还有一个坑要填，就是它:"
        self.wait()
        self.play(Write(captions_mob[0]))
        self.play(FadeOut(captions_mob[0]))

        # 展示数独盘面
        self.play(Write(Sudoku1[0:2]))
        self.add(Sudoku1[0:2])
        self.wait()

        # "咳咳，不过稍安勿躁，有一些术语还是需要说明一下的"
        self.play(FadeIn(bgSquare))         # 数独盘面变淡
        self.add(bgSquare)
        self.play(Write(captions_mob[1]))
        self.wait()
        self.play(captions_mob[1].shift,np.array([-15,0,0]),rate_func=rush_into,run_time=0.5)
        # 符号
        # 一些讲解标注用的东西
        explains = [
            "行",
            "列",
            "宫",
            "row",
            "column",
            "block",
            "r",
            "c",
            "b",
            " 第三行 ",
            " 第四列 ",
            " 第五宫 ",
            "r3",
            "c4",
            "b5",
            "="
        ]
        explains_mob = VGroup(
            *[
                SudokuLine(exp, font='站酷小薇LOGO体', size=2)
                for exp in explains
            ]
        )

        temp=VGroup(explains_mob[0:3])
        explains_mob[9].next_to(explains_mob[10],LEFT)
        explains_mob[11].next_to(explains_mob[10],RIGHT)
        explains_mob[0].move_to(explains_mob[9])
        explains_mob[1]
        explains_mob[2].move_to(explains_mob[11])
        explains_mob[3].move_to(explains_mob[9]).align_to(explains_mob[4],DOWN)
        explains_mob[4]
        explains_mob[5].move_to(explains_mob[11])
        explains_mob[6].move_to(explains_mob[9])
        explains_mob[7]
        explains_mob[8].move_to(explains_mob[11])
        explains_mob[12].move_to(explains_mob[9])
        explains_mob[13]
        explains_mob[14].move_to(explains_mob[11])


        self.wait()
        # # "为了兼顾直观和理论性，我们需要引入符号，来指示某一格的数字",行列宫
        self.play(Write(captions_mob[2]),FadeInFromDown(temp), lag_ratio=0.2)
        self.wait()

        # row column block
        self.play(Transform(explains_mob[0], explains_mob[3]),
                  Transform(explains_mob[1], explains_mob[4]),
                  Transform(explains_mob[2], explains_mob[5]))
        self.wait()
        # r c b
        self.play(Transform(explains_mob[0], explains_mob[6]),
                  Transform(explains_mob[1], explains_mob[7]),
                  Transform(explains_mob[2], explains_mob[8]))
        self.play(Flash(explains_mob[0], color=RED, flash_radius=1),
                  Flash(explains_mob[1], color=YELLOW_D, flash_radius=1),
                  Flash(explains_mob[2], color=GREEN, flash_radius=1))
        self.wait(1)
        # r3 c4 b5   "具体的某个行列宫，就用rcb加上数字表示"
        self.play(ReplacementTransform(captions_mob[2], captions_mob[3]))
        self.play(Transform(explains_mob[0], explains_mob[9]),
                  Transform(explains_mob[1], explains_mob[10]),
                  Transform(explains_mob[2], explains_mob[11]))
        self.wait()
        self.play(Transform(explains_mob[0], explains_mob[12]),
                  Transform(explains_mob[1], explains_mob[13]),
                  Transform(explains_mob[2], explains_mob[14]))
        self.play(Flash(explains_mob[0], color=RED, flash_radius=1),
                  Flash(explains_mob[1], color=YELLOW_D, flash_radius=1),
                  Flash(explains_mob[2], color=GREEN, flash_radius=1))
        self.wait(1)

        # 展示具体行列宫
        self.play(FadeOut(VGroup(*explains_mob[0:3])),
                  bgSquare.set_fill,{'opacity':0})

        self.play(FadeOut(Sudoku1[1]))
        self.wait()



        self.play(ApplyMethod(Sudoku1.tag.set_opacity,1,lag_ratio=0.5,run_time=3))
        self.wait(2)

        self.play(FadeOut(Sudoku1.tag[18:28]))
        Sudoku1.tag[18:28].set_opacity(0)
        self.wait()


        # "用行和列就可以确定一个格子（单元格）"
        self.play(Transform(captions_mob[3],captions_mob[4]))
        self.play(Sudoku1[0].shift,LEFT*3,
                  Sudoku1[3].shift,LEFT*3)
        Sudoku1[1:3].shift(LEFT*3)

        temp = VGroup(Sudoku1.rows_v_list[5].copy().set_color(RED),
                       Sudoku1.cols_v_list[3].copy().set_color(YELLOW_D),
                       Sudoku1.squares[5 * 9 + 3].copy().set_color(PURPLE).set_plot_depth(3))





        self.play(FadeIn(temp),lag_ratio=0.5)
        self.play(Indicate(temp[2],color=PURPLE))
        self.wait()

        #                       r6             r6          c4        square         =
        temp_copy=VGroup(Sudoku1.tag[5].copy(),Sudoku1.tag[5].copy().set_opacity(0),Sudoku1.tag[12].copy(),temp[2].copy(),explains_mob[15])
        temp_copy[4].move_to(RIGHT*3.5)
        temp_copy[1].next_to(temp_copy[4],RIGHT)
        self.play(temp_copy[3].next_to,temp_copy[4],LEFT,
                  FadeIn(temp_copy[4]),
                  temp_copy[0].next_to,temp_copy[4],
                  temp_copy[2].next_to,temp_copy[1])

        self.wait()
        self.play(FadeOut(VGroup(*temp_copy,*temp)),
                  Sudoku1.tag.set_opacity,0,
                  FadeOut(captions_mob[3]))
        self.wait()

        Sudoku2=SudokuWithKnownNum(num_str='1..4..6..2..1.....5...7..91......9.8....647.........56621793584437852169859641..7',
                                   plot_depth=-1, center_of_squares=[3, 0])
        Sudoku2.SetKnownNum('..........................1..........................6..179.58...7..21.985.64....')
        Sudoku2.move_to(Sudoku1[0])

        # "言归正传，我们开始吧"
        self.play(Write(captions_mob[5]))
        self.wait()
        self.play(FadeIn(Sudoku1[1]))
        self.play(FadeOut(Sudoku1[0:2]),
                  FadeIn(Sudoku2))
        self.wait()



