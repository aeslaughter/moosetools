from .ExodusSource import ExodusSource
from .ExodusCompositeReader import ExodusCompositeReader
from .. import base
from .. import utils

class ExodusCompositeSource(base.ChiggerCompositeSource):
    @staticmethod
    def validParams():
        params = ExodusSource.validParams()
        params.remove('reader')
        params.add('reader', default=utils.get_current_exodus_composite_reader(), required=True,
                   vtype=ExodusCompositeReader,
                   doc="ExodusCompositeReader object for extracting content for 3D visualization.")
        return params

    def __init__(self, **kwargs):
        base.ChiggerCompositeSource.__init__(self, **kwargs)
        for reader in self.getParam('reader'):
            params = ExodusSource.validParams()
            params.update(self.parameters())
            params.setValue('reader', reader)
            src = ExodusSource(**params.toDict())
            self._addSource(src)
