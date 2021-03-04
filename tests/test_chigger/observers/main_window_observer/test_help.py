#!/usr/bin/env python3
#* This file is part of the MOOSE framework
#* https://www.mooseframework.org
#*
#* All rights reserved, see COPYRIGHT for full restrictions
#* https://github.com/idaholab/moose/blob/master/COPYRIGHT
#*
#* Licensed under LGPL 2.1, please see LICENSE for details
#* https://www.gnu.org/licenses/lgpl-2.1.html
import unittest
import chigger


class TestHelp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls._window = chigger.Window(size=(400, 400))
        cls._test = chigger.observers.TestObserver()

        cls._left = chigger.Viewport(xmax=0.5)
        cls._rect0 = chigger.geometric.Rectangle(xmin=0.25, xmax=0.5, ymin=0.25, ymax=0.75, color=(0.5, 0.1, 0.2))
        cls._cube0 = chigger.geometric.Cube(xmin=0.5, xmax=0.8, ymin=0, ymax=0.5, zmin=0.8, zmax=1, color=(0.1, 0.2, 0.8))

        cls._right = chigger.Viewport(xmin=0.5)
        cls._rect1 = chigger.geometric.Rectangle(xmin=0.25, xmax=0.5, ymin=0.25, ymax=0.75, color=(0.2, 0.1, 0.5))
        cls._cube1 = chigger.geometric.Cube(xmin=0.5, xmax=0.8, ymin=0, ymax=0.5, zmin=0.8, zmax=1, color=(0.8, 0.2, 0.1))

    def testInitial(self):
        self._window.write(filename='initial[test_help.py].png')


    def testHelp(self):


        self._test.pressKey('h')


#window.start()
