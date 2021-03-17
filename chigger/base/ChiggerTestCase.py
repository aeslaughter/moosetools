import chigger
import unittest
class ChiggerTestCase(unittest.TestCase):
    """
    Base test class for testing chigger functionality.

    This class acts as a wrapper of the chigger.observer.TestObserver object. By default it setups
    a new chigger.Window and chigger.Viewport with the necessary observer for each test.
    """
    SIZE = (300, 300)

    def setUp(self):
        self._window = chigger.Window(size=self.SIZE)
        self._viewport = chigger.Viewport()
        self._test = chigger.observers.TestObserver()

    def pressKey(self, *args, **kwargs):
        self._test.pressKey(*args, **kwargs)

    def setObjectOptions(self, obj, *args, **kwargs):
        self._test.setObjectOptions(obj, *args, **kwargs)

    def assertImage(self, *args, **kwargs):
        self._test.assertImage(*args, **kwargs)

    def assertInConsole(self, *args, **kwargs):
        self._test.assertInConsole(*args, **kwargs)

    def assertNotInConsole(self, *args, **kwargs):
        self._test.assertInConsole(*args, **kwargs)

    def assertInLog(self, *args, **kwargs):
        self._test.assertInLog(*args, **kwargs)

    def assertNotInLog(self, *args, **kwargs):
        self._test.assertNotInLog(*args, **kwargs)

    def _callTestMethod(self, method):
        unittest.TestCase._callTestMethod(self, method)
        self._window.start()
        self.assertFalse(self._test.status())
