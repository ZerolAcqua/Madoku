from Package_Sudoku.Sudoku import *

class Sudoku_subset(Sudoku_with_Subset_scene):
    def construct(self):
        ## 设置物体
        self.create_board("test/test03.txt", True)

        ## 盘面
        cand_text = TextMobject("一、候选数", tex_to_color_map={"候选数": self.cand_color})
        cand_explain01 = TextMobject("候选数，顾名思义就是该格可选择的数字", tex_to_color_map={"候选数": self.cand_color})
        cand_explain02 = TextMobject("在盘面上标满数字可能不是首选的方法")
        cand_explain03 = TextMobject("但是可以帮助我们理解一些东西")
        cand_explain04 = TextMobject("1.唯一数法")
        cand_explain05 = TextMobject("注意这一格，候选数只剩下了9",
                                     tex_to_color_map={"剩下": self.board_color, "候选数": self.cand_color})
        cand_explain06 = TextMobject("所以此格只能填9")
        cand_explain07 = TextMobject("没有候选数时，观察难度较高", tex_to_color_map={"候选数": self.cand_color})
        cand_explain08 = TextMobject("这里的已知数都是分散的")
        cand_explain09 = TextMobject("填入9以后，显然它所在的行列宫",
                                     tex_to_color_map={"行": self.row_color, "列": self.col_color, "宫": self.box_color})
        cand_explain10 = TextMobject("都需要删除候选数9", tex_to_color_map={"候选数": self.cand_color})
        cand_explain11 = TextMobject("接下来，我们用唯一数法解题", tex_to_color_map={"唯一数法": self.cand_color})
        cand_explain12 = TextMobject("至此，唯一数法无法使用了", tex_to_color_map={"唯一数法": self.cand_color})
        cand_explain13 = TextMobject("但是别忘了，我们还可以使用摒除法", tex_to_color_map={"摒除法": self.cand_color})
        cand_explain14 = TextMobject("不过，这次我们使用候选数的视角", tex_to_color_map={"摒除法": self.cand_color})
        cand_explain15 = TextMobject("注意这一宫，只有一格可填1", tex_to_color_map={"宫": self.box_color})
        cand_explain16 = TextMobject("如果不用候选数应该是这样的：", tex_to_color_map={"候选数": self.cand_color})
        cand_explain17 = TextMobject("可以看出，这里利用候选数反而难观察一些", tex_to_color_map={"候选数": self.cand_color})
        cand_explain18 = TextMobject("现在，似乎又遇到了瓶颈……")
        cand_explain19 = TextMobject("还记得上次的区块摒除嘛", tex_to_color_map={"区块摒除": self.cand_color})
        cand_explain20 = TextMobject("这次就先自己思考一下吧~")

        block_explain01 = TextMobject("咳咳，注意第一宫的这里", tex_to_color_map={"宫": self.box_color})
        block_explain02 = TextMobject("咳咳，注意第一宫的这里", tex_to_color_map={"宫": self.box_color})
        block_explain03 = TextMobject("咳咳，注意第一宫的这里", tex_to_color_map={"宫": self.box_color})
        block_explain04 = TextMobject("咳咳，注意第一宫的这里", tex_to_color_map={"宫": self.box_color})
        block_explain05 = TextMobject("咳咳，注意第一宫的这里", tex_to_color_map={"宫": self.box_color})

        thanks_text = TextMobject("感谢观看，未完待续……")
        name_text = TextMobject("By Zerol Acqua", tex_to_color_map={"Zerol Acqua": self.board_color})

        ## 位置
        cand_text.to_edge(UP)
        cand_explain01.to_edge(UP)
        cand_explain02.to_edge(UP)
        cand_explain03.to_edge(UP)
        cand_explain04.to_edge(UP)
        cand_explain05.to_edge(UP)
        cand_explain06.to_edge(UP)
        cand_explain07.to_edge(UP)
        cand_explain08.to_edge(UP)
        cand_explain09.to_edge(UP)
        cand_explain10.to_edge(UP)
        cand_explain11.to_edge(UP)
        cand_explain12.to_edge(UP)
        cand_explain13.to_edge(UP)
        cand_explain14.to_edge(UP)
        cand_explain15.to_edge(UP)
        cand_explain16.to_edge(UP)
        cand_explain17.to_edge(UP)
        cand_explain18.to_edge(UP)
        cand_explain19.to_edge(UP)
        cand_explain20.to_edge(UP)

        ## 动画

        ## 格子
        self.show_grid()
        ## 数字
        self.show_num()
        ## 标题
        self.play(ApplyMethod(self.sudoku_group.next_to, cand_text.get_edge_center(DOWN), DOWN))
        self.play(Write(cand_text))
        self.wait(1)
        self.cand_mark()

        self.load_cand("cand/cand03.txt")
        self.show_cand()
        self.play(ApplyMethod(self.cand_group.set_fill, self.cand_color))
        self.play(ApplyMethod(self.cand_group.set_fill, WHITE))
        self.wait(2)

        self.play(ReplacementTransform(cand_text, cand_explain01))
        self.wait(2)
        self.play(ReplacementTransform(cand_explain01, cand_explain02))
        self.wait(2)
        self.play(ReplacementTransform(cand_explain02, cand_explain03))
        self.wait(3)

        self.play(ReplacementTransform(cand_explain03, cand_explain04))
        self.wait(2)
        self.play(ReplacementTransform(cand_explain04, cand_explain05))
        self.add_num_highlight(6, 4)
        self.show_num_highlight()
        self.wait(1)
        self.erase_num_highlight()

        self.play(ReplacementTransform(cand_explain05, cand_explain06))
        self.solve_from_cand(6, 4, 9, False)
        self.wait(2)
        self.play(ReplacementTransform(cand_explain06, cand_explain07))
        self.wait(2)

        self.box_highlight(7)
        self.add_num_highlight(8, 5)
        self.add_num_highlight(6, 5)
        self.add_num_highlight(7, 4)
        self.add_num_highlight(7, 3)
        self.show_num_highlight()
        self.erase_num_highlight()

        self.row_highlight(6)
        self.add_num_highlight(6, 1)
        self.add_num_highlight(6, 8)
        self.add_num_highlight(6, 0)
        self.show_num_highlight()
        self.erase_num_highlight()

        self.col_highlight(4)
        self.add_num_highlight(2, 4)
        self.show_num_highlight()
        self.erase_num_highlight()

        self.add_num_highlight(8, 5)
        self.add_num_highlight(6, 5)
        self.add_num_highlight(7, 4)
        self.add_num_highlight(7, 3)
        self.add_num_highlight(6, 1)
        self.add_num_highlight(6, 8)
        self.add_num_highlight(6, 0)
        self.add_num_highlight(2, 4)
        self.show_num_highlight()
        self.wait(3)

        self.play(ReplacementTransform(cand_explain07, cand_explain08))
        self.wait(3)
        self.erase_num_highlight()

        self.play(ReplacementTransform(cand_explain08, cand_explain09))
        self.wait(2)
        self.play(ReplacementTransform(cand_explain09, cand_explain10))
        self.solve_update_rand(6, 4, 9)
        self.wait(2)

        self.play(ReplacementTransform(cand_explain10, cand_explain11))
        self.solve_from_cand(6, 3, 7)
        self.solve_from_cand(7, 5, 2)
        self.solve_from_cand(7, 6, 1)
        self.solve_from_cand(6, 7, 8)
        self.solve_from_cand(6, 6, 5)
        self.solve_from_cand(6, 2, 1)
        self.solve_from_cand(7, 2, 7)
        self.solve_from_cand(7, 8, 9)
        self.solve_from_cand(8, 0, 8)
        self.solve_from_cand(8, 1, 5)
        self.solve_from_cand(8, 3, 6)
        self.solve_from_cand(8, 4, 4)

        self.wait(3)

        self.play(ReplacementTransform(cand_explain11, cand_explain12))
        self.wait(2)
        self.play(ReplacementTransform(cand_explain12, cand_explain13))
        self.wait(2)
        self.play(ReplacementTransform(cand_explain13, cand_explain14))
        self.wait(2)

        self.play(ReplacementTransform(cand_explain14, cand_explain15))
        self.box_highlight(2)
        self.add_num_highlight(2, 8, 1)
        self.show_num_highlight()
        self.erase_num_highlight()
        self.wait(2)
        self.play(ReplacementTransform(cand_explain15, cand_explain16))
        self.note(0, 0, 1, 1)
        self.note(1, 3, 1, 1)
        self.note(7, 6, 2, 1)
        self.show_note()
        self.wait(1)
        self.erase_note()
        self.wait(2)
        self.solve_from_cand(2, 8, 1)
        self.play(Uncreate(cand_explain16))

        self.box_highlight(5)
        self.add_num_highlight(5, 8, 6)
        self.show_num_highlight()
        self.erase_num_highlight()
        self.solve_from_cand(5, 8, 6)

        self.play(Write(cand_explain17))
        self.wait(4)
        self.play(ReplacementTransform(cand_explain17, cand_explain18))
        self.wait(4)
        self.play(ReplacementTransform(cand_explain18, cand_explain19))
        self.wait(2)
        self.play(ReplacementTransform(cand_explain19, cand_explain20))
        self.wait(2)

        self.play(FadeOut(cand_explain20))
        self.wait(1)