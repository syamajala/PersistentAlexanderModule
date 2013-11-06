#!/usr/bin/sage -python
from sage.all import *


class Box():

    def __init__(self, top=False, bottom=False, left=False, right=False, 
                 hh=False):

        self.t = top
        self.b = bottom
        self.l = left
        self.r = right
        self.hh = hh

    def relation(self):
        if hh == 'tl':
            return (self.b^-1)*(self.r^-1)*self.t*self.l
        elif hh == 'tr':
            return (self.l^-1)*(self.t^-1)*self.r*self.b

    def __str__(self):
        return str((self.t, self.b, self.l, self.r, self.hh))


class Crossing():

    def __init__(self, aos, aus, os, us):
        self.aos = aos
        self.aus = aus
        self.os = os
        self.us = us

    def __str__(self):
        return str((self.aos, self.aus, self.os, self.us))


class Wirtinger():

    def __init__(self, braid):
        self.braid = braid

        gens = []
        c = 0
        for i in range(0, len(self.braid)):
            gens.append('x'+str(c))
            c = c + 1

        self.g = FreeGroup(gens)
        self.g.inject_variables()

        self.crossings = self.build_crossings()

    def build_crossings(self):

        crossings = []

        for i in self.braid:
            if not crossings:
                if i > 0:
                    previ = i
                    crossings.append(Crossing(i, i+1, i, i+1))
            else:
                c = crossings[-1]
                if i > 0:
                    if c.os == i and previ > 0:
                        crossings.append(Crossing(c.aus, c.aos, c.os, c.us))
                    elif c.os == i-1 and previ > 0:
                        crossings.append(Crossing(c.aos, c.aus+1, c.aus, 
                                                  c.aus+1))
                    elif c.os == i and previ < 0:
                        crossings.append(Crossing(c.aus, c.us, c.aus, c.aos))
                    elif c.us == i+1 and previ < 0:
                        crossings.append(Crossing(c.aus+1, c.aos, c.aus, c.us))
                elif i < 0:
                    if c.os == -1*(i-1):
                        crossings.append(Crossing(c.aus, c.os, c.os, c.aos))
                    elif c.aus == -1*i:
                        crossings.append(Crossing(c.aus+1, c.aos, c.us+1, 
                                                  c.aus))
                    elif c.aos == -1*i:
                        crossings.append(Crossing(c.os, c.us, c.aus, c.aos))
                previ = i

        return crossings

    def build_boxes(self):

        gen = 0
        boxes = [Box() for i in range(0, len(self.braid))]

        strands = max(map(abs, self.braid))+1
        
        for s in range(1, strands+1):
            for i, j in enumerate(self.crossings):
                if j.aos == s:
                    boxes[i].top = self.g.gen(gen)
                    print (i, self.g.gen(gen))
                else:
                    gen = (gen + 1)%len(self.braid)

        return boxes

b = [1, -2, 1, -2]
w = Wirtinger(b)

# for i in w.crossings:
#     print i

boxes = w.build_boxes()
for i in boxes:
    print i
