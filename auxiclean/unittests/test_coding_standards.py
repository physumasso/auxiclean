import pep8
import os
import auxiclean
import unittest


# Add pep8 codes to ignore below
PEP8_ADDITIONAL_IGNORE = []
# add files to ignore below
EXCLUDE_FILES = []


class TestPEP8(unittest.TestCase):
    def test_pep8_conformance(self):

        dirs = []
        dirname = os.path.dirname(auxiclean.__file__)
        dirs.append(dirname)

        pep8style = pep8.StyleGuide()

        # Extends the number of pep8 guidelines which are not checked
        pep8style.options.ignore += tuple(PEP8_ADDITIONAL_IGNORE)
        pep8style.options.exclude.extend(EXCLUDE_FILES)

        result = pep8style.check_files(dirs)
        msg = "Found code syntax errors (and warnings)!"
        self.assertEqual(result.total_errors, 0, msg=msg)
