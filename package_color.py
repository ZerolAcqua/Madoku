# -*- coding=utf-8 -*-
from manimlib.imports import *


def trans_cmyk_to_rgb(c, m, y, k):
    R = round(255 * (100 - c) * (100 - k) / 10000)
    G = round(255 * (100 - m) * (100 - k) / 10000)
    B = round(255 * (100 - y) * (100 - k) / 10000)
    rgb_r = str(hex(R)[2:])
    rgb_g = str(hex(G)[2:])
    rgb_b = str(hex(B)[2:])
    if len(rgb_r)<2:
        rgb_r = '0' + str(hex(R)[2:])
    if len(rgb_g)<2:
        rgb_g = '0' + str(hex(G)[2:])
    if len(rgb_b)<2:
        rgb_b = '0' + str(hex(B)[2:])
    return '#' + rgb_r + rgb_g + rgb_b
