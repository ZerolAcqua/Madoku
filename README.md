# Madoku
Showing how to solve a sudoku with manim

> 最近在学习3b1b的 [manim](https://github.com/3b1b/manim) ，自己在学习的时候尝试练习一下，很多实现都不太简洁。  
初步设想是把数独盘面、规则讲解以及最基础的技巧结合数独题目介绍一下。~~其他的东西，无限期咕咕吧。~~   
自己也是第一次用github,就当是代码，还有学习的记录吧
# 
> 作者：***Hu_Lechen/HappyLakeCity/Zerol_Acqua***与***Naxi-s/ tucoconum***       
文档更新日期：**2021/1/27**   
感谢@Naxi-s全力地支持与合作，代码将在近期进行更新   
原先的代码已经放入old文件夹中
# 
> [我们使用的MK版本的链接](https://github.com/manim-kindergarten)

---

# `SudokuLine`类
- `SudokuLine`类是`Text`的子类，参考@cigar666的`CodeLine`类，定义好了各种关键名词的颜色——`t2c`字典。

---

#  `Sudoku`类
- `Sudoku`类是`VGroup`的子类，定义了数独盘面，已知数、候选数。
- 使用时将已知数字符串赋值给**num_str**，然后调用**create_board()**函数构造数独盘面。
- **类属性**
    *类属性*：以CONFIG字典形式给出
    *实例属性*：主要是存储数独盘面的图形和数字的相关列表和VGroup

- **类方法**
    > _ _ init _ _(self, **kwargs)
 
    调用父类的构造函数，调用_ _create_borad
    # 
    > _ _create_borad(self)
       
    构造一个数独盘面，根据`string1`提供的已知数，在盘面上绘制已知数和候选数
    # 
    > row_check(index1,index2)
    
    （静态函数）用于检查两个编号`index1` `index2`对应的格子是否在同一行
    # 
    > col_check(index1, index2)

    （静态函数）用于检查两个编号`index1` `index2`对应的格子是否在同一列
    # 
    > box_check(index1, index2)
     
    （静态函数）用于检查两个编号`index1` `index2`对应的格子是否在同一宫

    ---

#  `FadeOutWithParticles1`类
- `FadeOutWithParticles1`类是`FadeOut`的子类，用法和FadeOut等动画类是一样的。
- **类属性**
    *类属性*：以CONFIG字典形式给出
    *实例属性*：主要是存储粒子的VGroup和随机方向向量的列表
    -  `self.list1` = []
    -  `self.list2` = []
    -  `self.vg` = VGroup()

- *类方法*
    > _ _ init _ _(self, mobject, **kwargs)
    
    在构造函数中以`mobject`的位置，构造若干个圆或正方形，随机生成它们移动的方向
    # 
    > create_target(self):
     
    返回动画将变换成的“Target”，即最终状态
    # 