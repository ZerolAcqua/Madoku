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

class TestScene1(Scene):
    CONFIG = {
        "camera_config": {
            "background_color": WHITE,
        },
    }
    def construct(self):
        Sl1=SquareLoop(color=PURPLE)
        self.play(Write(Sl1))
