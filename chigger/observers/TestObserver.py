#pylint: disable=missing-docstring
#* This file is part of the MOOSE framework
#* https://www.mooseframework.org
#*
#* All rights reserved, see COPYRIGHT for full restrictions
#* https://github.com/idaholab/moose/blob/master/COPYRIGHT
#*
#* Licensed under LGPL 2.1, please see LICENSE for details
#* https://www.gnu.org/licenses/lgpl-2.1.html
import vtk
import traceback
from .ChiggerObserver import ChiggerObserver
class TestObserver(ChiggerObserver):
    """
    Tool for simulating key strokes and mouse movements.
    """

    @staticmethod
    def validOptions():
        opt = ChiggerObserver.validOptions()
        opt.add('terminate', vtype=bool, default=False, doc="Exit after rendering.")
        opt.add('duration', vtype=(int, float), default=1, doc="Duration to wait in seconds for event trigger.")
        return opt

    def __init__(self, *args, **kwargs):
        ChiggerObserver.__init__(self, *args, **kwargs)

        self._window.getVTKInteractor().CreateOneShotTimer(int(self.getOption('duration'))*1000)
        self.addObserver(vtk.vtkCommand.TimerEvent, self._onEvent)
        self._actions = list()
        self._retcode = 0

    def append(self, func):
        self._actions.append(func)

    def assertImage(self, *args, **kwargs):
        self.append(lambda: self._assertImage(*args, **kwargs))




    def _assertImage(self, filename):
        gold = vtk.vtkPNGReader()
        gold.SetFileName(filename)

        current = vtk.vtkWindowToImageFilter()
        current.SetInput(self._window.getVTKWindow())

        diff = vtk.vtkImageDifference()
        diff.SetInputConnection(current.GetOutputPort())
        diff.SetImageConnection(gold.GetOutputPort())
        diff.Update()

        if diff.GetThresholdedError():
            self._window.write(filename=filename)

            writer = vtk.vtkPNGWriter()
            writer.SetInputConnection(diff.GetOutputPort())
            writer.SetFileName("diff.png")
            writer.Write()


        return diff.GetThresholdedError(), str(diff)





    def pressKey(self, key, shift=False):
        """
        Simulate a key press.

        Inputs:
            key[str]: The key symbol (e.g. "k").
            shift[bool]: Flag for holding the shift key.
        """
        self._actions.append(lambda: self._pressKey(key, shift))

    def moveMouse(self, x, y): #pylint: disable=invalid-name
        """
        Simulate a mouse movement.

        Inputs:
            x[float]: Position relative to the current window size in the horizontal direction.
            y[float]: Position relative to the current window size in the vertical direction.
        """
        self._actions.append(lambda: self._moveMouse(x, y))

    def pressLeftMouseButton(self):
        self._actions.append(lambda: self._pressLeftMouseButton())

    def _pressLeftMouseButton(self):
        """
        Simulate a left mouse click.
        """
        vtkinteractor = self._window.getVTKInteractor()
        vtkinteractor.InvokeEvent(vtk.vtkCommand.LeftButtonPressEvent, vtkinteractor)

    def _moveMouse(self, x, y):
        # Determine relative position
        sz = self._window.getVTKWindow().GetSize()
        pos = [sz[0] * x, sz[1] * y]

        # Move the mouse
        vtkinteractor = self._window.getVTKInteractor()
        vtkinteractor.SetEventPosition(int(pos[0]), int(pos[1]))
        vtkinteractor.InvokeEvent(vtk.vtkCommand.MouseMoveEvent, vtkinteractor)

    def _pressKey(self, key, shift=False):
        self.info('Press Key: {} shift={}', key, shift)
        vtkinteractor = self._window.getVTKInteractor()
        vtkinteractor.SetKeySym(key)
        vtkinteractor.SetShiftKey(shift)
        vtkinteractor.InvokeEvent(vtk.vtkCommand.KeyPressEvent, vtkinteractor)
        vtkinteractor.SetKeySym(None)
        vtkinteractor.SetShiftKey(False)

    def status(self):
        return self._retcode

    def _onEvent(self, *args, **kwargs):
        self.debug("Execute event")

        for action in self._actions:
            out = action()
            if out is not None:
                self._retcode += out[0]
                if out[0]:
                    print(traceback.extract_stack())
                    print(out[1])
                    break

        if self.getOption('terminate'):
            self.terminate()
