from Package_Sudoku.Sudoku import *


class Sudoku_start(Sudoku_scene):
    def construct(self):
        ## 设置物体

        ## 盘面
        self.create_board("test/test01.txt", False)

        ## 文字
        introdution = TextMobject("一、认识数独盘面", tex_to_color_map={"数独": self.board_color})

        rule_title = TextMobject("二、数独的规则", tex_to_color_map={"数独": self.board_color})
        rule_text01 = TextMobject("规则1：数独的每行、每列，以及每个宫",
                                  tex_to_color_map={"数独": self.board_color, "行": self.row_color, "列": self.col_color,
                                                    "宫": self.box_color})
        rule_text02 = TextMobject("都有1-9九个数字，不能重复也不能缺少",
                                  tex_to_color_map={"1-9": PINK, "重复": ORANGE, "缺少": ORANGE})
        rule_text03 = TextMobject("规则2：一个正确的数独题目有唯一解", tex_to_color_map={"数独": self.board_color, "唯一": ORANGE})
        rule_text04 = TextMobject("不存在无解或多解的情况",
                                  tex_to_color_map={"不存在": PINK, "无解": ORANGE, "多解": ORANGE})

        explain_title = TextMobject("三、数独解法简介", tex_to_color_map={"数独": self.board_color})
        explain_text01 = TextMobject("根据规则1，第四行已经有8个数字", tex_to_color_map={"第四行": self.row_color})
        explain_text02 = TextMobject("只剩下数字8未出现")
        explain_text03 = TextMobject("因而第四行空缺的格子应填8", tex_to_color_map={"第四行": self.row_color})
        explain_text04 = TextMobject("同理,第五宫空缺的格子应填3", tex_to_color_map={"第五宫": self.box_color})

        explain_text05 = TextMobject("摒除：再看第七宫，还需填1、9两数", tex_to_color_map={"第七宫": self.box_color})
        explain_text06 = TextMobject("由于一行中每个数字只能出现一次", tex_to_color_map={"行": self.row_color})
        explain_text07 = TextMobject("而第八行已经有1", tex_to_color_map={"第八行": self.row_color})
        explain_text08 = TextMobject("所以，第七宫只有一格能填1", tex_to_color_map={"第七宫": self.box_color})
        explain_text09 = TextMobject("同理，也有几次摒除同时使用的")

        explain_text10 = TextMobject("解题中…")
        explain_text11 = TextMobject("完成！")

        block_text = TextMobject("四、区块摒除")
        block_explain01 = TextMobject("与刚才使用一个数的方法不同", tex_to_color_map={"一个数": self.board_color})
        block_explain02 = TextMobject("我们还可以用一个区域进行排除", tex_to_color_map={"一个区域": PURPLE})
        block_explain03 = TextMobject("第四宫的1只能出现在紫色区域里",
                                      tex_to_color_map={"第四宫": self.box_color, "紫色": PURPLE})
        block_explain04 = TextMobject("不论1是在哪个格子，对第六宫的效果都是一样的", tex_to_color_map={"第六宫": self.box_color})
        block_explain05 = TextMobject("这两个格子就可以看作一个区块进行摒除", tex_to_color_map={"区块": PINK})
        num1 = TextMobject("1")

        thanks_text = TextMobject("感谢观看，未完待续……")
        name_text = TextMobject("By Zerol Acqua", tex_to_color_map={"Zerol Acqua": self.board_color})

        row_text = TextMobject("行", tex_to_color_map={"行": self.row_color})
        col_text = TextMobject("列", tex_to_color_map={"列": self.col_color})
        box_text = TextMobject("宫", tex_to_color_map={"宫": self.box_color})

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
        block_text.to_edge(UP)
        block_explain01.to_edge(UP)
        block_explain02.to_edge(UP)
        block_explain03.to_edge(UP)
        block_explain04.to_edge(UP)
        block_explain05.to_edge(UP)

        row_text.shift(np.array([-10 * self.scale, 4 * self.scale, 0]))
        col_text.shift(np.array([2 * self.scale, 10 * self.scale, 0]))
        box_text.shift(np.array([-6 * self.scale, -9 * self.scale, 0]))

        ## 动画

        ## 格子
        self.show_grid()

        ## 数字
        self.show_num()

        ## 盘面介绍
        self.play(ApplyMethod(self.sudoku_group.next_to, introdution.get_edge_center(DOWN), DOWN))
        self.play(Write(introdution))
        self.wait(2)

        ## 行
        self.play(Transform(introdution, row_text),
                  ApplyMethod(self.sudoku_group.next_to,
                              row_text.get_edge_center(RIGHT) + np.array([0, -4 * self.scale, 0]),
                              RIGHT))
        self.row_highlight(2)

        ## 列
        self.play(Transform(introdution, col_text),
                  ApplyMethod(self.sudoku_group.next_to,
                              col_text.get_edge_center(DOWN) + np.array([-2 * self.scale, 0, 0]),
                              DOWN))
        self.col_highlight(5)

        ## 宫
        self.play(Transform(introdution, box_text),
                  ApplyMethod(self.sudoku_group.next_to,
                              box_text.get_edge_center(UP) + np.array([6 * self.scale, 0, 0]),
                              UP))
        self.box_highlight(6)

        ## 规则介绍
        self.play(Transform(introdution, rule_title),
                  ApplyMethod(self.sudoku_group.next_to, rule_title.get_edge_center(DOWN), DOWN))
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
                  ApplyMethod(self.sudoku_group.next_to, explain_title.get_edge_center(DOWN), DOWN))
        self.wait(2)
        self.play(FadeOut(rule_text03))

        self.play(Write(explain_text01))
        self.wait(1)
        self.play(Transform(explain_text01, explain_text02))
        self.wait(1)
        self.play(Transform(explain_text01, explain_text03))
        self.wait(1)
        self.row_highlight(3)
        self.solve(3, 1, 8)
        self.play(FadeOut(explain_text01))

        self.play(Write(explain_text04))
        self.wait(1)
        self.box_highlight(4)
        self.solve(4, 4, 3)
        self.play(FadeOut(explain_text04))

        self.play(Write(explain_text05))
        self.wait(1)
        self.box_highlight(6)
        self.play(Transform(explain_text05, explain_text06))
        self.wait(1)
        self.play(Transform(explain_text05, explain_text07))
        self.wait(1)
        self.play(Transform(explain_text05, explain_text08))
        self.note(7, 8, 1, 0)
        self.show_note()
        self.solve(6, 1, 1)
        self.erase_note()
        self.wait(1)
        self.play(FadeOut(explain_text05))

        self.play(Write(explain_text09))
        self.wait(1)
        self.box_highlight(5)
        self.note(7, 7, 2, 1)
        self.note(1, 6, 2, 0)
        self.note(5, 0, 1, 1)
        self.show_note()
        self.solve(4, 8, 7)
        self.erase_note()

        self.wait(1)
        self.play(Transform(explain_text09, explain_text10))
        self.box_highlight(6)
        self.solve(7, 1, 9)

        self.note(8, 0, 1, 1)
        self.show_note()
        self.box_highlight(8)
        self.solve(6, 7, 8)
        self.erase_note()

        self.solve(8, 7, 9)

        self.note(4, 3, 1, 1)
        self.show_note()
        self.col_highlight(6)
        self.solve(5, 6, 8)
        self.erase_note()

        self.solve(4, 6, 9)

        self.note(4, 4, 1, 1)
        self.show_note()
        self.box_highlight(5)
        self.solve(5, 8, 3)
        self.erase_note()

        self.solve(4, 7, 4)

        self.row_highlight(5)
        self.solve(5, 1, 4)

        self.note(0, 1, 2, 0)
        self.note(6, 0, 2, 1)
        self.show_note()
        self.box_highlight(3)
        self.solve(4, 2, 6)
        self.erase_note()

        self.note(1, 0, 2, 0)
        self.show_note()
        self.solve(4, 1, 2)
        self.erase_note()

        self.solve(4, 0, 1)

        self.col_highlight(0)
        self.solve(0, 0, 4)

        self.col_highlight(1)
        self.solve(1, 1, 5)

        self.col_highlight(2)
        self.solve(0, 2, 9)

        self.note(1, 1, 1, 1)
        self.show_note()
        self.col_highlight(7)
        self.solve(2, 7, 5)
        self.erase_note()

        self.solve(1, 7, 1)

        self.note(3, 5, 2, 1)
        self.note(4, 5, 2, 1)
        self.show_note()
        self.row_highlight(0)
        self.solve(0, 5, 1)
        self.erase_note()

        self.note(0, 5, 2, 0)
        self.note(4, 5, 2, 0)
        self.show_note()
        self.row_highlight(8)
        self.solve(8, 5, 2)
        self.erase_note()

        self.note(5, 3, 2, 0)
        self.show_note()
        self.row_highlight(8)
        self.solve(8, 4, 1)
        self.erase_note()

        self.solve(8, 3, 5)

        self.note(8, 3, 2, 1)
        self.show_note()
        self.row_highlight(0)
        self.solve(0, 4, 5)
        self.erase_note()

        self.solve(0, 3, 7)

        self.note(0, 3, 2, 0)
        self.show_note()
        self.row_highlight(6)
        self.solve(6, 4, 7)
        self.erase_note()

        self.solve(6, 3, 9)

        self.note(3, 3, 2, 1)
        self.note(8, 5, 2, 1)
        self.note(1, 0, 1, 1)
        self.show_note()
        self.box_highlight(1)
        self.solve(2, 4, 2)
        self.erase_note()

        self.note(1, 2, 1, 1)
        self.show_note()
        self.col_highlight(4)
        self.solve(7, 4, 8)
        self.erase_note()

        self.solve(1, 4, 9)

        self.note(1, 4, 1, 1)
        self.show_note()
        self.col_highlight(8)
        self.solve(2, 8, 9)
        self.erase_note()

        self.solve(1, 8, 4)

        self.note(4, 3, 2, 1)
        self.show_note()
        self.row_highlight(2)
        self.solve(2, 5, 8)
        self.erase_note()

        self.solve(2, 3, 4)

        self.note(1, 8, 1, 0)
        self.show_note()
        self.col_highlight(5)
        self.solve(7, 5, 4)
        self.erase_note()

        self.solve(1, 5, 6)

        self.box_highlight(1)
        self.solve(1, 3, 3)

        self.box_highlight(7)
        self.solve(7, 3, 6)

        self.wait(1)
        self.play(Transform(explain_text09, explain_text11))
        self.wait(1)
        self.play(FadeOut(explain_text09))
        self.wait(2)
        #################################################################################
        self.change_num("test/test02.txt")
        self.show_num()
        self.wait(1)
        self.play(Write(block_text))
        self.wait(2)
        self.play(ReplacementTransform(block_text, block_explain01))
        self.wait(1)
        self.play(ReplacementTransform(block_explain01, block_explain02))
        self.wait(1)

        self.note(0, 1, 0, 0)
        self.show_note()
        self.wait(1)
        self.add_num_highlight(5, 0)
        self.add_num_highlight(5, 2)
        self.show_num_highlight()

        self.play(ReplacementTransform(block_explain02, block_explain03))
        self.wait(2)

        self.play(ReplacementTransform(block_explain03, block_explain04))
        self.erase_note()
        tmp1 = self.note(5, 0, 1, True)
        tmp2 = self.note(5, 2, 1, True)
        tmp3 = tmp1.copy()
        num1.move_to(self.get_grid_center(5, 0))
        self.play(Write(num1), Write(tmp1))
        self.play(ApplyMethod(num1.move_to, self.get_grid_center(5, 2)), ReplacementTransform(tmp1, tmp2))
        self.wait(1)
        self.play(ApplyMethod(num1.move_to, self.get_grid_center(5, 0)), ReplacementTransform(tmp2, tmp3))
        self.solve(4, 8, 1)

        self.play(Uncreate(num1), Uncreate(tmp3))
        self.clear_note()
        self.wait(1)

        self.play(ReplacementTransform(block_explain04, block_explain05))
        self.erase_num_highlight()
        self.add_num_highlight(5, 0)
        self.add_num_highlight(5, 2)
        self.show_num_highlight()
        self.erase_num_highlight()
        self.play(FadeOut(block_explain05))
        self.wait(1)

        ################################################################################

        self.play(Transform(self.sudoku_group, thanks_text))
        self.wait(1)
        self.play(Transform(self.sudoku_group, name_text))
        self.wait(1)


