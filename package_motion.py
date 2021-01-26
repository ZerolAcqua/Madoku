# -*- coding=utf-8 -*-
import random
import time
from manimlib.imports import*
from package_color import *


# 移除V对象的破碎效果，其中的参数都除了vmobject和run_time外都可以忽略
def move_out_effects_particles_1(self, vmobject_A, run_time=1, inner_round=0.01, outer_round=0.1, parti_color=0,
                                 mobjects_range_inf=0, mobjects_range_sup=0.06, opacity=1, circles=10, squares=0,
                                 v_number=0, v_letters=0, **kwargs):
    # 物体破碎成粒子的效果
    list1 = []
    list2 = []
    group1 = VGroup()
    random.seed(time)
    for i in range(0, circles):
        a = random.uniform(mobjects_range_inf, mobjects_range_sup)
        b = random.uniform(inner_round, outer_round)
        if parti_color == 0:
            c = random.randint(0, 100)
            m = random.randint(0, 100)
            y = random.randint(0, 100)
            k = random.randint(0, 100)
            color = trans_cmyk_to_rgb(c, m, y, k)
        if parti_color != 0:
            color = parti_color
        if opacity == -1:
            locals()['circles' + str(i)] = Circle(fill_color=color,
                                                  fill_opacity=opacity,
                                                  stroke_width=0).scale(a)
        if 0 <= opacity <= 1:
            locals()['circles' + str(i)] = Circle(fill_color=color,
                                                  fill_opacity=opacity,
                                                  stroke_width=0).scale(a)
        group1.add(locals()['circles' + str(i)])
        list1.append(random.uniform(0, 2 * PI))
        list2.append(RIGHT * np.cos(list1[i]) * b + b * UP * np.sin(list1[i]))
        locals()['circles' + str(i)].shift(list2[i]+vmobject_A.get_center())
    for i in range(0, squares):
        a = random.uniform(mobjects_range_inf, mobjects_range_sup)
        b = random.uniform(inner_round, outer_round)
        if parti_color == 0:
            c = random.randint(0, 100)
            m = random.randint(0, 100)
            y = random.randint(0, 100)
            k = random.randint(0, 100)
            color = trans_cmyk_to_rgb(c, m, y, k)
        if parti_color != 0:
            color = parti_color
        if opacity == -1:
            locals()['squares' + str(i)] = Square(fill_color=color,
                                                  fill_opacity=opacity,
                                                  stroke_width=0).scale(a)
        if 0 <= opacity <= 1:
            locals()['squares' + str(i)] = Square(fill_color=color,
                                                  fill_opacity=opacity,
                                                  stroke_width=0).scale(a)
        group1.add(locals()['squares' + str(i)])
        list1.append(random.uniform(0, 2 * PI))
        list2.append(RIGHT * np.cos(list1[i+circles]) * b + b * UP * np.sin(list1[i+circles]))
        locals()['squares' + str(i)].shift(list2[i+circles])
    self.play(ReplacementTransform(vmobject_A, group1), rate_func=rush_into, run_time=run_time/6)
    text1 = "self.play("
    for i in range(0, circles):
        text1 = text1 + "FadeOutAndShift(locals()['circles'+str(" + str(i) + ")], list2[" + str(i) + "]), "
    for i in range(circles, circles + squares):
        text1 = text1 + "FadeOutAndShift(locals()['squares'+str(" + str(i-circles) + ")], list2[" + str(i) + "]), "
    text1 = text1 + 'rate_func=slow_into, run_time=5*run_time/6)'
    exec(text1)
    vmobject_A.set_opacity(0)


# 流动显示列表中的元素，显示后再消失
def flow_v_list(self, vmob_list, lag_ratio=0.03, run_time=1):
    self.play(LaggedStart(*[FadeIn(i, rate_func=there_and_back) for i in vmob_list],
                          lag_ratio=lag_ratio), run_time=run_time, rate_func=slow_into)


class SquareLoop(Circle):
    CONFIG = {
        "inner_radius": 1,
        "outer_radius": 2,
        "fill_opacity": 0.3,
        "stroke_width": 0,
        "corner_radius": 0.01,
        "color": WHITE,
        "mark_paths_closed": False,
    }

    def generate_points(self):
        self.radius = self.outer_radius
        outer_square = RoundedRectangle(height=2 * self.outer_radius, width=2 * self.outer_radius,
                                        corner_radius=self.corner_radius)
        inner_square = RoundedRectangle(height=2 * self.inner_radius, width=2 * self.inner_radius,
                                        corner_radius=self.corner_radius)
        inner_square.reverse_points()
        self.append_points(outer_square.points)
        self.append_points(inner_square.points)
        self.shift(self.arc_center)


def wave(self, vmobject_A):
    list1 = []
    for i in range(0, 30):
        squ = SquareLoop(inner_radius=0.04*i+0.3,
                         outer_radius=0.04*i+0.04+0.3,
                         fill_color=trans_cmyk_to_rgb(30+i, 60-i, 20, 0),
                         fill_opacity=0.45-0.015*i,
                         corner_radius=0.01+0.03*i,
                         stroke_width=0).shift(vmobject_A.get_center())
        list1.append(squ)
    flow_v_list(self, list1)