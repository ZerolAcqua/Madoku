# -*- coding=utf-8 -*-
import random
import time
from manimlib.imports import*
from package_color import *


# @Naxi-s
# 动画效果类，移除V对象的破碎效果，其中的参数都除了Mobject和run_time外都可以忽略
# Acqua做出的修改有：① parti_color的缺省值改为None,相应的判断也进行了修改
#                 ② run_time是基类的属性，所以我这里删掉了
#                 ③ 封装成类,可以像manim的其他方法那样同时调用，或许写成方法会更加灵活和方便
#                 ④ 修复了正方形粒子效果位置错误的BUG
# Todo:暂时没想好，主要是卡顿的问题
class FadeOutWithParticles(FadeOut):
    CONFIG = {
        'inner_round': 0.01,
        'inner_round': 0.01,
        'outer_round': 0.1,
        'parti_color': None,
        'mobjects_range_inf': 0,
        'mobjects_range_sup': 0.06,
        'circles': 30,
        'squares': 0,
        'v_number': 0,
        'v_letters': 0,
        'opacity': 1
    }

    def __init__(self, mobject, **kwargs):
        assert(isinstance(mobject, Mobject))
        digest_config(self,kwargs)
        self.list1 = []
        self.list2 = []
        self.vg = VGroup()   # 存储随机的圆形和正方形
        mobject.set_opacity(0)

        random.seed(time)
        for i in range(0, self.circles):
            a = random.uniform(self.mobjects_range_inf, self.mobjects_range_sup)
            b = random.uniform(self.inner_round, self.outer_round)
            if self.parti_color == None:
                c = random.randint(0, 100)
                m = random.randint(0, 100)
                y = random.randint(0, 100)
                k = random.randint(0, 100)
                color = trans_cmyk_to_rgb(c, m, y, k)
            if self.parti_color != 0:
                color = self.parti_color

            if self.opacity == -1:
                locals()['circles' + str(i)] = Circle(fill_color=color,
                                                      fill_opacity=self.opacity,
                                                      stroke_width=0).scale(a)
            if 0 <= self.opacity <= 1:
                locals()['circles' + str(i)] = Circle(fill_color=color,
                                                      fill_opacity=self.opacity,
                                                      stroke_width=0).scale(a)
            self.vg.add(locals()['circles' + str(i)])
            self.list1.append(random.uniform(0, 2 * PI))
            self.list2.append(RIGHT * np.cos(self.list1[i]) * b + b * UP * np.sin(self.list1[i]))
            locals()['circles' + str(i)].shift(self.list2[i]+mobject.get_center())


        for i in range(0, self.squares):
            a = random.uniform(self.mobjects_range_inf, self.mobjects_range_sup)
            b = random.uniform(self.inner_round, self.outer_round)
            if self.parti_color == 0:
                c = random.randint(0, 100)
                m = random.randint(0, 100)
                y = random.randint(0, 100)
                k = random.randint(0, 100)
                color = trans_cmyk_to_rgb(c, m, y, k)
            if self.parti_color != 0:
                color = self.parti_color
            if self.opacity == -1:
                locals()['squares' + str(i)] = Square(fill_color=color,
                                                      fill_opacity=self.opacity,
                                                      stroke_width=0).scale(a)
            if 0 <= self.opacity <= 1:
                locals()['squares' + str(i)] = Square(fill_color=color,
                                                      fill_opacity=self.opacity,
                                                      stroke_width=0).scale(a)
            self.vg.add(locals()['squares' + str(i)])
            self.list1.append(random.uniform(0, 2 * PI))
            self.list2.append(
                RIGHT * np.cos(self.list1[i + self.circles]) * b + b * UP * np.sin(self.list1[i + self.circles]))
            locals()['squares' + str(i)].shift(self.list2[i + self.circles]+mobject.get_center())

        self.vg.add(mobject)
        super().__init__(self.vg, **kwargs)


    def create_target(self):
        # 物体破碎成粒子的效果
        target_vg=self.vg.copy()
        for i in range(0, self.circles + self.squares):
            target_vg[i].shift(self.list2[i])
            target_vg[i].fade(1)
        target_vg[-1].set_opacity(0)
        # for i in range(0, self.circles):
        #     text1 = text1 + "FadeOutAndShift(locals()['circles'+str(" + str(i) + ")], list2[" + str(i) + "]), "
        # for i in range(self.circles, self.circles + self.squares):
        #     text1 = text1 + "FadeOutAndShift(locals()['squares'+str(" + str(i-self.circles) + ")], list2[" + str(i) + "]), "
        # text1 = text1 + 'rate_func=slow_into, run_time=5*run_time/6)'
        # exec(text1)
        return target_vg




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