#!/usr/bin/env python3

from moosetools import chigger

window = chigger.Window(observer=True)
viewport = chigger.Viewport()
reader = chigger.exodus.ExodusCompositeReader(pattern='../tests/input/multiapps_out_sub*.e')
source = chigger.exodus.ExodusSource(reader=reader, variable='u')

window.render()

#import vtk
#recorder = vtk.vtkInteractorEventRecorder()
#recorder.SetInteractor(window.getVTKInteractor())
#recorder.SetFileName('record.log')
#recorder.Record()

window.start()
