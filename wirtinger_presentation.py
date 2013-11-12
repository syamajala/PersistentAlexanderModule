#!/usr/bin/sage -python
from sage.all import *


class Box():

    def __init__(self, top=False, bottom=False, left=False, right=False, 
                 hh=False):

        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right
        self.hh = hh

    def relation(self):
        if self.hh == 'tl':
            return (self.bottom, self.right, self.top, self.left)
        elif self.hh == 'tr':
            return (self.left, self.top, self.right, self.bottom)

    def __str__(self):
        return str((self.top, self.bottom, self.left, self.right, self.hh))

    def __eq__(self, other):
        if ((self.top == other.top) and 
            (self.bottom == other.bottom) and
            (self.left == other.left) and
            (self.right == other.right) and 
            (self.hh == other.hh)):
            return True

        return False
        

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
        self.strands = max(map(abs, self.braid))+1

        gens = []
        c = 1
        for i in range(0, len(self.braid)):
            gens.append('x'+str(c))
            c = c + 1

        self.g = FreeGroup(gens)
        self.g.inject_variables()

        self.crossings = self.build_crossings()
        self.boxes = self.build_boxes()

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

        boxes = [Box() for i in range(0, len(self.braid))]
        m = self.permutation()
        g = 0
        bottomtotop = False

        for s in m:
            for i, j in enumerate(self.crossings):
                if not bottomtotop:
                    if j.aos == s:
                        boxes[i].top = g
                        boxes[i].bottom = g
                    elif j.aus == s and self.braid[i] > 0:
                        boxes[i].right = g
                        g = (g + 1) % len(self.braid)
                        boxes[i].left = g
                    elif j.aus == s and self.braid[i] < 0:
                        boxes[i].left = g
                        g = (g + 1) % len(self.braid)
                        boxes[i].right = g
                elif bottomtotop:
                    if j.aus == s:
                        boxes[i].right = g
                        g = (g + 1) % len(self.braid)
                        boxes[i].left = g
                    elif j.aos == s:
                        boxes[i].top = g
                        boxes[i].top = g
                    bottomtotop = False
            bottomtotop = True

        for i in boxes:
            if i.left == (i.right + 1) % len(self.braid):
                i.hh = "tl"
            elif i.right == (i.left + 1) % len(self.braid):
                i.hh = "tr"

        return boxes

    def permutation(self):
        self.strands = max(map(abs, self.braid))+1
        
        p = {i: PermutationGroupElement("("+str(i)+","+str(i+1)+")") 
             for i in range(1, self.strands)}

        f = PermutationGroupElement("()")

        for i in self.braid:
            if i < 0:
                f = f*p[-1*i].inverse()
            else:
                f = f*p[i]

        m = [1]+[f(i) for i in range(1, self.strands)]

        return m

    def gen_rel(self, r):
        return self.g.gen(r[0]).inverse()*self.g.gen(r[1]).inverse() * \
            self.g.gen(r[2])*self.g.gen(r[3])

    def presentation(self):
        rels = map(self.gen_rel, [i.relation() for i in self.boxes])
        return self.g / rels


def trefoil():
    b = [1, 1, 1]
    w = Wirtinger(b)

    boxes = [Box(0, 0, 2, 1, "tl"),
             Box(2, 2, 1, 0, "tl"), 
             Box(1, 1, 0, 2, "tl")]

    cboxes = w.build_boxes()

    g = w.presentation()
    return g.alexander_matrix()


def figure8():
    b = [1, -2, 1, -2]
    w = Wirtinger(b)

    boxes = [Box(0, 0, 2, 1, "tl"),
             Box(3, 3, 0, 1, "tr"),
             Box(2, 2, 0, 3, "tl"),
             Box(1, 1, 2, 3, "tr")]

    cboxes = w.build_boxes()

    g = w.presentation()
    print g.alexander_matrix()

    return boxes == cboxes


def k5_2():

    b = [1, 1, 1, 2, -1, 2]
    w = Wirtinger(b)

    boxes = [Box(0, 0, 3, 2, "tl"), 
             Box(3, 3, 1, 0, "tl"),
             Box(1, 1, 4, 3, "tl"),
             Box(1, 1, 0, 5, "tl"),
             Box(0, 0, 4, 5, "tr"),
             Box(5, 5, 2, 1, "tl")]

    cboxes = w.build_boxes()

    return boxes == cboxes


def main():
    if not trefoil():
        print "Trefoil error"
    if not figure8():
        print "Figure 8 error"
    if not k5_2():
        print "5_2 error"

main()
