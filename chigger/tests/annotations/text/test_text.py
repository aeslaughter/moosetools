#!/usr/bin/env python3
#* This file is part of the MOOSE framework
#* https://www.mooseframework.org
#*
#* All rights reserved, see COPYRIGHT for full restrictions
#* https://github.com/idaholab/moose/blob/master/COPYRIGHT
#*
#* Licensed under LGPL 2.1, please see LICENSE for details
#* https://www.gnu.org/licenses/lgpl-2.1.html
import chigger

class TestImage(chigger.base.ChiggerTestCase):
    def setUp(self):
        super().setUp()
        self._text = chigger.annotations.Text(text='This is a test.')

    def testDefault(self):
        self._test.assertImage('default.png')

    def testFontColor(self):
        self.setObjectOptions(self._text, font_color=chigger.utils.Color(1,0,1))
        self._test.assertImage('font_color.png')

    def testFontOpacity(self):
        self.setObjectOptions(self._text, font_opacity=0.2)
        self._test.assertImage('font_opacity.png')

    def testFontSize(self):
        self.setObjectOptions(self._text, font_size=1)
        self._test.assertImage('font_size.png')



if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
