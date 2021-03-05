#!/usr/bin/env python3
#* This file is part of the MOOSE framework
#* https://www.mooseframework.org
#*
#* All rights reserved, see COPYRIGHT for full restrictions
#* https://github.com/idaholab/moose/blob/master/COPYRIGHT
#*
#* Licensed under LGPL 2.1, please see LICENSE for details
#* https://www.gnu.org/licenses/lgpl-2.1.html
#import os
import unittest
#import io
#import logging
#import mock
import chigger
#import diff


import vtk

"""
def diff_window(window=chigger.utils.get_current_window(), ssim=0.97, **kwargs):
    window.setOptions(**kwargs)
    filename = window.getOption('filename')
    goldname = os.path.join('gold', filename)
    window.write()
    return diff.compare_images(goldname, filename, structural_similarity=ssim)
"""

def main():
    retcode = 0

    d = vtk.vtkImageDifference()

    window = chigger.Window(size=(400, 400))

    left = chigger.Viewport(xmax=0.5)
    rect0 = chigger.geometric.Rectangle(xmin=0.25, xmax=0.5, ymin=0.25, ymax=0.75, color=(0.5, 0.1, 0.2))
    cube0 = chigger.geometric.Cube(xmin=0.5, xmax=0.8, ymin=0, ymax=0.5, zmin=0.8, zmax=1, color=(0.1, 0.2, 0.8))

    right = chigger.Viewport(xmin=0.5)
    rect1 = chigger.geometric.Rectangle(xmin=0.25, xmax=0.5, ymin=0.25, ymax=0.75, color=(0.2, 0.1, 0.5))
    cube1 = chigger.geometric.Cube(xmin=0.5, xmax=0.8, ymin=0, ymax=0.5, zmin=0.8, zmax=1, color=(0.8, 0.2, 0.1))

    test = chigger.observers.TestObserver(terminate=True)
    test.assertImage('gold/initial.png')
    test.append(lambda: cube0.setOptions(color=(0.2,0.2,0.1)))
    test.assertImage('gold/initial.png')


    #window.setOptions(offscreen=True)
    window.start()

    #retcode += diff_window(window, filename='initial.png')

    #with mock.patch('sys.stdout', new=io.StringIO()) as out:
    #test.pressKey('h')
    #window.start()
    return test.status()


class TestHelp(unittest.TestCase):
    def test(self):
        self.assertFalse(main())


if __name__ == '__main__':
    #unittest.main(buffer=True)
    main()
#window = chigger.Window(size=(400, 400))
#left = chigger.Viewport(xmax=0.5)
#rect0 = chigger.geometric.Rectangle(xmin=0.25, xmax=0.5, ymin=0.25, ymax=0.75, color=(0.5, 0.1, 0.2))
#cube0 = chigger.geometric.Cube(xmin=0.5, xmax=0.8, ymin=0, ymax=0.5, zmin=0.8, zmax=1, color=(0.1, 0.2, 0.8))
#right = chigger.Viewport(xmin=0.5)
#rect1 = chigger.geometric.Rectangle(xmin=0.25, xmax=0.5, ymin=0.25, ymax=0.75, color=(0.2, 0.1, 0.5))
#cube1 = chigger.geometric.Cube(xmin=0.5, xmax=0.8, ymin=0, ymax=0.5, zmin=0.8, zmax=1, color=(0.8, 0.2, 0.1))
#window.start()
