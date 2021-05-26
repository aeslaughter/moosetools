#!/usr/bin/env python3
#pylint: disable=missing-docstring
#* This file is part of the MOOSE framework
#* https://www.mooseframework.org
#*
#* All rights reserved, see COPYRIGHT for full restrictions
#* https://github.com/idaholab/moose/blob/master/COPYRIGHT
#*
#* Licensed under LGPL 2.1, please see LICENSE for details
#* https://www.gnu.org/licenses/lgpl-2.1.html

import chigger

reader = chigger.exodus.ExodusReader('../input/variable_range.e', timestep=0)
mug = chigger.exodus.ExodusResult(reader, variable='u')
cbar = chigger.exodus.ExodusColorBar(mug, colorbar_origin=(0.7,0.25))
window = chigger.RenderWindow(mug, cbar, size=(300,300), test=True)

# Render the results and write a file
t = reader.getTimes()
for i in range(len(t)):
    reader.setOptions(timestep=i)
    window.write('auto_' + str(i) + '.png')
window.start()
