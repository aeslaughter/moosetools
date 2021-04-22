#* This file is part of MOOSETOOLS repository
#* https://www.github.com/idaholab/moosetools
#*
#* All rights reserved, see COPYRIGHT for full restrictions
#* https://github.com/idaholab/moosetools/blob/main/COPYRIGHT
#*
#* Licensed under LGPL 2.1, please see LICENSE for details
#* https://www.gnu.org/licenses/lgpl-2.1.html

import subprocess
from TestHarnessTestCase import TestHarnessTestCase


class TestHarnessTester(TestHarnessTestCase):
    def testRaceConditions(self):
        """
        Test for Race Conditions in the TestHarness
        """

        # Check for the words 'Diagnostic analysis' which indicate that race conditions exist
        with self.assertRaises(subprocess.CalledProcessError) as cm:
            self.runTests('--pedantic-checks', '-i', 'output_clobber_simple')
        e = cm.exception
        self.assertIn('Diagnostic analysis', e.output.decode('utf-8'))
