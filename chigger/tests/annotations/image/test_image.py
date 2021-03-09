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

class TestImage(unittest.TestCase):
    def setUp(self):
        self._window = chigger.Window(size=(300,300))
        self._viewport = chigger.Viewport()
        self._moose = chigger.annotations.Image(filename='../../../logos/moose.png')
        self._test = chigger.observers.TestObserver()

    def testDefault(self):
        self._window.write(filename='default.png')
        self._test.assertImage('default.png', threshold=50, averaging=True, shift=True)
        self._window.start()
        self.assertFalse(self._test.status())

    def testWidth(self):
        self._test.setObjectOptions(self._moose, width=1)
        self._test.assertImage('width.png')
        self._window.start()
        self.assertFalse(self._test.status())

    def testHeight(self):
        self._test.setObjectOptions(self._moose, height=1)
        self._test.assertImage('height.png')
        self._window.start()
        self.assertFalse(self._test.status())

    def testHeightAndWidth(self):
        self._test.setObjectOptions(self._moose, width=1, height=1)
        self._test.assertImage('height_and_width.png')
        self._window.start()
        self.assertFalse(self._test.status())

    def testPosition(self):
        self._test.setObjectOptions(self._moose, position=(0.5,0.5))
        self._test.assertImage('position.png', threshold=25, averaging=True, shift=True)
        self._window.start()
        self.assertFalse(self._test.status())

    def testHorizontalAlign(self):
        self._test.setObjectOptions(self._moose, halign='center', width=1, position=(0.5,0.5))
        self._test.assertImage('horizontal_alignment.png')
        self._window.start()
        self.assertFalse(self._test.status())

    def testVeriticalAlign(self):
        self._test.setObjectOptions(self._moose, valign='top', position=(0,1))
        self._test.assertImage('vertical_alignment.png', threshold=50, averaging=True, shift=True)
        self._window.start()
        self.assertFalse(self._test.status())

    def testOpacity(self):
        self._test.setObjectOptions(self._moose, opacity=0.2)
        self._test.assertImage('opacity.png')
        self._window.start()
        self.assertFalse(self._test.status())

if __name__ == '__main__':
    unittest.main(verbosity=2)
