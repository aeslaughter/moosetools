from .ChiggerObject import ChiggerObject
from .. import utils

class ChiggerCompositeSource(utils.KeyBindingMixin, ChiggerObject):
    @staticmethod
    def validParams():
        opt = ChiggerObject.validParams()
        opt += utils.KeyBindingMixin.validParams()
        opt.add('viewport', default=utils.get_current_viewport(), required=True,
                doc='The chigger.Viewport object that the sources are to be associated')
        return opt

    @staticmethod
    def validKeyBindings():
        bindings = utils.KeyBindingMixin.validKeyBindings()
        return bindings

    def __init__(self, *args, **kwargs):
        ChiggerObject.__init__(self, **kwargs)
        self._sources = list()

    @property
    def _viewport(self):
        """Property so that self._viewport acts like the actual Viewport object."""
        return self.getParam('viewport')

    def _addSource(self, src):
        self._viewport.add(src)
        self._sources.append(src)

    def setParam(self, *args):
        for src in self._sources:
            src.setParam(*args)

    def setParams(self, *args, **kwargs):
        for src in self._sources:
            src.setParams(*args, **kwargs)

    def assignParam(self, *args):
        for src in self._sources:
            src.assignParam(*args)

    """
    def getVTKActors(self):
        for src in self._sources:
            if src.getVTKActor() is not None:
                yield src.getVTKActor()
    """
