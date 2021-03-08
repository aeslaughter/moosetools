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

def main():
    window = chigger.Window(size=(400, 400))
    viewport = chigger.Viewport()

    reader = chigger.exodus.ExodusReader('../input/step10_micro_out.e', timestep=0)
    mug = chigger.exodus.ExodusSource(reader=reader, variable='phi', lim=(0, 1))

    test = chigger.observers.TestObserver()
    for i in [0,4,9]:
        filename = 'adapt_' + str(i) + '.png'
        test.setObjectOptions(reader, timestep=i)
        test.assertImage(filename)

    window.start()

class TestHelp(unittest.TestCase):
    def test(self):
        self.assertFalse(main(), "Failed to execute script without errors.")

if __name__ == '__main__':
    import sys
    sys.exit(main())
