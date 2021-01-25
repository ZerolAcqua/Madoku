# Madoku
Showing how to solve a sudoku with manim

> 最近在学习3b1b的 [manim](https://github.com/3b1b/manim) ，自己在学习的时候尝试练习一下，很多实现都不太简洁。  
初步设想是把数独盘面、规则讲解以及最基础的技巧结合数独题目介绍一下。~~其他的东西，无限期咕咕吧。  
自己也是第一次用github,就当是代码，还有学习的记录吧~~
# 
> 作者：***Hu_Lechen/HappyLakeCity/Zerol_Acqua***与***Naxi-s/ tucoconum***       
文档更新日期：**2021/1/25**   
感谢@Naxi-s全力地支持与合作，代码将在近期进行更新   
原先的代码已经放入old文件夹中
# 
> [我们使用的MK版本的链接](https://github.com/manim-kindergarten)

#`SudokuLine`类
- `SudokuLine`类是`Text`的子类，参考@cigar666的CodeLine类，定义好了各种关键名词的颜色。


#  `Sudoku_Scene`类
- `Sudoku_Scene`类是`Scene`的子类，定义了数独盘面，已知数、候选数。
- 使用时将已知数字符串赋值给**string1**，然后调用**create_board()**函数构造数独盘面。
- 类方法
    >  create_borad(self)
    #   
    构造一个数独盘面，根据`string1`提供的已知数，在盘面上绘制已知数和候选数
    
    > row_check(self,index1,index2)
    # 
    用于检查两个编号`index1` `index2`对应的格子是否在同一行
    
    > col_check(self, index1, index2)
    # 
    用于检查两个编号`index1` `index2`对应的格子是否在同一列
    
    > box_check(self, index1, index2)
    # 
    用于检查两个编号`index1` `index2`对应的格子是否在同一宫
