import math
import vtk
from .. import utils
from .GeometricSource import GeometricSource, GeometricSource2D


class Outline(GeometricSource):
    VTKSOURCETYPE = vtk.vtkOutlineSource

    @staticmethod
    def validOptions():
        opt = GeometricSource.validOptions()
        opt.add('color', vtype=utils.AutoColor, doc="The color of the outline")
        opt.add('linewidth', vtype=(int, float), doc="The linewidth for the outline")
        opt.add('xmin', default=0, vtype=(int, float),
                doc="Minimum x-value in 3D renderer coordinates.")
        opt.add('xmax', default=1, vtype=(int, float),
                doc="Minimum x-value in 3D renderer coordinates.")
        opt.add('ymin', default=0, vtype=(int, float),
                doc="Minimum y-value in 3D renderer coordinates.")
        opt.add('ymax', default=1, vtype=(int, float),
                doc="Maximum y-value in 3D renderer coordinates.")
        opt.add('zmin', default=0, vtype=(int, float),
                doc="Minimum z-value in 3D renderer coordinates.")
        opt.add('zmax', default=1, vtype=(int, float),
                doc="Maximum z-value in 3D renderer coordinates.")
        opt.add("offset", 0, vtype=(int, float),
                doc="The amount, in viewport coordinates, to offset the bounding box")
        return opt

    def _getBounds(self):
        return self._vtksource.GetBounds()

    def _onRequestInformation(self, *args):
        GeometricSource._onRequestInformation(self, *args)
        offset = self.getOption('offset')
        self._vtksource.SetBounds(self.getOption('xmin') - offset, self.getOption('xmax') + offset,
                                  self.getOption('ymin') - offset, self.getOption('ymax') + offset,
                                  self.getOption('zmin') - offset, self.getOption('zmax') + offset)
        if self.isOptionValid('color'):
            self._vtkactor.GetProperty().SetColor(self.getOption('color').rgb())
        self.assignOption('linewidth', self._vtkactor.GetProperty().SetLineWidth)

class Outline2D(GeometricSource2D):
    VTKSOURCETYPE = vtk.vtkOutlineSource

    @staticmethod
    def validOptions():
        opt = GeometricSource2D.validOptions()
        opt.add('color', vtype=utils.AutoColor, doc="The color of the outline")
        opt.add('linewidth', vtype=(int, float), doc="The linewidth for the outline")
        opt.add('xmin', default=0, vtype=(int, float),
                doc="Minimum x-value in relative viewport coordinates.")
        opt.add('xmax', default=1, vtype=(int, float),
                doc="Minimum x-value in relative viewport coordinates.")
        opt.add('ymin', default=0, vtype=(int, float),
                doc="Minimum y-value in relative viewport coordinates.")
        opt.add('ymax', default=1, vtype=(int, float),
                doc="Maximum y-value in relative viewport coordinates.")
        opt.add("offset", 0, vtype=(int, float),
                doc="The amount, in viewport coordinates, to offset the bounding box")
        return opt

    def _onRequestInformation(self, *args):
        GeometricSource2D._onRequestInformation(self, *args)
        self._vtksource.SetBounds(*self._getBounds())
        if self.isOptionValid('color'):
            self._vtkactor.GetProperty().SetColor(self.getOption('color').rgb())
        self.assignOption('linewidth', self._vtkactor.GetProperty().SetLineWidth)

    def _getBounds(self):
        offset = self.getOption('offset')
        xmin = self.getOption('xmin') - offset
        xmax = self.getOption('xmax') + offset
        ymin = self.getOption('ymin') - offset
        ymax = self.getOption('ymax') + offset

        if xmin < 0:
            self.error("The 'xmin' value ({}) is less than zero with offset applied ({}).", xmin, offset)
            xmin = 0
        if ymin < 0:
            self.error("The 'ymin' value ({}) is less than zero with offset applied ({}).", ymin, offset)
            ymin = 0
        if xmax > 1:
            self.error("The 'xmax' value ({}) is greater than one with offset applied ({}).", xmax, offset)
            xmax = 1
        if ymax > 1:
            self.error("The 'ymax' value ({}) is greater than one with offset applied ({}).", ymax, offset)
            ymax = 1

        return (xmin, xmax, ymin, ymax, 0, 0)
