# Madoku
Showing how to solve a sudoku with manim

> 最近在学习3b1b的 [manim](https://github.com/3b1b/manim) ，自己在学习的时候尝试练习一下，很多实现都不太简洁。  
初步设想是把数独盘面、规则讲解以及最基础的技巧结合数独题目介绍一下。~~其他的东西，无限期咕咕吧。  
自己也是第一次用github,就当是代码，还有学习的记录吧~~
# 
> 作者：***Hu_Lechen/HappyLakeCity/Zerol_Acqua***与***Naxi-s/ tucoconum***    
最新版本日期：**2020/11/10**   
文档更新日期：**2021/1/23**   
感谢@Naxi-s全力地支持与合作，代码将在近期进行更新   
原先的代码已经放入old文件夹中
# 
> [我们使用的MK版本的链接](https://github.com/manim-kindergarten)

#  Sudoku_scene类
## 一、概述
- Sudoku_scene类是Scene的子类，定义了数独盘面，已知数候选数的读取，以及一些基础的数独解法演示函数。可以强调行、列、宫，特定的若干格子和特定若干候选数，可以引出辅助线，填写数字时可以清除相应的候选数
## 二、用法
1.准备工作

- 创建一个**create_board**的子类，在**construct**中使用**create_board**函数构造数独盘面，并使用相关函数**show_grid**和**show_num**播放盘面和已知数的出现的动画。
- （可选）使用**load_cand**载入候选数，**show_cand**播放候选数出现的动画
- （可选）使用**change_num**重新载入已知数
