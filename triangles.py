from dataclasses import dataclass
from enum import Enum
from typing import List, Dict
from datetime import datetime
import numpy as np
import copy

class TriangleDict(Enum):
    VERTEX_A = 'vertex_a'
    VERTEX_B = 'vertex_b'
    VERTEX_C = 'vertex_c'

HOUR_IN_MS = 3600000

class Triangle:
    a_x = 0.0
    a_y = 0.0
    b_x = 0.0
    b_y = 0.0
    b_ema_55 = 0
    c_x = 0.0
    c_y = 0.0

class Triangles():
    def __init__(self, o, h, l, c, v, t, ema_5, ema_21, ema_55) -> None:
        self.list_of_triangles: List[Triangle] = []
        self.triangle = Triangle()
        self.triangle.a_x = t[0]
        self.triangle.a_y = l[0]
        is_long_ready = False
        in_long = False
        tp = 0
        sl = 0
        open_price = 0
        profit_pct = 1
        for i in range(0, len(c)):
            is_new_triangle = self.__append_candle(o, h, l, c, v, t, i, ema_5, ema_21, ema_55)
            if is_new_triangle:
                is_long_ready = True
            elif is_long_ready and not in_long:
                if np.all(0<(c[i-2:i]-o[i-2:i])) and c[i] > self.list_of_triangles[-1].c_y:
                    open_price = c[i]
                    tp = self.list_of_triangles[-1].b_ema_55
                    sl = self.list_of_triangles[-1].c_y
                    print("open_price: " + str(open_price))
                    print("sl: " + str(sl))
                    print("tp: " + str(tp))
                    in_long = True
                    is_long_ready = False
                    print("long opened")
            elif in_long:
                if l[i] < sl:
                    pct = sl/open_price
                    print("long lost: " + str(pct))
                    in_long = False
                    profit_pct *= pct
                elif h[i] > tp:
                    pct = tp/open_price
                    print("long won: " + str(pct))
                    in_long = False
                    profit_pct *= pct
        print("\n### profit_ptc: " + str(profit_pct))

    def __append_candle(self, o, h, l, c, v, t, i, ema_5, ema_21, ema_55) -> bool:
        if self.triangle.b_x == 0 and l[i] < self.triangle.a_y and ema_21[i] < ema_55[i]:
            self.triangle.a_x = t[i]
            self.triangle.a_y = l[i]
            return False
        elif self.triangle.c_x == 0 and t[i] > self.triangle.a_x + (5*HOUR_IN_MS) and self.triangle.b_y < h[i] and ema_21[i] > ema_55[i]:
            self.triangle.b_x = t[i]
            self.triangle.b_y = h[i]
            self.triangle.b_ema_55 = ema_55[i]
            return False
        elif self.triangle.a_x != 0 and self.triangle.b_x != 0 and t[i] > self.triangle.b_x + (2*HOUR_IN_MS) and l[i] < (self.triangle.a_y*1.01) and ema_21[i] < ema_55[i]:
            self.triangle.c_x = t[i]
            self.triangle.c_y = l[i]
            self.__print()
            self.list_of_triangles.append(copy.deepcopy(self.triangle))
            self.triangle.a_x = t[i]
            self.triangle.a_y = l[i]
            self.triangle.b_x = 0
            self.triangle.b_y = 0
            self.triangle.c_x = 0
            self.triangle.c_y = 0
            return True
        elif self.triangle.a_x != 0 and self.triangle.b_x != 0 and ema_21[i-1] < ema_55[i-1] and ema_21[i] > ema_55[i]:
            self.triangle.a_x = t[i]
            self.triangle.a_y = l[i]
            self.triangle.b_x = 0
            self.triangle.b_y = 0
            self.triangle.c_x = 0
            self.triangle.c_y = 0
            return False

    def __print(self):
        print("\n### new triangle:")
        print(datetime.fromtimestamp(float(self.triangle.a_x)/1000).strftime("%y.%m.%d.%H:%M"))
        print(self.triangle.a_y)
        print(datetime.fromtimestamp(float(self.triangle.b_x)/1000).strftime("%y.%m.%d.%H:%M"))
        print(self.triangle.b_y)
        print(datetime.fromtimestamp(float(self.triangle.c_x)/1000).strftime("%y.%m.%d.%H:%M"))
        print(self.triangle.c_y)
