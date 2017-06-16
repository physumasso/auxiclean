import pep8
import os
import auxiclean
from nose.tools import assert_equal

# Add pep8 codes to ignore below
PEP8_ADDITIONAL_IGNORE = []
# add files to ignore below
EXCLUDE_FILES = []


def test_pep8_conformance():

    dirs = []
    dirname = os.path.dirname(auxiclean.__file__)
    dirs.append(dirname)

    pep8style = pep8.StyleGuide()

    # Extends the number of pep8 guidelines which are not checked
    pep8style.options.ignore += tuple(PEP8_ADDITIONAL_IGNORE)
    pep8style.options.exclude.extend(EXCLUDE_FILES)

    result = pep8style.check_files(dirs)
    msg = "Found code syntax errors (and warnings)!"
    assert_equal(result.total_errors, 0, msg)
