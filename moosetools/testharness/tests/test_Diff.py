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
    def testDiffs(self):
        """
        Test for Exodiffs, CSVDiffs
        """
        with self.assertRaises(subprocess.CalledProcessError) as cm:
            self.runTests('-i', 'diffs')

        e = cm.exception
        self.assertRegex(e.output.decode('utf-8'), r'test_harness\.exodiff.*?FAILED \(EXODIFF\)')
        self.assertRegex(e.output.decode('utf-8'), r'test_harness\.csvdiff.*?FAILED \(CSVDIFF\)')
        self.assertRegex(e.output.decode('utf-8'), r'test_harness\.jsondiff.*?FAILED \(JSONDIFF\)')
        self.assertRegex(e.output.decode('utf-8'), r'test_harness\.exodiff.*?Running exodiff')
        self.assertRegex(e.output.decode('utf-8'), r'test_harness\.csvdiff.*?Running csvdiff')

        # Verify return code is DIFF related (0x81)
        self.assertIs(0x81, e.returncode)


if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
